from flask import Flask, jsonify
import random
import time
from threading import Thread

app = Flask(__name__)

# configurable amount of time for video processing
DELAY_SECONDS = 7

# initial status 
job_status = {"status": "pending"}

# update status 
def simulate_status_update():
    time.sleep(DELAY_SECONDS)  # Wait for the delay
    job_status["status"] = random.choice(["completed", "error"])

# start the status update simulation in a background thread, use a thread to simulate 
# backend processing, to make sure main is not blocked 
status_update_thread = Thread(target=simulate_status_update)
status_update_thread.daemon = True  # make sure it stops when program exit
status_update_thread.start()

@app.route('/status', methods=['GET'])
def get_status():
    return jsonify({"result": job_status["status"]})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
