# Job Data API to CSV and S3

This project retrieves job data from the [Muse Job API](https://www.themuse.com/developers/api/v2) and converts the relevant data into a CSV file, which is then saved to an S3 bucket.

## Scenario

The following API URL to retrieve job data from page 50:

`https://www.themuse.com/api/public/jobs?page=50`


## Requirements

The project includes the following files:

-   A shell scripts to set up your virtual environment and run the main python script
-   .gitignore file
-   A Python run script
-   A toml file for configuring parameters
-   A requirements.txt to load dependancies for the Python script

It is recommended to initiate your project environment with a shell script and use a run.sh script to run the Python script.

## Project Diagram

![alt text](https://github.com/stantaov/wcd_python_cloud_project/blob/main/image.png?raw=true)

## Data Extraction

From the JSON "Response body", the script extracts the following information:

-   Publication date
-   Job name
-   Job type
-   Job location
-   Company name

## CSV Conversion and S3 Storage

After extracting the required data, the script will convert it into a CSV file and save it to an S3 bucket using boto3.

## Getting Started

To get started with the project, follow these steps:

1.  Clone the repository and navigate to the project directory.
2.  Run the init.sh shell script to set up the virtual environment and install the required packages.
3.  Configure the toml file with the appropriate parameters and store your secrets in the separate secrets file.
4.  Execute run.sh to start the Python run script, which will retrieve the job data from the API, convert it to CSV, and save it to the S3 bucket.