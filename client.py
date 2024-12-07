import requests
import time


class VideoTranslationClient:
    def __init__(self, base_url, max_retries=5, backoff_factor=2, timeout=30, verbose=False):
        """
        Initialize the Video Translation Client.
        
        Parameters:
            base_url (str): The base URL of the server.
            max_retries (int): Maximum number of retries before giving up.
            backoff_factor (float): Exponential backoff factor for polling.
            timeout (int): Maximum time (in seconds) to wait for a result.
            verbose (bool): Enable verbose logging for debugging.
        """
        self.base_url = base_url
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.timeout = timeout
        self.verbose = verbose

    def log(self, message):
        """Log messages if verbose mode is enabled."""
        if self.verbose:
            print(message)

    def get_status(self):
        """Fetch the current job status from the server."""
        try:
            response = requests.get(f"{self.base_url}/status")
            response.raise_for_status()
            return response.json()["result"]
        except requests.RequestException as e:
            self.log(f"Error occurred while fetching status: {e}")
            return "error"

    def wait_for_completion(self, callback=None):
        """
        Wait for the job to complete with exponential backoff.
        
        Parameters:
            callback (function): Optional function to call when status changes.
        
        Returns:
            str: Final status ("completed" or "error").
        """
        start_time = time.time()
        interval = 1  # Start with 1 second polling interval

        while True:
            status = self.get_status()

            if status in ["completed", "error"]:
                if callback:
                    callback(status)  # Notify the customer via callback
                return status

            elapsed_time = time.time() - start_time
            if elapsed_time > self.timeout:
                self.log("Timeout reached. Exiting...")
                return "timeout"

            self.log(f"Status: {status}. Retrying in {interval} seconds...")
            time.sleep(interval)
            interval = min(interval * self.backoff_factor, self.timeout - elapsed_time)  # Adjust interval
