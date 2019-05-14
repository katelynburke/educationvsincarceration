-- Create and use education_v_incarceration_db
DROP DATABASE IF EXISTS ed_prison_db;
CREATE DATABASE ed_prison_db;

USE ed_prison_db;

DROP TABLE if exists education_v_incarceration;

CREATE TABLE education_v_incarceration (
    STATE VARCHAR(20),
    YEAR INT(4),
    TOTAL_EXPENDITURE VARCHAR(20),
    INSTRUCTION_EXPENDITURE VARCHAR(20),
    4TH_ENROLLED VARCHAR(20),
    8TH_ENROLLED VARCHAR(20),
    TOTAL_ENROLLMENT VARCHAR(20),
    PRISONER_COUNT VARCHAR(20),
	STATE_POPULATION VARCHAR(20),
	VIOLENT_CRIME_TOTAL VARCHAR(20),
    PROPERTY_CRIME_TOTAL VARCHAR(20)
);

-- Create and use education_v_incarceration_db
Drop Database if exists  education_v_incarceration_db;
CREATE DATABASE education_v_incarceration_db;
USE education_v_incarceration_db;

DROP TABLE if exists full_report;

CREATE TABLE full_report (
    STATE VARCHAR(20),
    YEAR INT(4),
    TOTAL_EXPENDITURE varchar(20),
    INSTRUCTION_EXPENDITURE varchar(20),
    4TH_ENROLLED varchar(20),
    8TH_ENROLLED varchar(20),
    TOTAL_ENROLLMENT varchar(20),
    4_AVG_MATH_SCORE varchar(20),
    8_AVG_MATH_SCORE varchar(20),
    4_AVG_RDG_SCORE varchar(20),
    8_AVG_RDG_SCORE varchar(20),
	PRISONER_COUNT varchar(20),
    STATE_POPULATION varchar(20),
    VIOLENT_CRIME_TOTAL varchar(20),
    PROPERTY_CRIME_TOTAL varchar(20),
	TOTAL_JAIL_ADM varchar(20),
    ASIAN_JAIL_POP  varchar(20),
    BLACK_JAIL_POP  varchar(20),
    LATINO_JAIL_POP  varchar(20),
    NATIVE_JAIL_POP  varchar(20),
    WHITE_JAIL_POP  varchar(20),
    ASIAN_PRISON_POP  varchar(20),
    BLACK_PRISON_POP varchar(20),
    LATINO_PRISON_POP  varchar(20),
    NATIVE_PRISON_POP varchar(20),
    OTHER_PRISON_POP varchar(20),
    WHITE_PRISON_POP varchar(20)
);

