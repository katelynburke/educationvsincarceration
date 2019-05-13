-- Create and use education_v_incarceration_db

CREATE DATABASE education_v_incarceration_db;
USE education_v_incarceration_db;

delete from education; 
delete from incarceration_report; 
delete from vera_incarceration_report; 
delete from education_v_incarceration; 

CREATE TABLE incarceration_report (
  id INT AUTO_INCREMENT NOT NULL,
  STATE	VARCHAR(20),
  YEAR INT(4),
  PRISONER_COUNT INT(11),	
  STATE_POPULATION INT(11),
  VIOLENT_CRIME_TOTAL FLOAT(7, 1), 
  PROPERTY_CRIME_TOTAL FLOAT(7, 1), 
  PRIMARY KEY (id)
);

CREATE TABLE incarceration_report (
  id INT AUTO_INCREMENT NOT NULL,
  STATE	VARCHAR(20),
  YEAR INT(4),
  TOTAL_JAIL_ADM FLOAT(7, 1), 
  ASIAN_JAIL_POP INT(11),	
  BLACK_JAIL_POP DECIMAL(2, 6), 
  LATINO_JAIL_POP DECIMAL(2, 6),
  NATIVE_JAIL_POP DECIMAL(2, 6),
  WHITE_JAIL_POP DECIMAL(2, 6),
  ASIAN_PRISON_POP DECIMAL(2, 6),
  BLACK_PRISON_POP DECIMAL(2, 6),
  LATINO_PRISON_POP DECIMAL(2, 6),
  NATIVE_PRISON_POP DECIMAL(2, 6),
  OTHER_PRISON_POP DECIMAL(2, 6),
  WHITE_PRISON_POP DECIMAL(2, 6),
  PRIMARY KEY (id)
);




