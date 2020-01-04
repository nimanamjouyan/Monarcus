DROP DATABASE IF EXISTS `year_2015`;
CREATE DATABASE `year_2015`; 
USE year_2015;

CREATE TABLE `2015_sa_casualty`  (
	`Casualty_id` INT NOT NULL AUTO_INCREMENT,
    `Report_id` VARCHAR(50) NOT NULL,
    `Und_Unit_Number` VARCHAR(50) NULL,
    `Casualty_Number` VARCHAR(50) NULL,
    `Casualty_Type` VARCHAR(50) NULL,
    `Sex` VARCHAR(50) NULL,
    `Age` VARCHAR(50) NULL,
    `Position_In_Veh` VARCHAR(50) NULL,
    `Thrown_Out` VARCHAR(50) NULL,
    `Injury_Extent` VARCHAR(50) NULL,
    `Seatbelt` VARCHAR(50) NULL,
    `Helmet` VARCHAR(50) NULL,
    `Hospital` VARCHAR(50) NULL,
    
    PRIMARY KEY (`Casualty_id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


delimiter $$
CREATE TRIGGER remover BEFORE INSERT ON 2015_sa_casualty
	FOR EACH ROW
		BEGIN
			IF NEW.Hospital LIKE '%XX%' OR NEW.Hospital = '' THEN
				SET NEW.Hospital = NULL;
			END IF;
		END; $$
delimiter ;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/road-crash-data-2015/2015_DATA_SA_Casualty.csv' 
INTO TABLE `2015_sa_casualty`
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(`Report_id`, `Und_Unit_Number`, `Casualty_Number`, `Casualty_Type`, `Sex`, `Age`, `Position_In_Veh`, `Thrown_Out`, `Injury_Extent`, `Seatbelt`, `Helmet`, `Hospital`);


CREATE TABLE `2015_sa_crash`  (
	`Crash_id` INT NOT NULL AUTO_INCREMENT,
    `Report_id` VARCHAR(50) NOT NULL,
    `State_Area` VARCHAR(50) NULL,
    `Suburb` VARCHAR(50) NULL,
    `Postcode` VARCHAR(50) NULL,
    `LGA_name` VARCHAR(50) NULL,
    `Total_units` VARCHAR(50) NULL,
    `Total_cas` VARCHAR(50) NULL,
    `Total_fats` VARCHAR(50) NULL,
    `Total_SI` VARCHAR(50) NULL,
    `Total MI` VARCHAR(50) NULL,
    `Year` VARCHAR(50) NULL,
    `Month` VARCHAR(50) NULL,
    `Day` VARCHAR(50) NULL,
    `Time` VARCHAR(50) NULL,
    `Area_speed` VARCHAR(50) NULL,
    `Position_type` VARCHAR(50) NULL,
    `Horizontal_align` VARCHAR(50) NULL,
    `Vertical_align` VARCHAR(50) NULL,
    `Other_feat` VARCHAR(50) NULL,
    `Road_surface` VARCHAR(50) NULL,
    `Moisture_cond` VARCHAR(50) NULL,
    `Weather_cond` VARCHAR(50) NULL,
    `DayNight` VARCHAR(50) NULL,
    `Crash_type` VARCHAR(50) NULL,
    `Unit_resp` VARCHAR(50) NULL,
    `Entity_code` VARCHAR(50) NULL,
    `CSEF_severity` VARCHAR(50) NULL,
    `Traffic_ctrls` VARCHAR(50) NULL,
    `DUI_involved` VARCHAR(50) NULL,
    `Drugs_involved` VARCHAR(50) NULL,
    `ACCLOC_X` VARCHAR(50) NULL,
    `ACCLOC_Y` VARCHAR(50) NULL,
    `UNIQUE_LOC` VARCHAR(50) NULL,
    
    PRIMARY KEY (`Crash_id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/road-crash-data-2015/2015_DATA_SA_Crash.csv' 
INTO TABLE `2015_sa_crash`
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(`Report_id`,`State_Area`,`Suburb`,`Postcode`,
    `LGA_name`,`Total_units`,`Total_cas`,`Total_fats`,
    `Total_SI`,`Total MI`,`Year`,`Month`,
    `Day`,`Time`,`Area_speed`,`Position_type`,
    `Horizontal_align`,`Vertical_align`,`Other_feat`,`Road_surface`,
    `Moisture_cond`,`Weather_cond`,`DayNight`,`Crash_type`,
    `Unit_resp`,`Entity_code`,`CSEF_severity`,`Traffic_ctrls`,
    `DUI_involved`,`Drugs_involved`,`ACCLOC_X`,`ACCLOC_Y`,
    `UNIQUE_LOC`);
    

CREATE TABLE `2015_sa_units`  (
	`Unit_id` INT NOT NULL AUTO_INCREMENT,
    `Report_id` VARCHAR(50) NOT NULL,
    `Unit_No` VARCHAR(50) NULL,
    `No_of_cas` VARCHAR(50) NULL,
    `Veh_reg_state` VARCHAR(50) NULL,
    `Unit_type` VARCHAR(50) NULL,
    `Veh_year` VARCHAR(50) NULL,
    `Direction_of_travel` VARCHAR(50) NULL,
    `Sex` VARCHAR(50) NULL,
    `Age` VARCHAR(50) NULL,
    `Lic_state` VARCHAR(50) NULL,
    `Licence_class` VARCHAR(50) NULL,
    `Licence_type` VARCHAR(50) NULL,
    `Towing` VARCHAR(50) NULL,
    `Unit_movement` VARCHAR(50) NULL,
    `Number_occupants` VARCHAR(50) NULL,
    `Postcode` VARCHAR(50) NULL,
    `Rollover` VARCHAR(50) NULL,
    `Fire` VARCHAR(50) NULL,
    
    PRIMARY KEY (`Unit_id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/road-crash-data-2015/2015_DATA_SA_Units.csv' 
INTO TABLE `2015_sa_units`
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(`Report_id`,`Unit_No`,`No_of_cas`,
    `Veh_reg_state`,`Unit_type`,`Veh_year`,
    `Direction_of_travel`,`Sex`,`Age`,
    `Lic_state`,`Licence_class`,`Licence_type`,
    `Towing`,`Unit_movement`,`Number_occupants`,
    `Postcode`,`Rollover`,`Fire`);
