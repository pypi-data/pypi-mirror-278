from .client import Client
from .utils.log import log
from .models.DataFrame import DataFrame

##############################################
# Project
##############################################


class Project:
    def __init__(self, project_id):
        """
        Initialize a Project object.

        Parameters:
        - project_id (str): The ID of the project.

        Returns:
        - None
        """
        self.project_id = project_id
        self.client = Client()
        self.devices = None
        self.elements = None

    def get_datalog(self, elements, from_time, to_time):
        """
        Get datalog for a list of elements within a specified time range.

        Parameters:
        - elements (list): A list of element IDs.
        - from_time (int): The start time of the time range in UNIX timestamp format.
        - to_time (int): The end time of the time range in UNIX timestamp format.

        Returns:
        - DataFrame: A DataFrame object containing the datalog.
        - None: If there was an error retrieving the datalog.
        """
        # Validate that the element_ids is a list
        if not isinstance(elements, list):
            log.error("Elements must be a list of element ids.")
            return None

        # Validate that the from_time and to_time are integers
        # Try and parse the from_time and to_time, we expect a datetime object
        try:
            from_time = int(from_time)
            to_time = int(to_time)
        except Exception as e:
            log.error("From time and to time must be integers.", e)
            return None

        if not isinstance(from_time, int) or not isinstance(to_time, int):
            log.error("From time and to time must be integers.")
            return None

        # Validate that the to_time is greater than from_time
        if to_time <= from_time:
            log.error("To time must be greater than from time.")
            return None

        # Validate that period is not more than 180 days
        if from_time - to_time > 180 * 24 * 60 * 60:
            log.error("The period cannot be more than 180 days.")
            return None

        log.info(
            f"Getting datalog for {len(elements)} element(s) from {from_time} to {to_time}")

        # Time in UNIX timestamp format
        from_time = int(from_time)
        to_time = int(to_time)

        # Elements to semi-colon separated string
        elements = ";".join(elements)

        # URL with "from_time", "to_time", and "element_ids"
        url = f"{self.client.get_api_url()}/projects/{self.project_id}/datalog?from_time={from_time}&to_time={to_time}&elements={elements}"

        # Get data
        response = self.client.http_get(url)

        if response is None:
            log.error("Error occurred while getting datalog.")
            return None

        # Payload in response, is a JSON Object, Upper map with Element ID, and here we have a list [] of data points {t, v}

        # Make a new DataFrame
        data_frame = DataFrame(self.project_id)

        # Loop through the response payload
        prepared_points = []
        for element_id, points in response["payload"].items():
            for point in points:
                prepared_points.append({
                    "element_id": element_id,
                    "timestamp": point["t"],
                    "value": point["v"]
                })

        # Add points to the DataFrame
        data_frame.add_many(prepared_points)

        return data_frame

    def get_devices(self):
        """
        Get the devices associated with the project.

        Returns:
        - list: A list of devices.
        - None: If there was an error retrieving the devices.
        """
        if self.devices is None:
            url = f"{self.client.get_api_url()}/projects/{self.project_id}/devices"
            response = self.client.http_get(url)

            if response is None:
                log.error("Error occurred while getting devices.")
                return None

            self.devices = response["payload"]

        return self.devices

    def get_elements(self):
        """
        Get the elements associated with the project.

        Returns:
        - list: A list of elements.
        - None: If there was an error retrieving the elements.
        """
        if self.elements is None:
            url = f"{self.client.get_api_url()}/projects/{self.project_id}/elements"
            response = self.client.http_get(url)

            if response is None:
                log.error("Error occurred while getting elements.")
                return None

            self.elements = response["payload"]

        return self.elements
