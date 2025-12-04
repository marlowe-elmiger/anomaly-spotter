
"""
Log Gatherer Component
Senior Project: Linux Anomaly Detection System
Team: Marlowe Elmiger, Miles Lindsey, Tockukwu Okwudire
Date: 12/4/2025


"""


import requests
import tarfile
from pathlib import Path


class LogGatherer:
    
    # For this project, our group will be using logpai/loghub which is a large third-party dataset of logs.
    # We want the dataset to be automatically downloaded the first time we run this program.
    # The loghub datasets are hosted on a platform called Zenodo


    
    # This ID will be used in the download URL below
    ZENODO_RECORD = "8196385"
    


    # Initializes the log gatherer and sets up a cache directory where the downloaded logs will be stored
    def __init__(self, cache_dir="./logs"):

        
        self.cache_dir = Path(cache_dir)

        # creates a cache directory for dataset ONLY if it doesnt exist already
        self.cache_dir.mkdir(exist_ok=True)

        
        self.base_url = f"https://zenodo.org/records/{self.ZENODO_RECORD}/files"
    

    # Extracts a compressed archive
    def _extract_archive(self, archive_path, extract_to):

        # Opens the tar.gz file in read mode
        with tarfile.open(archive_path, 'r:gz') as tar:
            # Extracts all files from the archive to the destination directory
            tar.extractall(extract_to)

    
    # Downloads and extracts a log dataset from Zenodo
    def download(self):

        log_file = self.cache_dir / "Linux" / "Linux.log"
        
        
        if log_file.exists():
            
            print(f"Found cached file: {log_file}")
            return log_file
        
        # creates the download URL
        url = f"{self.base_url}/Linux.tar.gz?download=1"

       
        archive_path = self.cache_dir / "Linux.tar.gz"
        
        
        print(f"Downloading Linux logs from Zenodo...")
        
        
        # This part tries to  download and extract the file, and handles all the download errors that could happen
        try:
             # Downloads the file from Zenodo, timeout=300 for large files (5 minutes) and stream=True for saving memory
            response = requests.get(url, timeout=300, stream=True)

            
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
        
        
        except requests.exceptions.RequestException as e:
            
            print(f"Failed to download Linux logs: {e}")
            raise
    
    # reads logs from dataset into memory 
    def read_logs(self, max_lines=None):

        # Makes sure log file is downloaded first
        log_file = self.download()

       
        logs = []
        
        # Opens the file for reading
        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:

            
            for i, line in enumerate(f):

                line = line.strip()
                
                if line:
                    
                    logs.append(line)

                if max_lines and i + 1 >= max_lines:
                    break
        # Returns the complete list of log lines
        return logs
    

# Testing
if __name__ == "__main__":

    
    gatherer = LogGatherer()
    
    
    print("\nTESTING:")
    
    
    # Reads the first 10 lines from the Linux dataset using read_log method
    logs = gatherer.read_logs( max_lines=10)
    print(f"\nRead {len(logs)} lines from Linux logs:")
    
    for i, log in enumerate(logs, 1):

        print(f"  {i}. {log}")
    
    

    
    
    
    