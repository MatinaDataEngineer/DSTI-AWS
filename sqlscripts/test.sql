	CREATE TABLE `playgroundA19`.`test_A19` (
	  `tst_key` INT NOT NULL,
	  `tst_name` VARCHAR(45) NULL,
	  `tst_value` VARCHAR(45) NULL,
	  PRIMARY KEY (`tst_key`));
	INSERT INTO `playgroundA19`.`test_A19`
	(`tst_key`,
	`tst_name`,
	`tst_value`)
	VALUES
	(1,'cohort','A19'),
	(2,'student','Matina Lysikatou'),
	(3,'project','RDS');
	commit;
