import logging
import os
import yaml
import json
import requests

from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
from tqdm import tqdm

from google.cloud import storage
from google.oauth2 import service_account


class ModelDownload:
    def __init__(self, config_file: str, max_workers: int = 1, model_path: str = None, key_file: str = None):
        self.config_data = None
        self.gcs_client = None
        self.max_workers = max_workers
        self.model_path = model_path
        self.config_file = config_file
        self.key_file = key_file

    # Start the download process
    def start(self):
        # Check if the model path is provided
        if self.model_path is None:
            logging.error("Model path is required.")
            return

        # Check if the file exists
        if not os.path.exists(self.config_file):
            logging.error(f"File '{self.config_file}' does not exist.")
            return

        # Create a GCS client using the credentials if a key file is provided
        if self.key_file is not None:
            with open(self.key_file) as f:
                json_key = json.load(f)
            credentials = service_account.Credentials.from_service_account_info(json_key)
            self.gcs_client = storage.Client(project=json_key['project_id'], credentials=credentials)

        # Load the nodes file
        with open(self.config_file, 'r') as file:
            self.config_data = yaml.safe_load(file)
        pass

        # Download each model type
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Retrieve each model type and its models
            executor.map(self.__download_model_type, self.config_data['models'].items())

    # Download each model type
    def __download_model_type(self, model_type_items):
        model_type, models = model_type_items

        # Define the directory where the models will be saved
        dir_path = os.path.join(self.model_path, model_type)

        # Create the directory if it does not exist
        os.makedirs(dir_path, exist_ok=True)

        # Download each model and save it in the model_path
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            executor.map(lambda model: self.__download_model(model, dir_path), models)

    # Download a model
    def __download_model(self, model, dir_path):
        try:
            model_name = model['name']
            model_url = model['url']
            force_download = model.get('force_download', False)

            # Define the path where the file will be saved
            file_path = os.path.join(dir_path, model_name)

            parsed_url = urlparse(model_url)

            # If parent folder does not exist, create it. exist_ok=True makes make it not raise an error if it
            # already exists.
            folder_name = os.path.dirname(file_path)
            os.makedirs(folder_name, exist_ok=True)

            if parsed_url.scheme == 'gs':
                if self.gcs_client is None:
                    logging.error("GCS client is required to download models from GCS."
                                  "Please provide a key file to authenticate with GCS.")
                    return

                # Handling GCS URL
                bucket_name = parsed_url.netloc
                blob = self.gcs_client.bucket(bucket_name).get_blob(parsed_url.path.lstrip('/'))
                logging.info(f"Blob {blob.path} size: {blob.size}")
                download_needed = (
                        not os.path.exists(file_path)
                        or force_download
                        or (os.path.exists(file_path) and os.path.getsize(file_path) != blob.size)
                )

                if download_needed:
                    reason = "force_download" if force_download else "does not exist" \
                        if not os.path.exists(file_path) else "size is different"
                    logging.info(f"Downloading {file_path}... because {reason}")
                    blob.download_to_filename(file_path)
                    logging.info(f"Model {file_path} downloaded successfully from GCS.")
                else:
                    logging.info(f"File {file_path} Size: {os.path.getsize(file_path)}")
                    logging.info(f"File {file_path} already exists and is up to date. Skipping download.")
            else:
                # Send a HEAD request to the model URL to get the file size
                response = requests.head(model_url, allow_redirects=True)
                if response.status_code != 200:
                    logging.error(
                        f"Failed to get file size for {file_path} from {model_url}. Status code: "
                        f" {response.status_code}")
                    if force_download:
                        logging.info(f"Forcing download ({file_path} from {model_url})...")
                        server_file_size = 0
                    else:
                        return
                else:
                    server_file_size = int(response.headers.get('content-length', 0))

                # Check if the file already exists and has the same size as the server's file
                if os.path.exists(file_path) and os.path.getsize(file_path) == server_file_size:
                    if force_download:
                        logging.info(f"Forcing download ({file_path} from {model_url})...")
                        server_file_size = 0
                    else:
                        logging.info(
                            f"File {file_path} already exists and has the same size as the server's file. Skipping "
                            f"download.")
                        return

                # Send a GET request to the model URL
                response = requests.get(model_url, stream=True, allow_redirects=True)

                # If the response status code is 200, write the content to a file
                if response.status_code == 200:
                    block_size = 1024 * 1024  # 1 Megabyte
                    progress_bar = tqdm(total=server_file_size, unit='iB', unit_scale=True)

                    with open(file_path, 'wb') as file:
                        for data in response.iter_content(block_size):
                            progress_bar.update(len(data))
                            file.write(data)

                    progress_bar.close()

                    if server_file_size != 0 and progress_bar.n != server_file_size:
                        logging.error("ERROR, something went wrong while downloading the file.")

                else:
                    logging.error(f"Failed to download {file_path} from {model_url}. Status code: "
                                  f"{response.status_code}")
                    exit(1)

            logging.info(f"Model {file_path} downloaded successfully.")
            return
        except Exception as e:
            logging.error(f"Failed to download {model['name']}. Reason: {e}")
            return
