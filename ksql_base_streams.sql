-- Create base streams to read raw JSON data from Kafka topics
CREATE STREAM heart_rate_stream (
    event_id STRING,  -- Added to store the unique event ID
    patient_id STRING KEY,
    heart_rate INT,
    timestamp STRING,
    data_type STRING
) WITH (KAFKA_TOPIC='heart-rate-data', VALUE_FORMAT='JSON', KEY_FORMAT='KAFKA');

CREATE STREAM blood_oxygen_stream (
    event_id STRING,  -- Added to store the unique event ID
    patient_id STRING KEY,
    spo2 INT,
    timestamp STRING,
    data_type STRING
) WITH (KAFKA_TOPIC='blood-oxygen-data', VALUE_FORMAT='JSON', KEY_FORMAT='KAFKA');

CREATE STREAM blood_pressure_stream (
    event_id STRING,  -- Added to store the unique event ID
    patient_id STRING KEY,
    systolic INT,
    diastolic INT,
    timestamp STRING,
    data_type STRING
) WITH (KAFKA_TOPIC='blood-pressure-data', VALUE_FORMAT='JSON', KEY_FORMAT='KAFKA');

CREATE STREAM fall_detection_stream (
    event_id STRING,  -- Added to store the unique event ID
    patient_id STRING KEY,
    fall_detected BOOLEAN,
    timestamp STRING,
    data_type STRING
) WITH (KAFKA_TOPIC='fall-detection-data', VALUE_FORMAT='JSON', KEY_FORMAT='KAFKA');