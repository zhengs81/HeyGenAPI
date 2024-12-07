from subprocess import Popen
import requests
import time
from client import VideoTranslationClient

def status_callback(status):
    print(f"Callback: Job status changed to {status}.")


def run_integration_test():
    # Start the server
    server_process = Popen(["python", "server.py"])
    time.sleep(1)  # Give server time to start

    try:
        client = VideoTranslationClient("http://127.0.0.1:5000", verbose=True)
        result = client.wait_for_completion(callback=status_callback)
        # time.sleep(3)
        print(f"Final status: {result}")

    finally:
        # Stop the server
        server_process.terminate()

if __name__ == "__main__":
    run_integration_test()
