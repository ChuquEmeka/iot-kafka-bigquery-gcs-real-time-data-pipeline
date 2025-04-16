-- Create processed streams, flattening JSON and joining with metadata
CREATE STREAM processed_heart_rate_stream_with_metadata AS
SELECT 
    hr.event_id AS event_id,  
    hr.patient_id AS key_patient_id,
    CAST(hr.patient_id AS STRING) AS patient_id,
    hr.heart_rate AS heart_rate,
    hr.timestamp AS original_timestamp,
    UNIX_TIMESTAMP() AS processed_timestamp,
    pm.age,
    pm.gender,
    pm.medical_history,
    pm.emergency_contact,
    pm.blood_type,
    pm.allergies,
    pm.last_checkup_date,
    pm.device_id,
    pm.data_format
FROM heart_rate_stream hr
LEFT JOIN patient_metadata_table pm 
  ON hr.patient_id = pm.patient_id
PARTITION BY hr.patient_id
EMIT CHANGES;

CREATE STREAM processed_blood_oxygen_stream_with_metadata AS
SELECT 
    bo.event_id AS event_id,  
    bo.patient_id AS key_patient_id,
    CAST(bo.patient_id AS STRING) AS patient_id,
    bo.spo2 AS spo2,
    bo.timestamp AS original_timestamp,
    UNIX_TIMESTAMP() AS processed_timestamp,
    pm.age,
    pm.gender,
    pm.medical_history,
    pm.emergency_contact,
    pm.blood_type,
    pm.allergies,
    pm.last_checkup_date,
    pm.device_id,
    pm.data_format
FROM blood_oxygen_stream bo
LEFT JOIN patient_metadata_table pm 
  ON bo.patient_id = pm.patient_id
PARTITION BY bo.patient_id
EMIT CHANGES;

CREATE STREAM processed_blood_pressure_stream_with_metadata AS
SELECT 
    bp.event_id AS event_id,  
    bp.patient_id AS key_patient_id,
    CAST(bp.patient_id AS STRING) AS patient_id,
    bp.systolic,
    bp.diastolic,
    bp.timestamp AS original_timestamp,
    UNIX_TIMESTAMP() AS processed_timestamp,
    pm.age,
    pm.gender,
    pm.medical_history,
    pm.emergency_contact,
    pm.blood_type,
    pm.allergies,
    pm.last_checkup_date,
    pm.device_id,
    pm.data_format
FROM blood_pressure_stream bp
LEFT JOIN patient_metadata_table pm 
  ON bp.patient_id = pm.patient_id
PARTITION BY bp.patient_id
EMIT CHANGES;

CREATE STREAM processed_fall_detection_stream_with_metadata AS
SELECT 
    fd.event_id AS event_id,  
    fd.patient_id AS key_patient_id,
    CAST(fd.patient_id AS STRING) AS patient_id,
    fd.fall_detected,
    fd.timestamp AS original_timestamp,
    UNIX_TIMESTAMP() AS processed_timestamp,
    pm.age,
    pm.gender,
    pm.medical_history,
    pm.emergency_contact,
    pm.blood_type,
    pm.allergies,
    pm.last_checkup_date,
    pm.device_id,
    pm.data_format
FROM fall_detection_stream fd
LEFT JOIN patient_metadata_table pm 
  ON fd.patient_id = pm.patient_id
PARTITION BY fd.patient_id
EMIT CHANGES;