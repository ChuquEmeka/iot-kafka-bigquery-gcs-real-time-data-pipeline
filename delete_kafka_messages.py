from confluent_kafka.admin import AdminClient, ConfigResource
import time

# Kafka configuration
conf = {
    'bootstrap.servers': '<your bootstrap server>',
    'security.protocol': 'SASL_SSL',
    'sasl.mechanism': 'PLAIN',
    'sasl.username': '<your api key>',
    'sasl.password': '<your api secret>'
}

# Create AdminClient
admin_client = AdminClient(conf)

# List all topics
metadata = admin_client.list_topics(timeout=10)
topics = metadata.topics.keys()
print("Topics found:", list(topics))

# Function to update topic retention
def update_retention(topic, retention_ms):
    config_resource = ConfigResource('topic', topic, set_config={"retention.ms": str(retention_ms)})
    futures = admin_client.alter_configs([config_resource])
    for topic_config, future in futures.items():
        try:
            future.result()
            print(f"Updated retention.ms to {retention_ms} for {topic}")
        except Exception as e:
            print(f"Failed to update retention for {topic}: {e}")

# Delete messages by setting retention to 1ms, then reset to 7 days
for topic in topics:
    # Skip internal topics
    if topic.startswith("_confluent"):
        continue

    print(f"Processing topic: {topic}")
    update_retention(topic, 1)
    print("Waiting 10 seconds for messages to be deleted...")
    time.sleep(10)
    update_retention(topic, 604800000)

print("All messages deleted and retention reset.")
