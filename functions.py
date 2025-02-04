import pandas as pd
import requests
from sklearn import preprocessing


def load_dataset(
    dataset_name: str,
    version: str = "1",
    csvType: str = "full",
    useColumnShortNames: str = "true",
) -> tuple:
    """
    Load a CSV dataset from Our World in Data.

    Parameters:
    ----------
    dataset_name : str
        the name of the dataset to fetch.
    version : str
        optional - the version of the dataset.
    csvType : str
        optional - download the full data including entities and time points or
        only the currently selected data visible in the chart on the website
        (default = full).
    useColumnShortNames : str
        optional - long column names or shortened column names
        (default = shortened).

    Returns:
    ----------
    df : DataFrame
        a pandas.DataFrame of the CSV data.
    metadata : json
        json of the metadata information pertaining to the CSV data.
    """
    storage_options = {"User-Agent": "Our World In Data data fetch/1.0"}
    # Fetch the data.
    df = pd.read_csv(
        f"https://ourworldindata.org/grapher/{dataset_name}.csv?v={version}&csvType={csvType}&useColumnShortNames={useColumnShortNames}",
        storage_options=storage_options,
    )

    # Fetch the metadata
    metadata = requests.get(
        f"https://ourworldindata.org/grapher/{dataset_name}.metadata.json?v={version}&csvType={csvType}&useColumnShortNames={useColumnShortNames}"
    ).json()
    return df, metadata


def normalize_data(
    dataframe,
    columns_to_normalize: list,
):
    """
    Normalize the data of the columns specified.

    Parameters:
    ----------
    dataframe : DataFrame
        the dataframe containing the data.
    columns_to_normalize : list
        a list of string with the names of the DataFrame columns to normalize.

    Returns:
    ----------
    df : DataFrame
        a pandas.DataFrame with the data of the columns specified normalized.
    """
    # Create the Scaler object
    scaler = preprocessing.StandardScaler()
    # Fit your data on the scaler object
    scaled_data = scaler.fit_transform(dataframe[columns_to_normalize])
    scaled_df = pd.DataFrame(scaled_data, columns=columns_to_normalize)
    df = dataframe.drop(columns=columns_to_normalize)
    df = pd.merge(df, scaled_df, how="inner", left_index=True, right_index=True)
    return df
