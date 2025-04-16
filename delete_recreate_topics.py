import subprocess
import time
import json

# List of topics to recreate
topics_to_recreate = [
    "heart-rate-data",
    "blood-oxygen-data",
    "blood-pressure-data",
    "fall-detection-data",
    "patient-metadata"
]

# Function to run a shell command and handle errors
def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f" Command executed successfully: {command}")
        print(result.stdout)
    else:
        print(f" Warning: Command failed but continuing: {command}")
        print(result.stderr)

# Step 1: List all topics in JSON format
print(" Listing all Kafka topics (JSON format)...")
list_topics_cmd = "confluent kafka topic list --output json"
result = subprocess.run(list_topics_cmd, shell=True, capture_output=True, text=True)

try:
    topics_json = json.loads(result.stdout)
    all_topics = [topic['name'] for topic in topics_json]
except json.JSONDecodeError as e:
    print(" Failed to parse JSON from topic list. Output was:")
    print(result.stdout)
    exit(1)

print(f"\nDeleting all existing topics: {all_topics}")

# Step 2: Delete every topic found
for topic in all_topics:
    print(f"\n Deleting topic: {topic}")
    delete_cmd = f"confluent kafka topic delete {topic} --force"
    run_command(delete_cmd)
    time.sleep(2)

# Step 3: Recreate only the specified topics
print(f"\n Recreating selected topics: {topics_to_recreate}")
for topic in topics_to_recreate:
    print(f"\n Creating topic: {topic}")
    create_cmd = f"confluent kafka topic create {topic} --partitions 6"
    run_command(create_cmd)
    time.sleep(2)

print("\n+ All topics have been deleted and required topics recreated.")
