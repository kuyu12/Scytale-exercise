# Scytale Exercise 

This project is an ETL (Extract, Transform, Load) pipeline designed to process data from GitHub repositories within the `Scytale-exercise` organization. The pipeline extracts pull request data, transforms it into a structured format using PySpark, and loads the result into a Parquet file.

## Table of Contents
- [Instructions](#instructions)
- [Setup](#setup)
- [Running the ETL](#running-the-etl)
- [Notes](#notes)
- [Project structue](#project-structue)

## Instructions

### Extract
- **Objective**: Retrieve all repositories from the `Scytale-exercise` organization on GitHub.
- For each repository, extract all pull requests.
- Save the extracted data as JSON files.

### Transform
- **Objective**: Use PySpark to transform the JSON files into a structured table.
- The table schema is as follows:
  - `Organization Name`
  - `repository_id`
  - `repository_name`
  - `repository_owner`
  - `num_prs`
  - `num_prs_merged`
  - `merged_at`
  - `is_compliant`
- Save the transformed data to a Parquet file.

### Load
- Load the transformed data into a specified storage location.

## Setup

### Prerequisites
- Python 3.9 or higher
- Apache Spark
- Docker (optional, for running with Docker Compose)


### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/kuyu12/Scytale-exercise.git
   cd Scytale-exercise
   ```

2. Install the required Python packages:
   ```bash
   pip install -r src/requirements.txt
   ```

3. Set the environment variable for the organization:

* set your [GitHub token](https://github.com/settings/tokens) as an environment variable named GITHUB_TOKEN
* Make sure the token has read permissions, **no write permissions are required**
* Define the organization name as an environment variable called ORGANIZATION_VAR_NAME.

   ```bash
   export ORGANIZATION_VAR_NAME='Scytale-exercise'
   export GITHUB_TOKEN='<YOUR_PERSONAL_GITHUB_TOKEN>'
   ```

## Running the ETL

### Locally
Ensure Spark is installed and configured in your environment. Then, run the ETL process with:
```bash
python src/etl.py
```

### Using Docker
You can also run the ETL process using Docker Compose:
```bash
docker-compose up
```

## Notes
- Ensure that the Spark path is correctly set in your environment variables if running locally.
- **Pagination Handling**: The ETL manages paginated API responses through the functionality provided by the GitHub library.
- **Rate Limit Handling**: The ETL includes logic to manage GitHub API rate limits.

## Project structue
```bash
|   .gitignore
|   docker-compose.yaml
|   README.md
|   setup.py
+---data
|   +---logs
|   |   |   errors.log
|   |   |   info.log
|   |   |   
|   |   \---config
|   |           logging.yaml
|   |           
|   +---processed  
|   +---raw  
+---src
|   |   etl.py
|   |   extract.py
|   |   transform.py
|   |   load.py
|   |   requirements.txt
|   |   dockerfile
|   |   
|   +---model
|   |   |   pull_request_data_model.py
|   |   |   repo_data_model.py
|   |   |   
|   |   +---schemas
|   |   |   |   pull_schema.py
|   |   |   |   repo_schema.py
|   |   |   |                 
|   +---providers
|   |   |   github_provider.py
|   |   |   
|   |   +---abstract
|   |   |   |   base_provider.py
|   |   |   |   git_provider.py
|   |   |   |                
|   +---utils
|   |   |   const.py
|   |   |   errors.py
|   |   |   logger_utils.py
|   |   |   spark_utils.py
|   |   |   utils.py
|   |   |     
+---tests
|   |   test_extract.py
|   |   test_load.py
|   |   test_transform.py
|   |   
```

---
