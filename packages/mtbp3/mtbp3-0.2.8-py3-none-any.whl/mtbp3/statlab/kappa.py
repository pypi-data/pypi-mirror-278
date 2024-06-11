#  Copyright (C) 2023 Y Hsu <yh202109@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public license as published by
#  the Free software Foundation, either version 3 of the License, or
#  any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details
#
#  You should have received a copy of the GNU General Public license
#  along with this program. If not, see <https://www.gnu.org/license/>

import numpy as np
from sklearn.utils import resample

class KappaCalculator:
    def __init__(self, y):
        assert isinstance(y, list) and len(y) >= 2, "y must be a list with at least 2 elements"
        assert all(isinstance(x, list) for x in y), "all elements of y must be lists"
        assert all(len(x) == len(y[0]) for x in y), "all elements of y must have equal lengths"

        self.y = y
        self.y_length = len(y)
        
        if self.y_length == 2:
            self.cohen_kappa = self.__calculate_cohen_kappa(y[0], y[1])
        else:
            self.cohen_kappa = np.nan

    @staticmethod
    def __calculate_cohen_kappa(y1, y2):
        total_pairs = len(y1)
        observed_agreement = sum(1 for i in range(total_pairs) if y1[i] == y2[i]) / total_pairs
        unique_labels = set(y1 + y2)
        expected_agreement = sum((y1.count(label) / total_pairs) * (y2.count(label) / total_pairs) for label in unique_labels)
        return (observed_agreement - expected_agreement) / (1 - expected_agreement)

    def bootstrap_cohen_ci(self, n_iterations=1000, confidence_level=0.95, outfmt='string', out_digits=3):
        assert isinstance(n_iterations, int) and n_iterations > 1, "n_iterations must be an integer greater than 1"
        assert isinstance(confidence_level, (float)) and 0 < confidence_level < 1, "confidence_level must be a number between 0 and 1"
        if self.y_length != 2:
            return []

        y1 = self.y[0]
        y2 = self.y[1]
        kappa_values = []
        for _ in range(n_iterations):
            r1_resampled = resample(y1)
            r2_resampled = resample(y2)

            kappa = self.__calculate_cohen_kappa(r1_resampled, r2_resampled)
            kappa_values.append(kappa)
        # Calculate confidence interval
        lower_percentile = (1 - confidence_level) / 2
        upper_percentile = 1 - lower_percentile
        lower_bound = np.percentile(kappa_values, lower_percentile * 100)
        upper_bound = np.percentile(kappa_values, upper_percentile * 100)
        if outfmt=='string':
            return "Cohen's kappa: {:.{}f}".format(self.cohen_kappa, out_digits) + "\nConfidence Interval ({}%): [{:.{}f}, {:.{}f}]".format(confidence_level * 100, lower_bound, out_digits, upper_bound, out_digits)
        else:
            return [self.cohen_kappa, n_iterations, confidence_level, lower_bound, upper_bound]

if __name__ == "__main__":
    y1 = ['B'] * 70 + ['A'] * 30
    y2 = ['A'] * 70 + ['B'] * 30
    calculator = KappaCalculator([y1, y2])
    print(calculator.bootstrap_cohen_ci(n_iterations=1000, confidence_level=0.95, out_digits=6))
