# A19 Project2
## Objective 
1. Create a public RDS MySQL-compatible Aurora cluster and connect to it using any web interface (SQL Workbench). Add data using SQL and display it.
2. Create a private RDS MySQL instance in the private subnet of the AWS architecture of Project1, connect using Python, insert Data and display it.

## Steps for Objective #1: Public MySQL-compatible Aurora cluster
##-----------------------------------------------------------------------

### Step 1: Create a VPC in 1 Region (e.g in US N.Virginia: us-east-1)



## Steps for Objective #2: Private MySQL instance
##-----------------------------------------------------------------------

### Step 1: Create and configure the MySQL RDS
1. From the Services select **RDS** and then we Select from the left **Databases**
1. Click on "Create Database" button
1. Pick "Standard Create", **MySQL**, MySQL Community, Free Tier
  -	DB Instance identifier: **DBMYSQLA19P2**
  -	Master username: **admin** and password: admin1234
  -	Connectivity: Select the **VPC_A19P1**
  -	Create new DB Subnet Group, Not Publicly accessible
  -	Create new Security Group: **SG_DB_A19P2**
  -	Availability zone: **us-east-1a**
  -	(Database port: 3306)
  -	Password and IAM database authentication
  -	Initial database name: **playgroundA19**
  -	Backup retention period: 1 day
4. Click on the button "Create Database"
5. You get the Error: "DB Subnet Group doesn't meet availability zone coverage requirement. Please add subnets to cover at least 2 availability zones." 
  1. Open new tab, go to VPC service and Subnets
	2. Create a new Subnet
	  - Name tag: **Private_Subnet_SlaveDB**
	  - VPC: **VPC_A19P1**
	  - AZ: choose a different AZ: **us-east-1b**
    - CIDR: **11.80.4.0/23**
6. Now go back to the previous tab with the error message and click again the button "Create Database"
![Alt text](pics/DB1.png?raw=true "DB1")

### Step 2: Add a route to the MySQL RDS from the FI Instance
1. Change the Inbound rules of the DB Security Group by adding the rule:
- Type: MYSQL/Aurora, TCP, 3306 from the Security Group of the FI instance:
![Alt text](pics/SG_Change.png?raw=true "SG")

### Step 3: Connect to the FI Instance (over the Jump Box)
1. We issue the following command to shh to the Bastion Server (the pem key is saved in the Downloads folder):
	```sh 
	ssh -i Downloads/"A19_Project1.pem" ec2-user@18.234.101.88
	```
1. From here, we issue the following command to ssh to the FI instance using the copied pem key in our tmp directory:
	```sh
	ssh -i /tmp/"A19_Project1.pem" ec2-user@11.80.3.34
	```
  
### Step 4: Connect to the RDS using MySQL client and perform SQL
1. From the FI instance we install the MySQL client:
	```sh
	sudo yum update
	sudo yum install -y https://dev.mysql.com/get/mysql57-community-release-el7-11.noarch.rpm
	sudo yum install -y mysql-community-client
	Mysql --version
	mysql -u admin -p -h dbmysqla19p2.cuzs16qcrkta.us-east-1.rds.amazonaws.com
	```
2. Using MySQL client we connect to the RDS instance using the admin user and the Endpoint URL (you need to type the password when it asks):
	```sh
	mysql -u admin -p -h dbmysqla19p2.cuzs16qcrkta.us-east-1.rds.amazonaws.com
	```
  ![Alt text](pics/mysql_client_conn.png?raw=true "MySQLClient")
  
3. We issue the following SQL commands to create data:
   - [sql_test.sql](sqlscripts/sql_test.py)
   
4. We issue the following SQL command to retrieve data:
	```sh
	Select * from playgroundA19.test_A19;
	```
  ![Alt text](pics/SQL_Resuls1.png?raw=true "SQLResults1")

### Step 5: Connect to the RDS using Python and perform SQL
1. Being on the FI instance connected, we install Python:
	```sh
		sudo yum install python3
	```
2. We install a second component PyMSQL we found documented here: https://docs.aws.amazon.com/lambda/latest/dg/services-rds-tutorial.html
	```sh
		Sudo python3 -m pip install PyMySQL
	```
3. We create a folder for our python scripts and we save these 2 python scripts
  - [A19test.py](pythonscripts/A19test.py)  (make sure to use your own SQL)
  - [rds_config.py](pythonscripts/rds_config.py) (make sure to use your own connection credencials)
  ```sh
	mkdir pythonscripts
	chmod 777 pythonscripts/
	cd pythonscripts
	vim A19test.py
  vim rds_config.py
	```
  ![Alt text](pics/python_results.png?raw=true "SQLResults1")
