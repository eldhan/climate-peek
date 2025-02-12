import pandas as pd
import requests
from urllib import error
import os
import re
from datetime import datetime
import streamlit as st


def fetch_dataset(
    dataset_name: str,
    version: str = "1",
    csvType: str = "full",
    useColumnShortNames: str = "false",
):
    """
    Fetch a CSV dataset from Our World in Data.

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
        (default = long column).

    Returns:
    ----------
    df : DataFrame
        a pandas.DataFrame of the CSV data.
    """
    storage_options = {"User-Agent": "Our World In Data data fetch/1.0"}
    # Fetch the data.
    try:
        df = pd.read_csv(
            f"https://ourworldindata.org/grapher/{dataset_name}.csv?v={version}&csvType={csvType}&useColumnShortNames={useColumnShortNames}",
            storage_options=storage_options,
        )
    except error.URLError:
        return "error"
    else:
        return df


def fetch_dataset_metadata(
    dataset_name: str,
    version: str = "1",
    csvType: str = "full",
    useColumnShortNames: str = "false",
):
    """
    Fetch the metadata of a CSV dataset from Our World in Data.

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
        (default = long column).

    Returns:
    ----------
    metadata : json
        json of the metadata information pertaining to the CSV data.
    """
    # Fetch the metadata
    try:
        metadata = requests.get(
            f"https://ourworldindata.org/grapher/{dataset_name}.metadata.json?v={version}&csvType={csvType}&useColumnShortNames={useColumnShortNames}"
        )
        if metadata.status_code == 200:
            metadata_json = metadata.json()
        else:
            raise requests.exceptions.ConnectionError("error")
    except requests.exceptions.ConnectionError:
        return "error"
    else:
        return metadata_json


def update_dataset(dataset_name: str, filename: str) -> bool:
    """
    Check if there is a new version of a dataset and import it.

    Parameters:
    ----------
    dataset_name : str
        the name of the dataset to fetch.
    filename :
        the name of the log file

    Returns:
    ----------
    : bool
        True if succes or False if error encountered
    """
    # Create log list
    log = []
    log.append(
        f"Starting update for {dataset_name} at {datetime.today().strftime("%Y-%m-%d-%H-%M")} \n"
    )
    # Get the date of the dataset last update
    metadata = fetch_dataset_metadata(dataset_name)
    log.append(
        f"1. Fetch metadata : {metadata if metadata is "error" else "success"}\n"
    )
    column_name = list(metadata["columns"].keys())[0]
    if metadata != "error":
        if "lastUpdated" in metadata["columns"][column_name]:
            last_updated = metadata["columns"][column_name]["lastUpdated"]
        else:
            last_updated = metadata["dateDownloaded"]
        log.append(f"2. Date of last WID update: {last_updated}\n")
        # Parse the datasets folder
        datasets_list = os.scandir("datasets")
        today = datetime.today().strftime("%Y-%m-%d")
        dataset_exists = False
        for dataset in datasets_list:
            # Check if we already have an existing dataset and get its update date
            if dataset_name in dataset.name:
                dataset_exists = True
                log.append(f"3. Found existing dataset : {dataset.name}\n")
                dataset_update_date = re.search(r"\d{4}-\d{2}-\d{2}", dataset.name)
                if isinstance(dataset_update_date, re.Match):
                    dataset_update_date = dataset_update_date[0]
                else:
                    dataset_update_date = today
                log.append(
                    f"4a. Date the dataset was last updated : {dataset_update_date}\n"
                )
        # if the dataset does not exist:
        if dataset_exists is False:
            dataset_update_date = today
        # if the existing dataset is not the most recent, get the new one
        success = False
        if dataset_exists is True:
            if dataset_update_date > last_updated or (
                dataset_update_date == last_updated == today
            ):
                df = fetch_dataset(dataset_name)
                log.append(f"5. Fetch dataset : {df if df is "error" else "success"}\n")
                if df is not "error":
                    # Create a new CSV with the freshest data
                    dataset_new_name = f"{dataset_name}-{last_updated}"
                    log.append(
                        f"6. Create new file for updated dataset {dataset_new_name}\n"
                    )
                    df.to_csv(
                        path_or_buf=f"datasets/{dataset_new_name}.csv",
                        index=False,
                    )
                    for dataset in datasets_list:
                        if dataset_new_name in dataset.name:
                            log.append(
                                f"7. New dataset file successfully created {dataset.name}\n"
                            )
                    # Delete the old dataset if it exists
                    if os.path.exists(
                        f"datasets/{dataset_name}-{dataset_update_date}.csv"
                    ):
                        os.remove(f"datasets/{dataset_name}-{dataset_update_date}.csv")
                        log.append(
                            f"8. Deleted datasets/{dataset_name}-{dataset_update_date}.csv\n"
                        )
                    elif os.path.exists(f"datasets/{dataset_name}.csv"):
                        os.remove(f"datasets/{dataset_name}.csv")
                        log.append(f"9. Deleted datasets/{dataset_name}.csv\n")
                    success = True
        elif dataset_exists is False:
            df = fetch_dataset(dataset_name)
            log.append(f"5. Fetch dataset : {df if df is "error" else "success"}\n")
            if df is not "error":
                # Create a new CSV with the freshest data
                dataset_new_name = f"{dataset_name}-{last_updated}"
                log.append(f"6. Import new dataset {dataset_new_name}\n")
                df.to_csv(
                    path_or_buf=f"datasets/{dataset_new_name}.csv",
                    index=False,
                )
                for dataset in datasets_list:
                    if dataset_new_name in dataset.name:
                        log.append(
                            f"7. New dataset file successfully created {dataset.name}\n"
                        )
                success = True
    logs = open(filename, "a")
    logs.write(str(log))
    logs.close()
    if success:
        return True
    else:
        return False


