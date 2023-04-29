#!/usr/bin python3
import os
import requests
import toml
import pandas as pd
from collections import ChainMap
from dotenv import load_dotenv
import boto3
import sys
from typing import Dict


def read_api(url: str) -> Dict:
    """
    This function sends a GET request to the specified URL and returns the JSON data.

    Args:
        url (str): The URL to send the GET request to.

    Returns:
        dict: The JSON data returned from the API.

    Raises:
        requests.exceptions.RequestException: If an error occurs while sending the GET request or processing the response.
    """
    try:
        response = requests.get(url)
        response.raise_for_status() # catch error HTTP response 
        return response.json()
    except requests.exceptions.RequestException as err:
        print(
            f"[ERROR: ] occurred reading the API with status code: {err.response.status_code}", 
            file=sys.stderr
        )
        raise


def transform_data(data: Dict) -> pd.DataFrame:
    """
    This function transforms the raw data from the API into a formatted DataFrame.

    Args:
        data (Dict): The raw data returned from the API as a dictionary.

    Returns:
        pd.DataFrame: A formatted DataFrame containing the extracted data.

    Raises:
        Exception: If an error occurs while transforming the data.
    """
    try:
        company_list = [result['company']['name'] for result in data['results']]
        location_list = [result['locations'][0]['name'] for result in data['results']]
        job_list = [result['name'] for result in data['results']]
        job_type_list = [result['type'] for result in data['results']]
        publication_date_list = [result['publication_date'] for result in data['results']]

        data = dict(ChainMap(
            {'company': company_list},
            {'locations': location_list},
            {'job': job_list},
            {'job_type': job_type_list},
            {'publication_date': publication_date_list}
        ))

        df = pd.DataFrame.from_dict(data)
        df['publication_date'] = df['publication_date'].str[:10]
        df[['city', 'country']] = df['locations'].str.split(',', expand=True)
        df.drop('locations', axis=1, inplace=True)

        return df
    
    except Exception as err:
        print(f"[ERROR: ] building the dataframe: {err}", file=sys.stderr)
        raise

def save_to_csv(df: pd.DataFrame, file_name: str) -> None:
    """
    This function saves a Pandas DataFrame to a CSV file.

    Args:
        df (pd.DataFrame): A Pandas DataFrame to save to CSV.
        file_name (str): A string indicating the name of the CSV file.

    Returns:
        None if the file was saved successfully.

    Raises:
        Exception: If an error occurs while saving the DataFrame to CSV file.
    """
    try:
        df.to_csv(file_name, index=False)
    except Exception as err:
        print(f"[ERROR: ] saving dataframe to CSV: {err}", file=sys.stderr)
        raise


def upload_to_s3(file_name: str, bucket: str, folder: str, access_key: str, secret_access_key: str) -> None:
    """
    This function uploads a file to an AWS S3 bucket.

    Args:
        file_name (str): The name of the file to upload.
        bucket (str): The name of the bucket to upload the file to.
        folder (str): The folder path inside the bucket to upload the file to.
        access_key (str): The AWS access key to access the S3 bucket.
        secret_access_key (str): The AWS secret access key to access the S3 bucket.

    Returns:
        None: None if the file was uploaded successfully.

    Raises:
        Exception: If any error occurs while uploading the file.
    """
    try:
        s3 = boto3.client('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_access_key)
        s3.upload_file(file_name, bucket, folder + file_name)
    except Exception as err:
        print(f"[ERROR: ] uploading file to S3: {err}", file=sys.stderr)
        raise


def main() -> None:
    '''
    This function runs the main program that reads the API, transforms the data,
    saves it to a local CSV file and uploads it to AWS S3.

    Raises:
        Exception: If an error occurs during the execution of the program.
    '''
    try:
        app_config = toml.load('config.toml')
        url = app_config['api']['url']

        print('Reading the API...')
        data = read_api(url)
        print('API Reading Done!')

        print('Building the dataframe...')
        df = transform_data(data)

        file_name = 'jobs.csv'
        print(f'dataframe saved to local file called {file_name}')
        save_to_csv(df, file_name)

        print('Uploading to AWS S3...')
        load_dotenv()
        access_key = os.getenv('ACCESS_KEY') 
        secret_access_key = os.getenv('SECRET_ACCESS_KEY') 
        bucket = app_config['aws']['bucket']
        folder = app_config['aws']['folder']
        
        upload_to_s3(file_name, bucket, folder, access_key, secret_access_key)
        print('File uploading Done!')

    except Exception as err:
        print(f"[ERROR: ] in main: {err}", file=sys.stderr)
        raise

if __name__ == '__main__':
    main()
