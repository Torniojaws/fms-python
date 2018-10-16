CREATE DATABASE IF NOT EXISTS fms;
CREATE USER 'fmstest'@'localhost' IDENTIFIED BY 'fmstest';
GRANT ALL ON fms.* TO 'fmstest'@'localhost';
