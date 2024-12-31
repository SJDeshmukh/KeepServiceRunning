from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import gunicorn
app = Flask(__name__)

scheduler = BackgroundScheduler()
scheduler.start()

DEFAULT_URL = "https://cartoonishimage.onrender.com/"
DEFAULT_INTERVAL = 40  # Default interval in seconds

# Function to trigger the website
def trigger_website(url):
    try:
        response = requests.get(url)
        print(f"Triggered {url}: Status Code {response.status_code}")
    except Exception as e:
        print(f"Error triggering {url}: {e}")

# Function to start the trigger
def start_default_trigger():
    scheduler.add_job(func=trigger_website, args=[DEFAULT_URL], trigger="interval", seconds=DEFAULT_INTERVAL, id="default_trigger", replace_existing=True)
    print("Trigger service is active and running.")

# API to stop the triggering
@app.route('/stop', methods=['POST'])
def stop_trigger():
    try:
        scheduler.remove_all_jobs()
        print("Service to trigger has been stopped.")
        return jsonify({"message": "Stopped all triggers"}), 200
    except Exception as e:
        print(f"Error stopping the service: {e}")
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    # Ensure the trigger starts when the app runs
    start_default_trigger()
    app.run()
