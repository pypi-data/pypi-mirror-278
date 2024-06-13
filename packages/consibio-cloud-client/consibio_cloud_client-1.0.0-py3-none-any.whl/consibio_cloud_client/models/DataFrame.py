from ..utils.log import log
from .SingleValue import SingleValue

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np


class DataFrame:
    """
    A class representing a DataFrame for storing and manipulating data.

    Attributes:
        project_id (str): The ID of the project associated with the DataFrame.
        columns (list): The column names of the DataFrame.
        data (pandas.DataFrame): The data stored in the DataFrame.

    Methods:
        __init__(self, project_id=None): Initializes a new instance of the DataFrame class.
        add_many(self, points): Adds multiple data points to the DataFrame.
        add(self, point): Adds a single data point to the DataFrame.
        empty(self): Empties the DataFrame.
        remove_element(self, element_id): Removes all data points with a specific element ID from the DataFrame.
        remove_specific(self, element_id, timestamp): Removes a specific data point from the DataFrame.
        get_data(self): Returns all data points in the DataFrame as a list of SingleValue objects.
        get_raw(self): Returns the raw data in the DataFrame as a list of dictionaries.
        plot(self, title="Consibio Cloud Plot", decimation=None, num_horizontal_bins=100, project=None): Plots the data in the DataFrame.
        _decimated_values(self, df, num_horizontal_bins, n=5000): Decimates the data points in a DataFrame.
        _is_duplicate_timestamp(self, element_id, timestamp): Checks if a duplicate timestamp exists for a specific element ID in the DataFrame.
        _remove_timestamp(self, element_id, timestamp): Removes a duplicate timestamp for a specific element ID from the DataFrame.
    """

    def __init__(self, project_id=None):
        """
        Initializes a new instance of the DataFrame class.

        Args:
            project_id (str, optional): The ID of the project associated with the DataFrame. Defaults to None.
        """
        self.project_id = project_id
        self.columns = ["element_id", "value", "timestamp"]
        self.data = pd.DataFrame(columns=self.columns)

    def add_many(self, points):
        """
        Adds multiple data points to the DataFrame.

        Args:
            points (list): A list of dictionaries representing the data points to be added.

        Returns:
            DataFrame: The DataFrame object for method chaining.
        """
        # Remove any duplicate timestamps
        for point in points:
            element_id = point["element_id"]
            timestamp = point["timestamp"]
            if self._is_duplicate_timestamp(element_id, timestamp):
                log.warning(
                    f"Duplicate timestamp was found for element_id {element_id}: {timestamp} (overwriting existing data)")
                self._remove_timestamp(element_id, timestamp)
        if self.data.empty:
            self.data = pd.DataFrame(points, columns=self.columns)
        else:
            new_df = pd.DataFrame(points, columns=self.columns)
            self.data = pd.concat([self.data, new_df],
                                  ignore_index=True, sort=False)

        # Return the DataFrame for method chaining
        return self

    def add(self, point):
        """
        Adds a single data point to the DataFrame.

        Args:
            point (dict): A dictionary representing the data point to be added.

        Returns:
            DataFrame: The DataFrame object for method chaining.
        """
        self.add_many([point])

        # Return the DataFrame for method chaining
        return self

    def empty(self):
        """
        Empties the DataFrame.

        Returns:
            bool: True if the DataFrame was successfully emptied
        """
        self.data = pd.DataFrame(columns=self.columns)
        return True

    def remove_element(self, element_id):
        """
        Removes all data points with a specific element ID from the DataFrame.

        Args:
            element_id (str): The element ID to be removed.

        Returns:
            DataFrame: The DataFrame object for method chaining.
        """
        self.data = self.data[self.data["element_id"] != element_id]
        return self

    def remove_specific(self, element_id, timestamp):
        """
        Removes a specific data point from the DataFrame.

        Args:
            element_id (str): The element ID of the data point to be removed.
            timestamp (int): The timestamp of the data point to be removed.

        Returns:
            DataFrame: The DataFrame object for method chaining.
        """
        self.data = self.data[~((self.data["element_id"] == element_id) & (
            self.data["timestamp"] == timestamp))]
        return self

    def get_data(self):
        """
        Returns all data points in the DataFrame as a list of SingleValue objects.

        Returns:
            list: A list of SingleValue objects representing the data points.
        """
        records = self.get_raw()
        # Parse each record to SingleValue Class
        data = []
        for record in records:
            element_id = record["element_id"]
            single_value = SingleValue(
                element_id, record["value"], record["timestamp"])
            data.append(single_value)
        return data

    def get_raw(self):
        """
        Returns the raw data in the DataFrame as a list of dictionaries.

        Returns:
            list: A list of dictionaries representing the raw data.
        """
        return self.data.to_dict(orient="records")

    def get_pandas_df(self):
        """
        Returns the DataFrame.

        Returns:
            pandas.DataFrame: The DataFrame.
        """
        return self.data

    def plot(self, title="Consibio Cloud Plot", decimation=None, num_horizontal_bins=100, project=None):
        """
        Plots the data in the DataFrame.

        Args:
            title (str, optional): Title of the plot. Defaults to "Consibio Cloud Plot".
            decimation (int, optional): Number of data points to decimate. Defaults to None.
            num_horizontal_bins (int, optional): Number of horizontal bins for decimation. Defaults to 100.
            project (Project, optional): Project object containing elements. If provided, element color and name will be used in the plot. Defaults to None.

        Returns:
            None
        """
        # If use_metadata is True, we should get the metadata for the elements
        elements = None

        if project:
            # Check if elements are in the project
            elements = project.get_elements()

        # Get data
        data = self.get_data()
        # Create a plot
        fig, ax = plt.subplots()
        log.info(f"Plotting {len(data)} records")

        # Define colors and names for each element_id
        colors = {}
        names = {}

        # If elements are not None, we should get the metadata for the elements
        if elements:
            for element_id in set(record.get_element_id() for record in data):
                if element_id in elements:
                    element = elements[element_id]
                    colors[element_id] = element.get("color", "black")
                    names[element_id] = element.get("name", element_id)

        for element_id in set(record.get_element_id() for record in data):
            timestamps = []
            values = []
            for record in data:
                if record.get_element_id() == element_id:
                    timestamps.append(record.get_timestamp())
                    values.append(record.get_value())
            try:
                df = pd.DataFrame({'timestamp': pd.to_datetime(
                    timestamps, unit='s'), 'value': values})
                df.set_index('timestamp', inplace=True)
                if decimation or decimation is None:
                    df = self._decimated_values(df, num_horizontal_bins)
                    ax.plot_date(df.index, df['value'], '-', label=names.get(
                        element_id, element_id), color=colors.get(element_id, 'black'))
            except ValueError:
                pass
        ax.set(xlabel="timestamp", ylabel="value", title=title)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y %H:%M:%S'))
        ax.grid()
        plt.legend()
        plt.show()
        return None

    def _decimated_values(self, df, num_horizontal_bins, n=5000):
        """
        Decimates the data points in a DataFrame.

        Args:
            df (pandas.DataFrame): The DataFrame containing the data points.
            num_horizontal_bins (int): Number of horizontal bins for decimation.
            n (int, optional): Number of evenly spaced data points to keep after decimation. Defaults to 5000.

        Returns:
            pandas.DataFrame: The decimated DataFrame.
        """
        if len(df) > num_horizontal_bins:
            df = df.sort_index()
            bins = np.linspace(df.index.min().timestamp(),
                               df.index.max().timestamp(), num_horizontal_bins)
            df['bin'] = np.digitize(df.index, bins)
            min_df = df.groupby('bin')['value'].idxmin()
            max_df = df.groupby('bin')['value'].idxmax()
            first_df = df.groupby('bin').apply(lambda x: x.index[0])
            last_df = df.groupby('bin').apply(lambda x: x.index[-1])
            evenly_spaced_df = df.groupby('bin').apply(
                lambda x: x.iloc[np.linspace(0, len(x) - 1, n).astype(int)].index)
            df = df.loc[np.unique(np.concatenate(
                [min_df, max_df, first_df, last_df, np.concatenate(evenly_spaced_df.values)]))]
        return df

    def _is_duplicate_timestamp(self, element_id, timestamp):
        """
        Checks if a duplicate timestamp exists for a specific element ID in the DataFrame.

        Args:
            element_id (str): The element ID to check for duplicate timestamps.
            timestamp (int): The timestamp to check for duplicates.

        Returns:
            bool: True if a duplicate timestamp exists, False otherwise.
        """
        # Check df for duplicate timestamp for element_id
        return len(self.data[(self.data["element_id"] == element_id) & (self.data["timestamp"] == timestamp)]) > 0

    def _remove_timestamp(self, element_id, timestamp):
        """
        Removes a duplicate timestamp for a specific element ID from the DataFrame.

        Args:
            element_id (str): The element ID to remove the duplicate timestamp from.
            timestamp (int): The duplicate timestamp to be removed.

        Returns:
            None
        """
        # Remove duplicate timestamp for element_id
        self.data = self.data[~((self.data["element_id"] == element_id) & (
            self.data["timestamp"] == timestamp))]
