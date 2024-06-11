import os
import psycopg2
import pandas as pd
from psycopg2 import extras
import json
from pandas.core.common import flatten

class DataQuality(object):
    def __init__(self, df,flow,config_path):
        """
        Initializes the DataQuality object with a DataFrame, a flow identifier, and a path to a configuration file.

        Args:
            df (pd.DataFrame): The DataFrame to assess for quality.
            flow (str): An identifier used to select the appropriate section of the configuration.
            config_path (str): The filesystem path to a JSON configuration file.
        """
        self.df = df
        self.flow = flow
        self.config_path = config_path
        self.config = self.load_config()

    
    def load_config(self):
        """
        Loads configuration settings from a JSON file based on the provided flow.

        Returns:
            dict: A dictionary containing the configuration settings specific to the flow or an empty dict if an error occurs.
        """
        try:
            with open(self.config_path, 'r') as file:
                config = json.load(file)
                return config.get(self.flow, {})  # Return only the part of the config relevant to the current flow
        except FileNotFoundError:
            print(f"No configuration file found at {self.config_path}")
        except json.JSONDecodeError:
            print("Error decoding JSON from the configuration file")
        except Exception as e:
            print(f"An error occurred: {e}")
        return {}  #

    def quality_metrics(self):
        """
        Validates the data according to the loaded configuration and returns a report of quality metrics and any failing rows.

        Returns:
            tuple: A tuple containing a dictionary of results by column and a dictionary of DataFrames of failing rows for each check.
        """
        results = {}
        failing_rows = {}

        if not self.config:
            print("No configuration loaded, cannot perform assessment of data quality metrics")
            return results, failing_rows
        
        if self.df.empty:
            print("df is empty, cannot perform assessment of data quality metrics")
            return results, failing_rows

        for column in self.config.get('data_quality', []):
            column_name = column['name']
            column_results = {}

            column_results['lenght'] =  len(self.df[column_name])

            # Completeness Checks
            for completeness_check in column.get('completeness', []):
                if completeness_check.get('required', False):
                    score, incompletes = self.check_completeness(self.df,column_name,completeness_check.get('authorized_na', 0))
                    column_results['completeness'] = score
                    if int(score) != 100:
                        failing_rows[f"{column_name}_completeness_fail"] = incompletes

            # Accuracy Checks
            for accuracy_check in column.get('accuracy', []):
                if accuracy_check.get('required', False):
                    range_val = accuracy_check.get('range')
                    score, out_of_range = self.check_accuracy(self.df,column_name, range_val)
                    column_results['accuracy'] = score
                    if int(score) != 100:
                        failing_rows[f"{column_name}_accuracy_range_fail"] = out_of_range

            # Uniqueness Checks
            for uniqueness_check in column.get('uniqueness', []):
                if uniqueness_check.get('required', False):
                    unique_columns = uniqueness_check.get('unique_columns')
                    score, duplicates = self.check_uniqueness(self.df,unique_columns)
                    column_results['uniqueness'] = score
                    if int(score) != 100:
                        failing_rows[f"{column_name}_uniqueness_fail"] = duplicates

            # Consistency Checks
            for consistency_check in column.get('consistency', []):
                if consistency_check.get('required', False):

                    if consistency_check['type'] == 'z_score':
                        outlier_threshold = consistency_check.get('outlier_threshold')
                        score, outliers = self.detect_outliers_z_score(self.df,column_name, outlier_threshold)
                        if int(score) != 100:
                            failing_rows[f"{column_name}_consistency_z_score_fail"] = outliers

                    if consistency_check['type'] == 'moving_std':
                        score, outliers = self.detect_outliers_moving_std(self.df,
                            column_name,
                            consistency_check['window']
                        )
                        if int(score) != 100:
                            failing_rows[f"{column_name}_consistency_moving_std_fail"] = outliers
                    column_results['consistency'] = score

            # Timeliness Checks
            for timeliness_check in column.get('timeliness', []):
                if timeliness_check.get('required', False):
                    if timeliness_check['type'] == 'gap_between_entries':
                        score, gaps = self.check_gap_between_entries(self.df,
                            timeliness_check['start_time_column'], 
                            timeliness_check['end_time_column']
                        )
                        if int(score) != 100:
                            failing_rows[f"{column_name}_timeliness_gap_between_entries_issues"] = gaps
                    elif timeliness_check['type'] == 'regular_intervals':
                        score, gaps = self.check_regular_intervals(self.df,
                            timeliness_check['time_column'], 
                        )
                        if int(score) != 100:
                            failing_rows[f"{column_name}_timeliness_regular_intervals_issues"] = gaps
                    column_results['timeliness'] = score

            results[column_name] = column_results

        return results, failing_rows
    

