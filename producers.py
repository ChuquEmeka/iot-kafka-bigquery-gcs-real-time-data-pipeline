from confluent_kafka import Producer
import json
import random
import time
from datetime import datetime
import sys
import uuid  # Import the uuid library to generate unique event IDs

# Kafka configuration
conf = {
    'bootstrap.servers': '<your bootstrap server>',
    'security.protocol': 'SASL_SSL',
    'sasl.mechanism': 'PLAIN',
    'sasl.username': '<your api key>',
    'sasl.password': '<your api secret>'
}

# Create Producer instance and check for authentication errors
try:
    producer = Producer(conf)
    # Poll once to trigger any immediate connection errors
    producer.poll(0)
except Exception as e:
    print(f"Failed to initialize Kafka producer: {e}")
    print("Please check your API Key, API Secret, bootstrap server, and Confluent Cloud environment.")
    sys.exit(1)

# Function to generate a random patient ID (patient1 to patient5)
def generate_random_patient_id():
    return f"patient{random.randint(1, 5)}"

# Function to generate patient metadata (no event_id needed here)
def generate_patient_metadata(patient_id):
    return {
        "patient_id": patient_id,
        "age": random.randint(30, 85),
        "gender": random.choice(["Male", "Female", "Other"]),
        "medical_history": random.choice(["Hypertension", "Diabetes", "Asthma", "None"]),
        "emergency_contact": f"+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
        "blood_type": random.choice(["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]),
        "allergies": random.choice(["Peanuts", "Penicillin", "None"]),
        "last_checkup_date": "2024-10-01",
        "device_id": f"smartwatch-{patient_id}",
        "data_format": "JSON"
    }

# Function to generate heart rate data with a unique event_id
def generate_heart_rate_data():
    patient_id = generate_random_patient_id()
    timestamp = datetime.utcnow().isoformat() + "Z"
    return {
        "event_id": str(uuid.uuid4()),  # Generate a unique event ID
        "patient_id": patient_id,
        "heart_rate": random.randint(40, 140),  # Normal range: 60-100 bpm
        "timestamp": timestamp,
        "data_type": "heart_rate"
    }

# Function to generate blood oxygen data with a unique event_id
def generate_blood_oxygen_data():
    patient_id = generate_random_patient_id()
    timestamp = datetime.utcnow().isoformat() + "Z"
    return {
        "event_id": str(uuid.uuid4()),  # Generate a unique event ID
        "patient_id": patient_id,
        "spo2": random.randint(85, 100),  # Normal range: 95-100%
        "timestamp": timestamp,
        "data_type": "blood_oxygen"
    }

# Function to generate blood pressure data with a unique event_id
def generate_blood_pressure_data():
    patient_id = generate_random_patient_id()
    timestamp = datetime.utcnow().isoformat() + "Z"
    return {
        "event_id": str(uuid.uuid4()),  # Generate a unique event ID
        "patient_id": patient_id,
        "systolic": random.randint(90, 180),  # Normal range: 90-120 mmHg
        "diastolic": random.randint(60, 110),  # Normal range: 60-80 mmHg
        "timestamp": timestamp,
        "data_type": "blood_pressure"
    }

# Function to generate fall detection data with a unique event_id
def generate_fall_detection_data():
    patient_id = generate_random_patient_id()
    timestamp = datetime.utcnow().isoformat() + "Z"
    return {
        "event_id": str(uuid.uuid4()),  # Generate a unique event ID
        "patient_id": patient_id,
        "fall_detected": random.choice([True, False]),
        "timestamp": timestamp,
        "data_type": "fall_detection"
    }

# Delivery callback to handle message delivery status
def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
        if "authentication" in str(err).lower():
            print("Authentication failure detected. Stopping the producer...")
            producer.flush(timeout=10)
            producer.close()
            sys.exit(1)
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

# Produce patient metadata for each patient (patient1 to patient5)
for patient_number in range(1, 6):
    patient_id = f"patient{patient_number}"
    metadata = generate_patient_metadata(patient_id)
    print(f"Sent patient metadata for {patient_id}: {metadata}")
    producer.produce('patient-metadata', key=patient_id.encode('utf-8'), value=json.dumps(metadata).encode('utf-8'), callback=delivery_report)

# Flush the producer to ensure metadata is sent (with timeout)
producer.flush(timeout=10)

# Produce health data in a loop
try:
    while True:
        # Poll to process callbacks and allow the producer to handle interrupts
        producer.poll(0)

        # Generate and send heart rate data
        heart_rate_data = generate_heart_rate_data()
        print(f"Sent heart rate data: {heart_rate_data}")
        producer.produce('heart-rate-data', key=heart_rate_data["patient_id"].encode('utf-8'), value=json.dumps(heart_rate_data).encode('utf-8'), callback=delivery_report)

        # Generate and send blood oxygen data
        blood_oxygen_data = generate_blood_oxygen_data()
        print(f"Sent blood oxygen data: {blood_oxygen_data}")
        producer.produce('blood-oxygen-data', key=blood_oxygen_data["patient_id"].encode('utf-8'), value=json.dumps(blood_oxygen_data).encode('utf-8'), callback=delivery_report)

        # Generate and send blood pressure data
        blood_pressure_data = generate_blood_pressure_data()
        print(f"Sent blood pressure data: {blood_pressure_data}")
        producer.produce('blood-pressure-data', key=blood_pressure_data["patient_id"].encode('utf-8'), value=json.dumps(blood_pressure_data).encode('utf-8'), callback=delivery_report)

        # Generate and send fall detection data
        fall_detection_data = generate_fall_detection_data()
        print(f"Sent fall detection data: {fall_detection_data}")
        producer.produce('fall-detection-data', key=fall_detection_data["patient_id"].encode('utf-8'), value=json.dumps(fall_detection_data).encode('utf-8'), callback=delivery_report)

        # Flush the producer with a timeout to ensure messages are sent
        producer.flush(timeout=5)

        # Wait for 5 seconds before sending the next set of data
        time.sleep(5)

except KeyboardInterrupt:
    print("Stopping the producer...")
    producer.flush(timeout=10)
    producer.close()
    print("Producer stopped successfully.")
    sys.exit(0)