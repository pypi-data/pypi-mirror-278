#################################################################################
#     OscilloWatch, early warning application for low-frequency oscillations
#     Copyright (C) 2024  Maurits Sørensen Molberg
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.
#################################################################################

from time import time
import copy

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

from OscilloWatch.HHT import HHT
from OscilloWatch.OWSettings import OWSettings


class SegmentAnalysis:
    """
    Class for determining the different oscillating modes and their damping in a signal segment by performing HHT and
    interpreting the Hilbert spectrum.
    """

    def __init__(self, input_signal, settings: OWSettings, previous_segment=None, timestamp=""):
        """
        Constructor for the SegmentAnalysis class. Initializes variables, but does not perform the actual analysis.

        :param numpy.ndarray | list input_signal: Signal segment to be analyzed.
        :param OWSettings settings: Object containing the settings for the different algorithms used in the signal
         analysis.
        :param SegmentAnalysis | None previous_segment: SegmentAnalysis object of the previous segment.
        :param datetime.datetime timestamp: Timestamp in datetime format.
        """
        self.input_signal = input_signal
        self.settings = settings
        self.previous_segment = copy.deepcopy(previous_segment)

        self.hht = HHT(self.input_signal, self.settings)

        self.mode_info_list = []
        self.runtime = 0

        self.timestamp = timestamp

    def interpolate_signal(self, signal, mode_info_dict):
        """
        Fills in zero-values of a signal using cubic spline interpolation. Deletes sequences of non-zero values that are
        too short to be assumed to be meaningful. Disregards all zero-elements before and after the first and last non-
        zero element. Updates info about where this sequence starts and ends in the dict damping_info, which is a
        parameter. Intended to be used on a row in a Hilbert spectrum.

        :param numpy.ndarray signal: Amplitude curve containing zeros. Intended to be a single or combined row from a
            Hilbert spectrum containing the amplitude of a single oscillating mode.
        :param dict mode_info_dict: Dict containing info about the oscillating mode that is to be analyzed.

        :return: Copy of the portion of the input signal that starts at the first non-zero and ends at the last, with
            zero-values in-between non-zero values filled in.
        :rtype: numpy.ndarray
        """
        # Find the indices of non-zero values
        non_zero_indices = np.nonzero(signal)[0]
        non_zero_indices = remove_short_consecutive_sequences(non_zero_indices,
                                                              self.settings.minimum_consecutive_non_zero_length)
        # If there are no non-zero values, return the original signal
        if not len(non_zero_indices):
            return signal
        
        start_index = non_zero_indices[0]
        end_index = non_zero_indices[-1] + 1
        
        first_max_index = np.argmax(signal)
        if self.settings.start_amp_curve_at_peak and first_max_index <= len(signal[start_index:end_index])/2:
            start_index = first_max_index

        mode_info_dict["start_time"] = start_index/self.settings.fs
        mode_info_dict["end_time"] = end_index/self.settings.fs

        # Ignore all zero values before the first and after the last non-zero value
        cropped_signal = signal[start_index:end_index]

        # Recalculate non_zero_indices based on the cropped signal
        non_zero_indices = np.nonzero(cropped_signal)[0]
        mode_info_dict["interp_frac"] = 1 - len(non_zero_indices)/len(cropped_signal)
        if mode_info_dict["interp_frac"] > self.settings.max_interp_fraction:
            if self.settings.skip_storing_uncertain_modes:
                return None
            mode_info_dict["uncertain_mode_flag"] = True

        # Get the corresponding non-zero values and their indices
        non_zero_values = [cropped_signal[i] for i in non_zero_indices]

        # Generate the new signal with interpolated values
        new_signal = []
        for i, value in enumerate(cropped_signal):
            if not value:
                new_signal.append(float(np.interp(i, non_zero_indices, non_zero_values)))
            else:
                new_signal.append(value)
        return new_signal

    def analyze_frequency_band(self, amp_curve, bottom_row_ind, top_row_ind):
        """
        Analyzes the damping of a frequency band by curve fitting an amplitude curve to a decaying exponential curve.
        Removes zero-values before and after the first and last non-zero value and interpolates the remaining curve
        before curve fitting. Stores the following information about the frequency band in a dict that is added to the
        DampingAnalysis object's damping_info_list dict.

        :param numpy.ndarray amp_curve: Single or combined row from Hilbert spectrum that is being analyzed.
        :param int bottom_row_ind: Index of the bottom row in the frequency band that is being analyzed.
        :param int top_row_ind: Index of the top row in the frequency band that is being analyzed.
        :return: None
        """
        non_zero_fraction = np.count_nonzero(amp_curve)/len(amp_curve)

        mode_info_dict = {"mode_status": "",
                          "damping_evaluation": "",
                          "alarm": "",
                          "frequency": self.estimate_frequency(bottom_row_ind, top_row_ind),
                          "median_amp": 0.0,
                          "damping_ratio": 0.0,
                          "start_time": 0.0,
                          "end_time": 0.0,
                          "init_amp": 0.0,
                          "final_amp": 0.0,
                          "freq_start": self.hht.freq_axis[bottom_row_ind],
                          "freq_stop": self.hht.freq_axis[top_row_ind],
                          "init_amp_est": 0.0,
                          "decay_rate": 0.0,
                          "NZF": non_zero_fraction,
                          "interp_frac": 0.0,
                          "CV": 0.0,
                          
                          "inaccurate_damping_flag": False,
                          "uncertain_mode_flag": False}

        interp_amp_curve = self.interpolate_signal(amp_curve, mode_info_dict)  # Updates dict

        # If interpolated fraction is too high and skip storing is enabled (interpolate_signal() returns None)
        if interp_amp_curve is None:
            return

        # Curve fit to find approximate initial amplitude and decay rate
        time_points = np.linspace(0, len(interp_amp_curve)/self.settings.fs, len(interp_amp_curve))
        popt, _ = 0, 0
        try:
            popt, _ = curve_fit(exponential_decay_model, time_points, interp_amp_curve, maxfev=1500)
        except Exception as e:
            mode_info_dict["damping_ratio"] = "N/A (SciPy curve fit failed)."
            self.mode_info_list.append(mode_info_dict)
            print(f"Exception occurred during curve fit: {e}. Skipped and added note in CSV.")
            return
        A, decay_rate = popt[0], popt[1]

        # Uncomment to get a plot for the mode's amplitude curve and fitted exponential curve:
        # plt.figure()
        # plt.plot(time_points, interp_amp_curve, label="Amplitude curve w. interpolation")
        # plt.plot(time_points, exponential_decay_model(time_points, A, decay_rate), label="Fitted curve",
        #         linestyle="dashed")
        # plt.xlabel("Time [s]")
        # plt.ylabel("Amplitude")
        # plt.legend()
        # plt.tight_layout()
        # plt.show()

        mode_info_dict["CV"]\
            = (np.std(interp_amp_curve - exponential_decay_model(time_points, A, decay_rate)) /
               np.mean(interp_amp_curve))
        if mode_info_dict["CV"] > self.settings.max_coefficient_of_variation:
            mode_info_dict["inaccurate_damping_flag"] = True

        mode_info_dict["median_amp"] = np.median(interp_amp_curve)
        mode_info_dict["init_amp"] = interp_amp_curve[0]
        mode_info_dict["final_amp"] = interp_amp_curve[-1]

        mode_info_dict["init_amp_est"] = A
        mode_info_dict["decay_rate"] = decay_rate

        mode_info_dict["damping_ratio"] = decay_rate/(np.sqrt(decay_rate**2 + (2*np.pi*mode_info_dict["frequency"])**2))

        self.mode_alarm_evaluation(mode_info_dict)  # Updates dict

        self.mode_info_list.append(mode_info_dict)
        return

    def estimate_frequency(self, bottom_row_ind, top_row_ind):
        """
        Finds and returns the frequency most likely to be the true frequency of the detected mode, based on the number
        of non-zero values in Hilbert Spectrum rows.

        :param int bottom_row_ind: Index of the bottom row in the frequency band that is being analyzed.
        :param int top_row_ind: Index of the top row in the frequency band that is being analyzed.
        :return: Value of estimated frequency of the mode.
        :rtype: float
        """
        max_non_zero_count = 0
        freq_est_row_ind = bottom_row_ind
        for row_ind in range(bottom_row_ind, top_row_ind + 1):
            non_zero_count = np.count_nonzero(self.hht.hilbert_spectrum[row_ind])
            if non_zero_count > max_non_zero_count:  # New frequency estimate found
                max_non_zero_count = non_zero_count
                freq_est_row_ind = row_ind
            elif non_zero_count == max_non_zero_count and max_non_zero_count != 0:  # Two equally likely frequencies
                #print(f"Equally likely {self.hht.freq_axis[freq_est_row_ind]:.3f} and {self.hht.freq_axis[row]:.3f}")
                freq_est_row_ind = (row_ind + freq_est_row_ind)//2  # Take average frequency of the two estimates
        return self.hht.freq_axis[freq_est_row_ind]

    def mode_alarm_evaluation(self, mode_info_dict):
        """
        Checks if mode should raise an alarm and adds the correct alarm message to mode_info_dict if so.
        :param mode_info_dict: Dict with estimated characteristics of the mode.
        :return: None
        """
        # Check if mode is new or sustained
        sustained_osc_flag = False
        if self.previous_segment is not None:
            for mode in self.previous_segment.mode_info_list:
                if abs(mode["frequency"] - mode_info_dict["frequency"]) <= self.settings.segment_memory_freq_threshold:
                    sustained_osc_flag = True
                    break

        if sustained_osc_flag:
            mode_info_dict["mode_status"] = "Sustained"
        else:
            mode_info_dict["mode_status"] = "New"

        if mode_info_dict["damping_ratio"] < 0:
            mode_info_dict["damping_evaluation"] = "Negative"
            if sustained_osc_flag and mode_info_dict["median_amp"] >= self.settings.alarm_median_amplitude_threshold:
                if self.settings.segment_length_time - mode_info_dict["end_time"] <= self.settings.oscillation_timeout:
                    mode_info_dict["alarm"] += "Critical"
                    if self.settings.print_alarms:
                        print(f"Critical alarm for {mode['frequency']:.2f} Hz mode.")
                else:
                    mode_info_dict["alarm"] += "No alarm, ended early"
        elif mode_info_dict["damping_ratio"] <= self.settings.damping_ratio_strong_alarm_threshold:
            mode_info_dict["damping_evaluation"] = "Very low"
            if sustained_osc_flag and mode_info_dict["median_amp"] >= self.settings.alarm_median_amplitude_threshold:
                if self.settings.segment_length_time - mode_info_dict["end_time"] <= self.settings.oscillation_timeout:
                    mode_info_dict["alarm"] += "Strong"
                    if self.settings.print_alarms:
                        print(f"Strong alarm for {mode['frequency']:.2f} Hz mode.")
                else:
                    mode_info_dict["alarm"] += "No alarm, ended early"
        elif mode_info_dict["damping_ratio"] <= self.settings.damping_ratio_weak_alarm_threshold:
            mode_info_dict["damping_evaluation"] = "Low"
            if sustained_osc_flag and mode_info_dict["median_amp"] >= self.settings.alarm_median_amplitude_threshold:
                if self.settings.segment_length_time - mode_info_dict["end_time"] <= self.settings.oscillation_timeout:
                    mode_info_dict["alarm"] += "Weak"
                    if self.settings.print_alarms:
                        print(f"Weak alarm for {mode['frequency']:.2f} Hz mode.")
                else:
                    mode_info_dict["alarm"] += "No alarm, ended early"
        else:
            mode_info_dict["damping_evaluation"] = "Good"

    def analyze_segment(self):
        """
        Runs HHT, uses row combination algorithm on Hilbert spectrum to identify modes, and uses interpolation and
        curve fitting to estimate damping.

        :return: None
        """
        start_time = time()
        self.hht.full_hht()  # Calculate hilbert_spectrum and freq_axis

        # Main loop
        n = 0
        while n < len(self.hht.freq_axis):
            # Row adding loop (add to top)
            # k = 0
            non_zero_count = np.count_nonzero(self.hht.hilbert_spectrum[n])
            if not non_zero_count:
                n += 1
                continue
            combined_row = self.hht.hilbert_spectrum[n]
            combined_row_old = np.copy(combined_row)
            non_zero_count_old = non_zero_count
            k = 1
            while n + k < len(self.hht.freq_axis):
                combined_row_old = np.copy(combined_row)
                non_zero_count_old = non_zero_count
                combined_row = np.maximum(combined_row, self.hht.hilbert_spectrum[n+k])
                non_zero_count = np.count_nonzero(combined_row)
                if non_zero_count - non_zero_count_old > self.settings.minimum_non_zero_improvement \
                    or np.count_nonzero(self.hht.hilbert_spectrum[n+k]) \
                        > self.settings.minimum_total_non_zero_fraction*len(self.input_signal):
                    k += 1
                else:
                    break

            # Row removal loop (remove from bottom)
            m = 1
            while m < k:
                combined_row_old = self.combine_rows(n+m-1, n+k-1)
                non_zero_count_old = np.count_nonzero(combined_row_old)
                combined_row = self.combine_rows(n+m, n+k-1)
                non_zero_count = np.count_nonzero(combined_row)

                row = self.hht.hilbert_spectrum[n+m-1]
                non_zero_count_current = np.count_nonzero(row)
                freq = self.hht.freq_axis[n+m-1]

                if non_zero_count_old - non_zero_count > self.settings.minimum_non_zero_improvement\
                        or np.count_nonzero(self.hht.hilbert_spectrum[n+m])\
                        > self.settings.minimum_total_non_zero_fraction*len(self.input_signal):
                    break
                else:
                    m += 1

            # Calculate and store info if non-zero fraction is large enough
            if non_zero_count_old/len(self.input_signal) > self.settings.minimum_total_non_zero_fraction:
                self.analyze_frequency_band(combined_row_old, n+m-1, n+k-1)
            n += k

        self.runtime = time() - start_time
        if self.settings.print_segment_analysis_time:
            print(f"Segment analysis completed in {self.runtime:.3f} seconds.")

    def combine_rows(self, bottom_row_ind, top_row_ind):
        """
        Combines a range of Hilbert spectrum rows into a single row, where the highest value from the original rows at
        each time point is kept.

        :param int bottom_row_ind: Index in the Hilbert spectrum of the bottom-most row that is to be included in the
         combined row.
        :param int top_row_ind: Index in the Hilbert spectrum of the top-most row that is to be included in the
         combined row.
        :return: Combined row
        :rtype: numpy.ndarray
        """
        combined_row = self.hht.hilbert_spectrum[bottom_row_ind]
        if bottom_row_ind == top_row_ind:
            return combined_row

        for i in range(1, top_row_ind - bottom_row_ind + 1):
            combined_row = np.maximum(combined_row, self.hht.hilbert_spectrum[bottom_row_ind + i])
        return combined_row