################# COMPLETENESS #################

    @staticmethod
    def check_completeness(df, column,authorized_na):
        """
        Checks for missing values in a specified column of a DataFrame and returns the percentage of complete entries along with any incomplete rows.

        Args:
            df (pd.DataFrame): The DataFrame to analyze.
            column (str): The column name to check for missing values.

        Returns:
            tuple: A tuple containing the completeness percentage and either None or a DataFrame of rows with missing values.

        Example:
            >>> df = pd.DataFrame({'data': [1, 2, None, 4]})
            >>> check_completeness(df, 'data')
            (75.0,   data
            2   NaN)  # Indicates one entry is missing in the 'data' column
        """

        total_entries = len(df[column]) - authorized_na
        non_missing_count = df[column].notna().sum()
        completeness_percentage = (non_missing_count / total_entries) * 100
        incomplete_rows = df[df[column].isna()]
        
        if not incomplete_rows.empty:
            return completeness_percentage, incomplete_rows
        return completeness_percentage, None


################# ACCURACY #################

    @staticmethod
    def check_accuracy(df, column, range_val):
        """
        Checks if the non-NA values in a specified column fall within a defined range, returning the accuracy percentage and any rows that fail this check.

        Args:
            df (pd.DataFrame): The DataFrame to analyze.
            column (str): The column name to check for value accuracy.
            range_val (tuple): A tuple of two values (min, max) defining the acceptable range.

        Returns:
            tuple: A tuple containing the accuracy percentage and either None or a DataFrame of rows outside the range.

        Example:
            >>> df = pd.DataFrame({'data': [1, 2, 3, 10, 20]})
            >>> check_accuracy(df, 'data', (1, 10))
            (80.0,    data
            4     20)  # Indicates the value 20 is outside the specified range (1, 10)
        """
        if range_val:
            # Filter out NaN values from the column before creating the boolean mask
            notna_data = df[column].notna()
            # Use this clean data to create a mask where True indicates values outside the desired range
            mask = ~df[column].between(range_val[0], range_val[1]) & notna_data
            # Use the mask to select rows from the original DataFrame that are outside the range
            outside_range = df[mask]

            total_entries = len(notna_data)
            inaccurate_count = len(outside_range)
            accurate_percentage = ((total_entries - inaccurate_count) / total_entries) * 100

            if not outside_range.empty:
                return accurate_percentage, outside_range
        return accurate_percentage, None

    @staticmethod
    def check_uniqueness(df, columns):
        """
        Checks if the entries in specified columns are unique, returning the percentage of unique entries and any duplicated rows.

        Args:
            df (pd.DataFrame): The DataFrame to analyze.
            columns (list of str or str): The column(s) to check for uniqueness.

        Returns:
            tuple: A tuple containing the uniqueness percentage and either None or a DataFrame of duplicated rows.

        Example:
            >>> df = pd.DataFrame({'id': [1, 1, 2, 3]})
            >>> check_uniqueness(df, 'id')
            (75.0,   id
            0    1
            1    1)  # Indicates entries with the id 1 are duplicated
        """
        total_entries = len(df[columns].notna())
        duplicated_rows = df[df.duplicated(subset=columns, keep=False)]
        duplicated_rows_count = len(duplicated_rows)
        uniqueness_percentage = ((total_entries - duplicated_rows_count) / total_entries) * 100
        if not duplicated_rows.empty:
            return uniqueness_percentage, duplicated_rows
        return uniqueness_percentage, None
    
