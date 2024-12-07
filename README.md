# Video Translation Client Library

## Overview

This library provides a simple way to interact with a video translation server. It can check the status of a job and efficiently wait for it to complete.

## Installation

### Install Python dependencies:

pip install -r requirements.txt


### Run the server:

python server.py


## Usage

### Using the Client Library

```
from client import VideoTranslationClient

def status_callback(status):
    print(f"Callback: Job status changed to {status}.")

client = VideoTranslationClient("http://127.0.0.1:5000", verbose=True)
result = client.wait_for_completion(callback=status_callback)
print(f"Job status: {result}")
```


## Run Test

python test.py