def remove_short_consecutive_sequences(non_zero_indices, min_consecutive_length):
    """
    Removes consecutive sequences of integers from non_zero_indices parameter if they are shorter than the specified
    minimum consecutive length.

    :param numpy.ndarray non_zero_indices: Contains indices of a signal's non-zero values.
    :param int min_consecutive_length: The length a consecutive sequence of indices must exceed to not be removed from
        the returned version of non_zero_indices.

    :return: Updated version of non_zero_indices with the short consecutive sequences removed.
    :rtype: numpy.ndarray
    """
    if len(non_zero_indices) < 2:
        # No consecutive sequences to remove if there are fewer than 2 elements
        return non_zero_indices

    # Initialize variables
    current_sequence = [non_zero_indices[0]]
    prev_index = non_zero_indices[0]
    updated_indices = []

    # Iterate through the sorted indices
    for index in non_zero_indices[1:]:
        # Check if the current index is consecutive to the previous index
        if index == prev_index + 1:
            current_sequence.append(index)
        else:
            # Remove indices from the current sequence if it's shorter than the minimum length
            if len(current_sequence) >= min_consecutive_length:
                updated_indices.extend(current_sequence)
            # Start a new sequence
            current_sequence = [index]

        # Update the previous index
        prev_index = index

    # Check the last sequence
    if len(current_sequence) >= min_consecutive_length:
        updated_indices.extend(current_sequence)

    return np.array(updated_indices)


def exponential_decay_model(t, A, k):
    """
    Model for exponential decay curve used for curve fitting amplitude curve to.

    :param numpy.ndarray t: Time-points
    :param float | int A: Initial amplitude of curve
    :param float | int k: Decay rate of curve
    :return: Exponential decay curve
    :rtype: numpy.ndarray
    """
    return A * np.exp(-k * t)