################# TIMELINESS #################

    @staticmethod
    def check_gap_between_entries(df, start_time_column, end_time_column):
        """
        Checks for gaps between the end time of one entry and the start time of the next entry across the dataset.

        Args:
            df (pd.DataFrame): The DataFrame to analyze.
            start_time_column (str): The name of the column containing start times.
            end_time_column (str): The name of the column containing end times.

        Returns:
            tuple: A tuple containing the percentage of entries without gaps and either None or a DataFrame of rows where gaps occur.

        Example:
            >>> df = pd.DataFrame({
            >>>     'start_time': pd.to_datetime(['2021-01-01 08:00', '2021-01-01 09:00']),
            >>>     'end_time': pd.to_datetime(['2021-01-01 08:30', '2021-01-01 09:30'])
            >>> })
            >>> check_gap_between_entries(df, 'start_time', 'end_time')
            (100.0, None)  # Indicates no gaps between entries
        """
        # Convert columns to datetime
        df.loc[:, start_time_column] = pd.to_datetime(df[start_time_column])
        df.loc[:, end_time_column] = pd.to_datetime(df[end_time_column])

        # Ensure the DataFrame is sorted by start_time
        sorted_df = df.sort_values(by=start_time_column)
        
        # Shift the end_time column up to compare with the next row's start_time
        sorted_df['next_start'] = sorted_df[start_time_column].shift(-1)
        
        # Find rows where the end_time does not seamlessly lead into the next start_time
        gaps = sorted_df[sorted_df[end_time_column] < sorted_df['next_start']]

        total_entries = len(df[start_time_column])
        gap_rows_count = len(gaps)
        gap_percentage = ((total_entries - gap_rows_count) / total_entries) * 100

        if not gaps.empty:
            return gap_percentage, gaps
        return gap_percentage, None
    
    @staticmethod
    def check_regular_intervals(df, time_column):
        """
        Checks for regularity of time intervals between consecutive timestamps in a DataFrame.

        Args:
            df (pd.DataFrame): The DataFrame containing the time data.
            time_column (str): The column with datetime entries to check for regular intervals.

        Returns:
            tuple: A tuple containing the percentage of time covered by the most common interval and either None or a DataFrame of inconsistencies.

        Example:
            >>> df = pd.DataFrame({
            >>>     'time': pd.to_datetime(['2021-01-01 00:00', '2021-01-01 00:05', '2021-01-01 00:10', '2021-01-01 00:20'])
            >>> })
            >>> check_regular_intervals(df, 'time')
            (75.0,   time                   time_diff
            3 2021-01-01 00:20:00     600.0)  # Indicates inconsistency in the interval at the last entry
        """
        # Ensure the column is in datetime format
        df.loc[:, time_column] = pd.to_datetime(df[time_column])

        # Sort the DataFrame based on the time column
        sorted_df = df.sort_values(by=time_column)

        # Calculate the time differences between consecutive entries and convert to seconds
        sorted_df['time_diff'] = sorted_df[time_column].diff().dt.total_seconds()

        valid_diffs = sorted_df['time_diff'].dropna()

        # Calculate the total time span in seconds
        total_time_span = (sorted_df[time_column].iloc[-1] - sorted_df[time_column].iloc[0]).total_seconds()

        # Find the most common time difference, which we consider as the expected interval
        if not valid_diffs.mode().empty:
            mode_diff = valid_diffs.mode()[0]
            
            # Check for deviations from this mode, excluding the first entry
            inconsistencies = sorted_df[(sorted_df['time_diff'] != mode_diff) & sorted_df['time_diff'].notna()]

            # Calculate covered time using entries that match the most common interval
            consistent = sorted_df[(sorted_df['time_diff'] == mode_diff) & sorted_df['time_diff'].notna()]
            time_covered = len(consistent) * mode_diff  # Total time covered by consistent intervals

            covered_time_percentage = (time_covered / total_time_span) * 100

            if not inconsistencies.empty:
                return covered_time_percentage, inconsistencies
            return covered_time_percentage, None
        else:
            return False, "No mode found for intervals; insufficient data or too many unique intervals."



