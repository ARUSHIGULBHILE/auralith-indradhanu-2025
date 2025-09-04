import time, json, random, requests

BACKEND_INGEST = "http://localhost:8000/iot/ingest"

def generate_payload(device_id="sim-01"):
    return {
        "device_id": device_id,
        "soil_moisture": round(random.uniform(20,70),2),
        "temperature": round(random.uniform(15,35),2),
        "humidity": round(random.uniform(40,90),2),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

if __name__ == "__main__":
    print("Starting sensor simulator. Sending data every 5 seconds to", BACKEND_INGEST)
    while True:
        payload = generate_payload()
        try:
            resp = requests.post(BACKEND_INGEST, json=payload, timeout=5)
            print("Sent:", payload, "Response:", resp.status_code)
        except Exception as e:
            print("Could not send to backend:", e)
        time.sleep(5)
