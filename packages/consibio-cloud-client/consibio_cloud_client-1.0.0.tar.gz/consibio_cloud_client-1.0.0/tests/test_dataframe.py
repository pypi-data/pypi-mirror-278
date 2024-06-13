from consibio_cloud_client.models import DataFrame, SingleValue
import pandas as pd

new_data = [
    {"element_id": "1", "value": 1, "timestamp": 1},
    {"element_id": "2", "value": 2, "timestamp": 2},
]


def test_dataframe_initialization():
    df = DataFrame()
    print(df.get_data())
    assert df.get_data() == []


def test_dataframe_add_many():
    df = DataFrame()
    df.add_many(new_data)
    print(df.get_raw())
    assert df.get_raw() == new_data


def test_dataframe_add():
    df = DataFrame()
    df.add(new_data[0])


def test_dataframe_instances_returned():
    df = DataFrame()
    df.add(new_data[0])
    assert isinstance(df, DataFrame)
    assert isinstance(df.get_data()[0], SingleValue)
    assert df.get_raw() == [new_data[0]]


def test_dataframe_pandas():
    """
    Test that a correct Pandas DataFrame is returned when calling `get_pandas()`:
    """
    df = DataFrame()
    df.add_many(new_data)
    assert df.get_pandas_df().equals(pd.DataFrame(new_data))
