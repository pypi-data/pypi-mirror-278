#  Copyright (C) 2023-2024 Y Hsu <yh202109@gmail.com>
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
import pandas as pd

class summary_by_group:
    """
    A class for generating summary statistics and performing calculations on a DataFrame.

    Attributes:
        df (pandas.DataFrame): The input DataFrame.

    Methods:
        __init__(self, df): Initializes the summary_by_group class.
        generate_dataset(design=1): Generate an example dataset for clinical health.
        count_by_group(columns): Count occurrences of unique combinations of values in the DataFrame.
        count_to_cate(group_columns, target_column, bins, stats): Convert numerical data into categorical data based on specified bins and calculate statistics.
    """

    def __init__(self, df):
        """
        Initializes the summary_by_group class.

        Args:
            df (pandas.DataFrame): The input DataFrame.

        Raises:
            ValueError: If the input is not a DataFrame.
        """
        if df is None:
            df = self.generate_dataset()
        self.df = df

    @staticmethod
    def generate_dataset(design=1):
        """
        Generate an example dataset for clinical health.

        Args:
            design (int, optional): The type of dataset to generate. Defaults to 1.

        Returns:
            df (pandas.DataFrame): The generated example dataset.
        """
        df = pd.DataFrame()
        if design==1:
            for study in range(2): 
                for treatment in range(2): 
                    nsubj = 20
                    v0 = np.random.randint(1, 5, size=nsubj)
                    for subject in range(nsubj):
                        m0 = np.random.randint(2, 6, size=v0[subject])
                        for visit in range(v0[subject]):
                            if not df.empty:
                                df = pd.concat([df, pd.DataFrame({'study': [f"STD{study+1}"] * m0[visit],
                                                            'treatment': [f"TRT{treatment+1}"] * m0[visit],
                                                            'subject': [f"SUBJ{subject+1:02d}"] * m0[visit],
                                                            'visit': [f"VISIT{visit+1}"] * m0[visit],
                                                            'meal': range(1, m0[visit] + 1)})], axis=0, ignore_index=True)
                            else: 
                                df = pd.DataFrame({'study': [f"STD{study+1}"] * m0[visit],
                                                            'treatment': [f"TRT{treatment+1}"] * m0[visit],
                                                            'subject': [f"SUBJ{subject+1:02d}"] * m0[visit],
                                                            'visit': [f"VISIT{visit+1}"] * m0[visit],
                                                            'meal': range(1, m0[visit] + 1)})
            df['calorie'] = np.random.randint(300, 2001, size=len(df))
        return df
    
    def count_by_group(self, columns):
        """
        Count occurrences of unique combinations of values in the DataFrame.

        Args:
            columns (list): The columns to group by.

        Returns:
            grouped_df (pandas.DataFrame): The grouped DataFrame with count.

        Raises:
            ValueError: If the input is not a DataFrame or columns is not a list or a column does not exist in the DataFrame.
        """
        if not isinstance(self.df, pd.DataFrame):
            raise ValueError("Input is not a DataFrame.")
        if not isinstance(columns, list):
            raise ValueError("columns should be a list.")
        for col in columns:
            if col not in self.df.columns:
                raise ValueError(f"Column '{col}' does not exist in the DataFrame.")
        grouped_df = self.df.groupby(columns, observed=False).size().reset_index(name='count')
        return grouped_df
    
    def count_to_cate(self, group_columns, target_column, bins, stats):
        """
        Convert numerical data into categorical data based on specified bins and calculate statistics.

        Args:
            group_columns (list): The columns to group by.
            target_column (str): The column to convert and calculate statistics on.
            bins (int or list or numpy.ndarray): The bin edges for converting the target_column.
            stats (list): The statistics to calculate.

        Returns:
            out1 (pandas.DataFrame): The resulting DataFrame with calculated statistics.

        Raises:
            ValueError: If the input is not a DataFrame or group_columns is not a list or contains non-string elements,
                        target_column is not a non-empty string or does not exist in the DataFrame,
                        target_column is not a numerical column, bins is not an integer or a sequence of bin edges,
                        or stats is not a list of strings or contains invalid statistics.
        """
        if not isinstance(self.df, pd.DataFrame):
            raise ValueError("Input is not a DataFrame.")
        if not isinstance(group_columns, list):
            raise ValueError("group_columns should be a list.")
        if not all(isinstance(col, str) for col in group_columns):
            raise ValueError("group_columns should contain only strings.")
        if not target_column or not isinstance(target_column, str):
            raise ValueError("target_column should be a non-empty string.")
        if target_column not in self.df.columns:
            raise ValueError(f"Column '{target_column}' does not exist in the DataFrame.")
        if not pd.api.types.is_numeric_dtype(self.df[target_column]):
            raise ValueError(f"Column '{target_column}' is not a numerical column.")
        if not isinstance(bins, (int, list, np.ndarray)):
            raise ValueError("bins should be an integer or a sequence of bin edges.")
        if isinstance(bins, int):
            bins = [bins]
        assert all(isinstance(stat, str) for stat in stats), "Input stats should be a list of strings."
        valid_stats = ['count', 'sum', 'total_max', 'total_min', 'total_sum', 'total_count']
        assert all(stat in valid_stats for stat in stats), f"Input stats should be within values {valid_stats}."

        nb = len(bins)
        out0 = pd.DataFrame()
        out1 = pd.DataFrame()
        for stat in stats:
            out0 = pd.DataFrame()
            if stat == 'count':
                out0 = self.df.groupby(group_columns, observed=False)[target_column].apply(lambda x: np.histogram(x, bins=bins)[0]).reset_index()
                out0_columns = [f"N({bins[i]}<=X<{bins[i+1]})" for i in range(nb - 2)]+[f"N({bins[nb-2]}<=V<={bins[nb-1]})"]
                out0[out0_columns] = pd.DataFrame(out0[target_column].tolist(), index=out0.index)
                out0.drop(columns=[target_column], inplace=True)
            elif stat == 'sum':
                out0 = self.df.groupby(group_columns, observed=False)[target_column].apply(lambda x: np.histogram(x, bins=bins, weights=x)[0]).reset_index()
                out0_columns = [f"Sum({bins[i]}<=X<{bins[i+1]})" for i in range(nb - 2)]+[f"Sum({bins[nb-2]}<=V<={bins[nb-1]})"]
                out0[out0_columns] = pd.DataFrame(out0[target_column].tolist(), index=out0.index)
                out0.drop(columns=[target_column], inplace=True)
            elif stat == 'total_max':
                out0 = self.df.groupby(group_columns, observed=False)[target_column].max().reset_index()
                out0.columns = group_columns + ['Max(all)']
            elif stat == 'total_min':
                out0 = self.df.groupby(group_columns, observed=False)[target_column].min().reset_index()
                out0.columns = group_columns + ['Min(all)']
            elif stat == 'total_sum':
                out0 = self.df.groupby(group_columns, observed=False)[target_column].sum().reset_index()
                out0.columns = group_columns + ['Sum(all)']
            elif stat == 'total_count':
                out0 = self.df.groupby(group_columns, observed=False)[target_column].count().reset_index()
                out0.columns = group_columns + ['N(all)']

            if not out0.empty:
                if not out1.empty:
                    out1 = out1.merge(out0, on=group_columns, how='outer')
                else:
                    out1 = out0

        return out1

if __name__ == "__main__":
    pass

