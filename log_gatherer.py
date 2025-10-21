
"""
Log Gatherer Component
Senior Project: Linux Anomaly Detection System
Team: Marlowe Elmiger, Miles Lindsey, Tockukwu Okwudire
Date: 10/21/2025


"""


import requests
import tarfile
from pathlib import Path


class LogGatherer:
    
    # For this project, our group will be using logpai/loghub which is a large third-party dataset of logs.
    # We want the dataset to be automatically downloaded the first time we run this program.
    # The loghub datasets are hosted on a platform called Zenodo


    # The Zenodo record ID where LogHub datasets are stored
    # This ID will be used in the download URL below
    ZENODO_RECORD = "8196385"
    


    # Initializes the log gatherer and sets up a cache directory where the downloaded logs will be stored
    def __init__(self, cache_dir="./logs"):

        # This path object is useful because it automatically uses the correct seperator for the OS being used.
        self.cache_dir = Path(cache_dir)

        # creates a cache directory for dataset ONLY if it doesnt exist already
        self.cache_dir.mkdir(exist_ok=True)

        # URL for downloading from Zenodo
        self.base_url = f"https://zenodo.org/records/{self.ZENODO_RECORD}/files"
    

    # Extracts a compressed archive
    def _extract_archive(self, archive_path, extract_to):

        # Opens the tar.gz file in read mode ('r:gz' means read with gzip compression)
        with tarfile.open(archive_path, 'r:gz') as tar:
            # Extracts all files from the archive to the destination directory
            tar.extractall(extract_to)

    
    # Downloads and extracts a log dataset from Zenodo.
    def download(self, dataset_name):

        log_file = self.cache_dir / "Linux" / "Linux.log"
        
        # checks to see if we have the extracted log file already. If thats the case, we don't need to download or extract anything
        if log_file.exists():
            # Will print this if already downloaded to let the user know
            print(f"Found cached file:: {log_file}")
            return log_file
        
        # creates the download URL
        url = f"{self.base_url}/Linux.tar.gz?download=1"

        # makes the local save path
        archive_path = self.cache_dir / "Linux.tar.gz"
        
        # prints the status so users know whats actually going on
        print(f"Downloading Linux logs from Zenodo...")
        
        
        # This part tries to  download and extract the file, and handles all the download errors that could happen
        try:
             # Downloads the file from Zenodo (the timeout 300 means waiting up to 5 minutes to download. The stream=true means downloading in chunks to save memory)
            response = requests.get(url, timeout=300, stream=True)

            # Checks if download was successful
            response.raise_for_status()
            
            # Saves to a file in 8KB chunks to handle large downloads efficiently
            with open(archive_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print(f"Downloaded to: {archive_path}")
            
            # Makes the extraction directory (e.g., ./logs/Linux/)
            extract_dir = self.cache_dir / "Linux"
            extract_dir.mkdir(exist_ok=True)
            # Extracts the compressed archive
            self._extract_archive(archive_path, extract_dir)

            print(f"Extraction complete!")

            # Deletes the compressed file to save some space
            archive_path.unlink()
            
            # Returns the path to the extracted log file
            return log_file
        
        # If download fails
        except requests.exceptions.RequestException as e:
            # Shows error message
            print(f"Failed to download Linux logs: {e}")
            raise
    
    # reads logs from dataset into memory (can be very memory intensive/ good for smaller datasets or when you need random access to logs)
    # We will use this method for training and developing our model
    def read_logs(self, dataset_name, max_lines=None):

        #Before we are able to read logs, we need to make sure the file exists on our computer. This line checks for that.
        log_file = self.download(dataset_name)

        # Initializes an empty list to store log lines
        logs = []
        
        # Opens the file for reading
        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:

            # Iterates through each line in the file
            for i, line in enumerate(f):

                #removes whitespace
                line = line.strip()

                # skips empty lines
                if line:
                    # Appends this log line to our list
                    logs.append(line)

                # Checks if we've read enough lines
                if max_lines and i + 1 >= max_lines:
                    break
        # Returns the complete list of log lines
        return logs
    

    # This method can handle millions of logs without crashing (is more memory efficient than reading logs into memory)
    # We will use this method for real-time anomoly detection on the full dataset
    def stream_logs(self, dataset_name):

        #Before we are able to read logs, we need to make sure the file exists on our computer. This line checks for that.
        log_file = self.download(dataset_name)
        
        # Opens the file for reading
        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:

            # Iterate through each line in the file
            for line in f:

                #removes whitespace
                line = line.strip()
                # skips empty lines
                if line:
                    # returns one line at a time then pauses
                    yield line

# This code right here is meant for testing purposes 
# When imported as a module, it wont run.
if __name__ == "__main__":

    # Creates an instance of LogGatherer
    gatherer = LogGatherer()
    
    
    print("\nTESTING:")
    
    print("\nMethod 1: Reading logs into memory\n")
    
    # Reads the first 10 lines from the Linux dataset using read_log method
    logs = gatherer.read_logs("Linux", max_lines=10)
    print(f"\nRead {len(logs)} lines from Linux logs:")
    
    #creates a numbered list as well as log content
    for i, log in enumerate(logs, 1):

        # log[:80] takes only the first 80 characters so the lines arent too long
        print(f"  {i}. {log[:80]}...")
    
    
    print("\nMethod 2: Streaming logs")
    
    # Streams the first 5 lines from the Linux dataset using stream_log method
    print("\nStreaming logs (first 5 only):\n")
    
    #creates a numbered list as well as log content
    for i, log in enumerate(gatherer.stream_logs("Linux"), 1):

        # log[:80] takes only the first 80 characters so the lines arent too long
        print(f"  {i}. {log[:80]}...")

        # Stop after 5 examples
        if i >= 5:
            break
    
    
    
    