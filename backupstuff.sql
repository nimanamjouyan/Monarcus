-- UPDATE `2015_sa_casualty`
-- SET Age = NULL
-- WHERE Age NOT REGEXP '^-?[0-9]+$';
UPDATE `2015_sa_casualty`
SET Hospital = NULL 
WHERE Hospital LIKE '%XX%';

UPDATE `2015_sa_casualty`
SET Age = TRIM(LEADING '0' FROM Age) 
WHERE Age LIKE '0%';

-- UPDATE `2015_sa_casualty`
-- SET Hospital = NULL 
-- WHERE Hospital LIKE 'XXXXXX';