# Healthcare IoT Data Pipeline Project

Watch the video demonstration of this project on [YouTube](https://youtu.be/1tE6pKaLzpI) to see the pipeline in action.

## Table of Contents

- [What You Will Achieve](#what-you-will-achieve)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Step-by-Step Guide](#step-by-step-guide)
  - [Step 1: Sign Up and Create a Cluster in Confluent Cloud](#step-1-sign-up-and-create-a-cluster-in-confluent-cloud)
  - [Step 2: Set Up Your Confluent Cloud Environment](#step-2-set-up-your-confluent-cloud-environment)
  - [Step 3: Generate API Key and Secret for Confluent Cloud](#step-3-generate-api-key-and-secret-for-confluent-cloud)
  - [Step 4: Create Kafka Topics](#step-4-create-kafka-topics)
  - [Step 5: Set Up Google Cloud Storage (GCS) and BigQuery](#step-5-set-up-google-cloud-storage-gcs-and-bigquery)
  - [Step 6: Create a Dataset in BigQuery](#step-6-create-a-dataset-in-bigquery)
  - [Step 7: Create BigQuery Tables for Processed Data](#step-7-create-bigquery-tables-for-processed-data)
  - [Step 8: Run the Data Producer](#step-8-run-the-data-producer)
  - [Step 9: Deploy a Google Cloud Storage Sink Connector](#step-9-deploy-a-google-cloud-storage-sink-connector)
  - [Step 10: Set Up ksqlDB for Stream Processing](#step-10-set-up-ksqldb-for-stream-processing)
  - [Step 11: Deploy a BigQuery Sink Connector](#step-11-deploy-a-bigquery-sink-connector)
  - [Step 12: Verify the Pipeline](#step-12-verify-the-pipeline)
  - [Step 13: Analyze Data in BigQuery](#step-13-analyze-data-in-bigquery)
  - [Step 14: Troubleshoot Issues](#step-14-troubleshoot-issues)

## What You Will Achieve

- Archive raw data in GCS as a single source of truth.
- Process data in real-time with ksqlDB (flattening JSON, adding metadata, performing joins).
- Store processed data in BigQuery for analytics (e.g., detecting low oxygen levels or falls).
- Monitor patient health in real-time using a scalable, fault-tolerant pipeline.

## Tech Stack

- **Confluent Cloud (Kafka):** Streams data in real-time.
- **ksqlDB:** Processes data with SQL-like queries on Confluent Cloud.
- **Python (Producer):** Simulates IoT health data.
- **Google Cloud Storage (GCS):** Archives raw data.
- **Google BigQuery:** Stores processed data for analytics.
- **Google Cloud Storage Sink Connector:** Moves raw data to GCS.
- **BigQuery Sink Connector:** Moves processed data to BigQuery.

## Prerequisites

- A Confluent Cloud account.
- A Google Cloud account with BigQuery and GCS enabled.
- Python installed with required libraries (see [requirements.txt](requirements.txt)).

## Step-by-Step Guide

### Step 1: Sign Up and Create a Cluster in Confluent Cloud

- Go to confluent.cloud and sign up.
- Create a cluster named `<your cluster name>`:
  - Click `Clusters` > `Create cluster`.
  - Choose the `Basic` cluster type.
  - Name it `<your cluster name>`.

**Details:**

- The Basic Cluster uses eCKUs for auto-scaling, adding brokers when the workload increases and scaling down to zero when idle.
- This ensures high throughput and scalability, supporting parallel processing across 6 partitions per topic.
- With a replication factor of 3, data is copied across brokers for fault tolerance.

**What This Achieves:**

Sets up the foundation for your pipeline by creating a Kafka cluster on Confluent Cloud, enabling real-time data streaming with auto-scaling and fault tolerance.

### Step 2: Set Up Your Confluent Cloud Environment

- Create an environment named `<your environment name>`:
  - Click `Environments` > `Create environment`.
  - Name it `<your environment name>`.
- Assign `<your cluster name>` to `<your environment name>`:
  - Go to `<your environment name>`, click `Set cluster`, and select `<your cluster name>`.

**What This Achieves:**

Organizes your pipeline components (topics, connectors) into a single environment, making management easier and ensuring all resources work together seamlessly.

### Step 3: Generate API Key and Secret for Confluent Cloud

- In Confluent Cloud, go to `<your cluster name>`.
- Click `API Keys` > `Create key`:
  - Select `Granular access` and give the key access to all topics in `<your cluster name>`.
  - Download the key and secret:
    - API Key: `<your API Key>`
    - API Secret: `<your API Secret>`

**What This Achieves:**

Provides secure credentials for your producer and connectors to access Kafka topics, ensuring only authorized processes can interact with your cluster.

### Step 4: Create Kafka Topics

- In Confluent Cloud, go to `<your cluster name>` > `Topics` > `Create topic`.
- Create the following topics:
  - `heart-rate-data`
  - `blood-oxygen-data`
  - `blood-pressure-data`
  - `fall-detection-data`
  - `patient-metadata`
- For each topic:
  - Set `Number of partitions` to 6 (enables parallel processing for better throughput).
  - Set `Replication factor` to 3 (for fault tolerance).
  - Set `Retention time` to 1 week.
- To automate topic creation, use the script [delete_recreate_topics.py](delete_recreate_topics.py).

**What This Achieves:**

Prepares Kafka topics to receive health data, with 6 partitions for parallelism and replication for reliability, ensuring the pipeline can handle data efficiently.

### Step 5: Set Up Google Cloud Storage (GCS) and BigQuery

- Sign up for Google Cloud at cloud.google.com.
- Create a project named `<your project ID>`:
  - Click `Select a project` > `New Project`.
  - Name it `<your project ID>`.
- Enable the BigQuery API and Cloud Storage API:
  - Go to `APIs & Services` > `Library`.
  - Search for `BigQuery API` and `Cloud Storage API`, and enable both.
- Create a GCS bucket:
  - Go to `Cloud Storage` > `Buckets` > `Create`.
  - Name it `<your bucket name>`.
  - Use default settings (e.g., location: `us-central1`).
- Create a service account:
  - Go to `IAM & Admin` > `Service Accounts` > `Create Service Account`.
  - Name it `<your service account name>`.
  - Grant roles: `BigQuery Admin` and `Storage Admin`.
  - Create a key: Click the service account, go to `Keys` > `Add Key` > `JSON`, and save as `service_account.json`.

**What This Achieves:**

Configures GCS for archiving raw data and BigQuery for analytics, with a service account to allow secure data transfer between your pipeline and Google Cloud.

### Step 6: Create a Dataset in BigQuery

- In Google Cloud, go to BigQuery.
- Create a dataset named `<your dataset name>`:
  - Click `Create dataset`.
  - Set `Dataset ID` to `<your dataset name>`.
  - Set `Location` to `us-central1`.

**What This Achieves:**

Creates a container in BigQuery to organize your tables, preparing the storage space for processed health data.

### Step 7: Create BigQuery Tables for Processed Data

- In BigQuery, go to `<your dataset name>`.
- Run the SQL commands in [bigquery_tables_creation.sql](bigquery_tables_creation.sql) to create tables for processed data (e.g., `processed_heart_rate_data`).
- These tables include an `event_id` field as the primary key to ensure each record is unique.

**What This Achieves:**

Sets up structured tables in BigQuery to store processed health data, enabling analytics on metrics like heart rate or oxygen levels with unique event identifiers.

### Step 8: Run the Data Producer

- Use the script [producer.py](producer.py) to simulate health data from smartwatches and send it to Kafka topics.
- Update the script with:
  - Bootstrap server: `<your bootstrap server>` (find in `<your cluster name>` > `Cluster settings`).
  - API Key: `<your API Key>`
  - API Secret: `<your API Secret>`
- Run the script to send simulated data for 5 patients, including `event_id` as a unique identifier.
- To delete Kafka messages for a fresh start, use [delete_kafka_messages.py](delete_kafka_messages.py).

**What This Achieves:**

Simulates IoT health data (e.g., heart rate, blood oxygen) and sends it to Kafka topics, populating the pipeline with realistic data for processing and analysis.

### Step 9: Deploy a Google Cloud Storage Sink Connector

- In Confluent Cloud, go to `<your cluster name>` > `Connectors` > `Add connector`.
- Search for `Google Cloud Storage Sink` and select it.
- Configure the connector:
  - **Topics:** `heart-rate-data`, `blood-oxygen-data`, `blood-pressure-data`, `fall-detection-data`, `patient-metadata`
  - **API Key:** `<your API Key>`
  - **API Secret:** `<your API Secret>`
  - **GCS Credentials:** Upload `service_account.json`
  - **GCS Bucket Name:** `<your bucket name>`
  - **Output Format:** `JSON`
  - **Time Interval:** `3600` (1 hour)
  - **Path Prefix:** `raw_data/`
  - **Tasks:** 6 (matches the 6 partitions per topic)
- Name the connector `gcs-sink` and launch it.

**What This Achieves:**

Archives raw health data in GCS as a single source of truth, ensuring you have a durable backup of the original data for recovery or future use.

### Step 10: Set Up ksqlDB for Stream Processing

- In Confluent Cloud, go to `<your cluster name>` > `ksqlDB`.
- Create a ksqlDB application named `<your ksqlDB app name>`:
  - Click `Add application`, name it, and launch.
- Open the ksqlDB editor and run the following SQL scripts:
  - [ksql_base_streams.sql](ksql_base_streams.sql): Creates base streams for raw data.
  - [patients_metadata_table.sql](patients_metadata_table.sql): Creates a table for patient metadata.
  - [processed_streams.sql](processed_streams.sql): Creates processed streams, flattening JSON, adding metadata, and performing joins.

**What This Achieves:**

Processes raw data in real-time, flattening JSON, enriching it with patient metadata (e.g., age, medical history), and performing joins to prepare it for BigQuery analytics.

### Step 11: Deploy a BigQuery Sink Connector

- In Confluent Cloud, go to `<your cluster name>` > `Connectors` > `Add connector`.
- Search for `Google BigQuery Sink V2` and select it.
- Configure the connector:
  - **Topics:** `pksqlc-wzkdg9PROCESSED_HEART_RATE_STREAM_WITH_METADATA`, `pksqlc-wzkdg9PROCESSED_BLOOD_OXYGEN_STREAM_WITH_METADATA`, `pksqlc-wzkdg9PROCESSED_BLOOD_PRESSURE_STREAM_WITH_METADATA`, `pksqlc-wzkdg9PROCESSED_FALL_DETECTION_STREAM_WITH_METADATA`
  - **API Key:** `<your API Key>`
  - **API Secret:** `<your API Secret>`
  - **Authentication:** Upload `service_account.json`
  - **Project ID:** `<your project ID>`
  - **Dataset:** `<your dataset name>`
  - **Ingestion Mode:** `STREAMING`
  - **Input Format:** `JSON`
  - **Key Format:** `STRING`
  - **Sanitize Topics:** `false`
  - **Auto Update Schemas:** `DISABLED`
  - **Sanitize Field Names:** `false`
  - **Auto Create Tables:** `DISABLED`
  - **Tasks:** 6
- Name the connector `bigquery-sink` and launch it.

**What This Achieves:**

Moves processed data to BigQuery, enabling real-time analytics to detect health issues like low oxygen levels or falls, with 6 tasks for efficient data transfer.

### Step 12: Verify the Pipeline

- Let the producer run for a few minutes.
- Check GCS:
  - Go to Google Cloud > `Cloud Storage` > `<your bucket name>`.
  - Confirm raw data files are in `raw_data/`.
- Check processed topics in Confluent Cloud:
  - Go to `Topics` > `pksqlc-wzkdg9PROCESSED_BLOOD_OXYGEN_STREAM_WITH_METADATA`.
  - Verify `event_id` and `patient_id` are present in messages.
- Check BigQuery:
  - Go to BigQuery > `<your dataset name>` > `processed_blood_oxygen_data`.
  - Query: `SELECT * FROM <your dataset name>.processed_blood_oxygen_data LIMIT 10`.
  - Confirm `event_id` and other fields are populated.

**What This Achieves:**

Ensures the pipeline works as expected, verifying that raw data is archived, processed data is enriched, and analytics-ready data is in BigQuery.

### Step 13: Analyze Data in BigQuery

- In BigQuery, query the data to detect health issues:
  - Low oxygen levels: `SELECT event_id, patient_id, spo2, original_timestamp, age, medical_history FROM <your dataset name>.processed_blood_oxygen_data WHERE spo2 < 90 ORDER BY original_timestamp DESC LIMIT 10`
  - Irregular heart rates: `SELECT event_id, patient_id, heart_rate, original_timestamp, age, medical_history FROM <your dataset name>.processed_heart_rate_data WHERE heart_rate > 100 OR heart_rate < 60 ORDER BY original_timestamp DESC LIMIT 10`
  - Falls in elderly: `SELECT event_id, patient_id, fall_detected, original_timestamp, age, emergency_contact FROM <your dataset name>.processed_fall_detection_stream_with_metadata WHERE fall_detected = TRUE AND age > 65 ORDER BY original_timestamp DESC LIMIT 10`

**What This Achieves:**

Enables real-time health monitoring by querying processed data, identifying critical issues like low oxygen or falls for timely intervention.

### Step 14: Troubleshoot Issues

- If `event_id` is `null` in BigQuery:
  - Check processed topic messages in Confluent Cloud.
  - Review BigQuery Sink Connector logs for errors.
- If no data in BigQuery:
  - Confirm the connector is running (`bigquery-sink`).
  - Ensure the producer is sending data.
- If no data in GCS:
  - Check GCS Sink Connector logs (`gcs-sink`).
  - Verify `service_account.json` permissions.
- If the pipeline is slow:
  - Confirm 6 tasks are set in connectors.
  - Check if the cluster is auto-scaling in `<your cluster name>` > `Cluster overview`.

**What This Achieves:**

Helps identify and resolve issues in the pipeline, ensuring reliable operation for real-time health monitoring and data processing.