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

### Step 2: Add a route to the IGW for each Public Subnet
1. Select each of the public subnets you have created, go to the Routes tab and add this route:
  - Destination: **0.0.0.0/0**
  - Target: select the ID of the Internet Gateway **IGW_PUB_DB_A19**
  ![Alt text](pics/public_subnets.png?raw=true "Public Subnets")
