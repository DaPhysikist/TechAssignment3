CREATE DATABASE IF NOT EXISTS `TechAssignment3`;

USE `TechAssignment3`;

-- Drop existing tables if they exist (optional, use with caution)
DROP TABLE IF EXISTS sensordata;

-- Create the 'sensordata' table
CREATE TABLE IF NOT EXISTS sensordata (
  id INTEGER AUTO_INCREMENT PRIMARY KEY,
  temperature FLOAT NOT NULL,
  humidity FLOAT NOT NULL,
  light_level FLOAT NOT NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

SELECT * from sensordata;

DELETE from sensordata;