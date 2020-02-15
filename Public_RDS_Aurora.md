# Setting up a Public RDS instance of MySQL-compatible Aurora cluster

## Objective 
Create a public RDS MySQL-compatible Aurora cluster and connect to it using any web interface (SQL Workbench).
Add data using SQL and display it.

### Step 1: Create a new VPC with 2 Public Subnets (in 2 different AZs)
1. Go to the VPC service and create a VPC:
    - Name: **VPC_DB_A19**
    - CIDR range: **15.50.0.0/16**
1. From the Subnets screen create the first Public Subnet:
    - Name: **Public_Subnet1_DB_A19**
    - CIDR range: **15.50.1.0/24**
    - AZ: **us-east-1e**
1. From the Subnets screen create the second Public Subnet:
    - Name: **Public_Subnet2_DB_A19**
    - CIDR range: **15.50.2.0/24**
    - AZ: **us-east-1f**
 
### Step 2: Create a new Internet Gateway and attach it to your VPC
1. Go to the Internet Gateways screen and click on the create
    - Name: **IGW_PUB_DB_A19**
1. It is detached. Select it and attach it to the **VPC_DB_A19**

### Step 3: Add a route to the IGW for each Public Subnet
1. Select each of the public subnets you have created, go to the Routes tab and add this route:
    - Destination: **0.0.0.0/0**
    - Target: select the ID of the Internet Gateway **IGW_PUB_DB_A19**
    ![Alt text](pics/public_subnets.png?raw=true "Public Subnets")

### Step 4: Prepare the VPC DNS
1. Select the VPC **VPC_DB_A19** and from the Actions menu, select "Edit DNS resolution", enable
1. Select the VPC **VPC_DB_A19** and from the Actions menu, select "Edit DNS hostnames", enable

### Step 5: Create and configure the Amazon Aurora RDS
1. From the Services select **RDS** and then we Select from the left **Databases**
1. Click on "Create Database" button
1. Pick "Standard Create", **Amazon Aurora with MySQL compatibility**
  - Regional 
  - Choose **Parallel Query** (one writer and multiple readers)
  - DB CLUSTER identifier: **DBPUBMYSQLA19P2**
  	  -	Master username: **admin** and password: admin1234
 	-	Connectivity: Select the **VPC_DB_A19**
 	-	Create new DB Subnet Group, **Publicly accessible**
 	-	Create new Security Group: **SG_DB_Public_A19**
 	-	Availability zone: **us-east-1a**
 	-	(Database port: 3306)
 	-	Password authentication
  - DB Instance identifier: **DBPUBMYSQLA19P2-1**
 	-	Initial database name: **playgroundA19**
 	-	Backup retention period: 1 day
1. Disable deletion protection and Click on the button "Create Database"