################# CONSISTENCY #################

    @staticmethod
    def check_categorical_consistency(df, column, categories):
        """
        Checks if all values in a specified column of a DataFrame are within the allowed categories.

        Args:
            df (pd.DataFrame): The DataFrame to check.
            column (str): The name of the column to check for categorical consistency.
            categories (list): A list of allowed categories.

        Returns:
            tuple: A tuple containing a boolean indicating if the check passes, and either None or a DataFrame of invalid rows.

        Example:
            >>> df = pd.DataFrame({'category': ['apple', 'banana', 'cherry', 'durian']})
            >>> categories = ['apple', 'banana', 'cherry']
            >>> check_categorical_consistency(df, 'category', categories)
            (False,   category
                    3    durian)
        """
        invalid_rows = df[~df[column].isin(categories)]
        if not invalid_rows.empty:
            return False, invalid_rows
        return True, None
    

    @staticmethod
    def detect_outliers_z_score(df, column, threshold):
        """
        Detects outliers in a DataFrame column based on Z-score, assuming a normal distribution.

        Args:
            df (pd.DataFrame): The DataFrame containing the data.
            column (str): The name of the column to check for outliers.
            threshold (float): The Z-score value above which a data point is considered an outlier.

        Returns:
            tuple: A tuple containing the percentage of non-outlier entries and either None or a DataFrame of outliers.

        Example:
            >>> df = pd.DataFrame({'data': [10, 12, 12, 12, 500]})
            >>> detect_outliers_z_score(df, 'data', 2)
            (80.0,    data
            4    500)
        """
        # Example threshold for Z-score
        mean_val = df[column].mean()
        std_dev = df[column].std()
        z_scores = (df[column] - mean_val) / std_dev
        outliers = df[z_scores.abs() > threshold]

        total_entries = len(df[column])
        outliers_rows_count = len(outliers)
        outliers_percentage = ((total_entries - outliers_rows_count) / total_entries) * 100


        if not outliers.empty:
            return outliers_percentage, outliers
        return outliers_percentage, None
    
    @staticmethod
    def detect_outliers_moving_std(df, column, window=50):  # window size depends on the frequency of data points
        """
        Detects outliers in a DataFrame column based on a moving standard deviation.

        Args:
            df (pd.DataFrame): The DataFrame containing the data.
            column (str): The name of the column to check for outliers.
            window (int): The number of observations used for calculating the rolling mean and standard deviation.

        Returns:
            tuple: A tuple containing the percentage of non-outlier entries and either None or a DataFrame of outliers.

        Example:
            >>> df = pd.DataFrame({'data': [10, 20, 30, 40, 100, 60, 70, 80, 90, 1000]})
            >>> detect_outliers_moving_std(df, 'data', 3)
            (90.0,    data
            9   1000)
        """
        rolling_mean = df[column].rolling(window=window).mean()
        rolling_std = df[column].rolling(window=window).std()
        upper_bound = rolling_mean + (3 * rolling_std)
        lower_bound = rolling_mean - (3 * rolling_std)
        outliers = df[(df[column] > upper_bound) | (df[column] < lower_bound)]

        total_entries = len(df[column])
        outliers_rows_count = len(outliers)
        outliers_percentage = ((total_entries - outliers_rows_count) / total_entries) * 100

        if not outliers.empty:
            return outliers_percentage, outliers
        return outliers_percentage, None



######## MDM DQ

def find_missing(df, timedim, coldims, missingdim, granularity):
    """
    Identifies missing entries in a DataFrame based on specified time and column dimensions.

    Args:
        df (pd.DataFrame): The DataFrame to check for missing entries.
        timedim (str): The name of the column in `df` that represents time.
        coldims (list of str): The list of columns to check for combinations of missing entries.
        missingdim (str): The column to check for missing values.
        granularity (int): The granularity in minutes for generating the time range.

    Returns:
        pd.DataFrame: A DataFrame containing the rows where `missingdim` is null for each 
                      combination of `coldims` and time steps defined by `granularity`.

    Example:
        >>> df = pd.DataFrame({
        >>>     'time': pd.to_datetime(['2021-01-01 00:00', '2021-01-01 00:30']),
        >>>     'category': ['A', 'B'],
        >>>     'value': [10, None]
        >>> })
        >>> find_missing(df, 'time', ['category'], 'value', 30)
        Returns DataFrame with missing entries identified based on 'time', 'category', and 'value'.
    """
        
    time_array = pd.date_range(df[timedim].min(), df[timedim].max(), freq=f"{granularity}T")
    nC = 1
    for col in coldims:
        nC *= len(df[col].unique())

    df_ref = pd.DataFrame({timedim: list(flatten([[t] * nC for t in time_array]))})

    for col in coldims:
        col_values = df[col].unique()
        df_ref[col] = sorted(list(flatten([[v] * int(nC / len(col_values) * len(time_array)) for v in col_values])))

    join_df = pd.merge(df_ref, df, how='left', left_on=coldims + [timedim], right_on=coldims + [timedim])

    return join_df[join_df[missingdim].isnull()]



def add(a, b):
    """
    Adds two numbers together.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The sum of the two numbers.
    """
    return a + b