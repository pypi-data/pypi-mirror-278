class SingleValue:
    """
    Represents a single value with an element ID, value, and timestamp.
    """

    def __init__(self, element_id, value, timestamp):
        """
        Initializes a SingleValue object.

        Args:
            element_id (str): The ID of the element.
            value: The value associated with the element.
            timestamp: The timestamp of when the value was recorded.
        """
        self.element_id = element_id
        self.value = value
        self.timestamp = timestamp

    def __str__(self):
        """
        Returns a string representation of the SingleValue object.
        """
        return f"element_id: {self.element_id}, value: {self.value}, timestamp: {self.timestamp}"

    def __repr__(self):
        """
        Returns a string representation of the SingleValue object.
        """
        return f"element_id: {self.element_id}, value: {self.value}, timestamp: {self.timestamp}"

    def get_element_id(self):
        """
        Returns the ID of the element.
        """
        return self.element_id

    def get_value(self):
        """
        Returns the value associated with the element.
        """
        return self.value

    def get_timestamp(self):
        """
        Returns the timestamp of when the value was recorded.
        """
        return self.timestamp

    def get_raw(self):
        """
        Returns a dictionary representation of the SingleValue object.
        """
        return {
            "element_id": self.element_id,
            "value": self.value,
            "timestamp": self.timestamp
        }