def is_dataset_uptodate():
    """
    Check if the datasets have already been updated today.

    Parameters:
    ----------
    none

    Returns:
    ----------
        True if dataset is up-to-date or today's date if not
    """
    today = datetime.today().strftime("%Y-%m-%d")
    if os.path.exists(f"datasets/{today}.txt"):
        return True
    else:
        return today


def check_datasets(datasets: list) -> None:
    """
    Perform all checks on datasets.

    Parameters:
    ----------
    datasets : list
        a list of datasets to check

    Returns:
    ----------
    None
    """
    # Check if datasets are up-to-date
    check_result = is_dataset_uptodate()
    if check_result is not True:
        # Delete previous check file
        for file in os.listdir("datasets"):
            if file.endswith(".txt"):
                os.remove(f"datasets/{file}")
        # update all datasets
        f = open(f"datasets/{check_result}.txt", "a")
        progress_text = "Les données sont en cours de chargement, veuillez patienter"
        progress = 0
        my_bar = st.progress(progress, text=progress_text)
        step = round(len(datasets) / 100, 2)
        for dataset in datasets:
            update_dataset(dataset, f.name)
            progress += step
            if progress > 1.0:
                progress = 1.0
            my_bar.progress(progress, text=progress_text)
        f.close()
        my_bar.empty()


def get_dataset(dataset_name: str) -> str:
    """
    Get the dataset path

    Parameters:
    ----------
    dataset name : str
        the name of the dataset

    Returns:
    ----------
    dataset_name : str
        the name of the dataset file or error
    """
    datasets_list = os.scandir("datasets")
    for dataset in datasets_list:
        # Get the dataset name
        if dataset_name in dataset.name:
            dataset_update_date = re.search(r"\d{4}-\d{2}-\d{2}", dataset.name)[0]
            dataset_name = f"{dataset_name}-{dataset_update_date}.csv"
            return dataset_name
    return "error"
