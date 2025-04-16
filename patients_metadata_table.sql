-- Create a table for patient metadata to use in joins
SET 'auto.offset.reset' = 'latest';
CREATE TABLE patient_metadata_table (
    patient_id STRING PRIMARY KEY,
    age INT,
    gender STRING,
    medical_history STRING,
    emergency_contact STRING,
    blood_type STRING,
    allergies STRING,
    last_checkup_date STRING,
    device_id STRING,
    data_format STRING,
    timestamp STRING
) WITH (KAFKA_TOPIC='patient-metadata', VALUE_FORMAT='JSON', KEY_FORMAT='KAFKA');
UNSET 'auto.offset.reset';