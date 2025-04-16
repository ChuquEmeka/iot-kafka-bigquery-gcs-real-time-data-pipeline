CREATE TABLE `healthcare_dataset.processed_heart_rate_data` (
    event_id STRING,  
    patient_id STRING,
    heart_rate INT64,
    original_timestamp STRING,
    processed_timestamp INT64,
    age INT64,
    gender STRING,
    medical_history STRING,
    emergency_contact STRING,
    blood_type STRING,
    allergies STRING,
    last_checkup_date STRING,
    device_id STRING,
    data_format STRING,
    PRIMARY KEY(event_id) NOT ENFORCED  -- event_id is the unique identifier
);

CREATE TABLE `healthcare_dataset.processed_blood_oxygen_data` (
    event_id STRING,  
    patient_id STRING,
    spo2 INT64,
    original_timestamp STRING,
    processed_timestamp INT64,
    age INT64,
    gender STRING,
    medical_history STRING,
    emergency_contact STRING,
    blood_type STRING,
    allergies STRING,
    last_checkup_date STRING,
    device_id STRING,
    data_format STRING,
    PRIMARY KEY(event_id) NOT ENFORCED  -- event_id is the unique identifier
);

CREATE TABLE `healthcare_dataset.processed_blood_pressure_data` (
    event_id STRING,  
    patient_id STRING,
    systolic INT64,
    diastolic INT64,
    original_timestamp STRING,
    processed_timestamp INT64,
    age INT64,
    gender STRING,
    medical_history STRING,
    emergency_contact STRING,
    blood_type STRING,
    allergies STRING,
    last_checkup_date STRING,
    device_id STRING,
    data_format STRING,
    PRIMARY KEY(event_id) NOT ENFORCED  -- event_id is the unique identifier
);

CREATE TABLE `healthcare_dataset.processed_fall_detection_data` (
    event_id STRING,  
    patient_id STRING,
    fall_detected BOOLEAN,
    original_timestamp STRING,
    processed_timestamp INT64,
    age INT64,
    gender STRING,
    medical_history STRING,
    emergency_contact STRING,
    blood_type STRING,
    allergies STRING,
    last_checkup_date STRING,
    device_id STRING,
    data_format STRING,
    PRIMARY KEY(event_id) NOT ENFORCED  -- event_id is the unique identifier
);