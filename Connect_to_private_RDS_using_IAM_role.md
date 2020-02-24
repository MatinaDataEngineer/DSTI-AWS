# Connect to a private RDS instance over a private EC2 instance by assuming an IAM role
## Objective 
Using the private RDS MySQL instance created in the private subnet of the AWS architecture of [A19_Project2](/A19_Project2_readme.md), connect using Python, insert data and display it. (We added an optional step to use MySQL client for the same)
with 
  - DB Instance identifier: **DBMYSQLA19**
  - Version: MySQL 5.7.17 t2.medium (I have also tried with Free tier)
  -	Master username: **admin** and password: admin1234
  	- Connectivity: VPC_A19P1 (from Project1)
 	-	Security Group: **SG_DB_A19**
 	-	Availability zone: **us-east-1a**
 	-	(Database port: 3306)
 	-	Password and IAM database authentication
connect to it over the private FI instance by assuming an IAM role with the managed policy: **AmazonRDSFullAccess** 
*(without using database username and password credentials)*
>ARN of RDS instance: arn:${Partition}:rds:${Region}:${Account}:{ResourceType}/${Resource}

### Step 1: Create a managed policy for full RDS access over IAM Authentication
1. Open the IAM console, and choose Policies from the navigation panel.
2. Click on "Create policy"
3. Click on "Import managed policy"
4. Type and select AmazonRDSFullAccess and click on "Import"
5. Under the "IAM" part click on "Add additional permissions", for "Service" type and select "RDS IAM Authentication" and configure it like this:
	![Alt text](pics/RDSIAMAuthentication.png?raw=true "RDSIAMAuthentication")
	
   and for any db-user:
   	![Alt text](pics/RDSIAMAuthentication2.png?raw=true "RDSIAMAuthentication2")
	
6. Click on "Review policy" and give it a Name: **FULL_RDS_ACCESS_OVER_IAM_AUTH**
7. Click on "Create policy"

### Step 2: Create an EC2 IAM role that allows Amazon RDS access

1.    Open the IAM console, and choose Roles from the navigation panel

2.    Choose "Create role", choose AWS service, and then choose EC2

3.    For Select your use case, choose EC2, and then choose "Next: Permissions"

4.    In the "Filter policies" drop down, select **FULL_RDS_ACCESS_OVER_IAM_AUTH** policy by checking the checkbox left of it and click on "Next: Tags" and then on "Next: Review"

5.    For Role Name, enter a name for this IAM role: **EC2_CONNECT_RDS**

6.    For Role Description enter: Allows EC2 instances to connect and to manage any RDS instance in your account.

7.    Choose "Create Role".

### Step 3: Modify the DB Security Group to allow inbound MySQL access from the FI instance
1. Select EC2 Service and from the panel click on Security Groups
1. Select the "SG_DB_A19" and add an inbound rule to allow MySQL traffic from the FI instance security group.

### Step 4: Connect to the FI Instance (over the Jump Box)
1. We issue the following command to shh to the Bastion Server (the pem key is saved in the Downloads folder):
	```sh 
	ssh -i Downloads/"A19_Project1.pem" ec2-user@18.234.101.88
	```
1. From here, we issue the following command to ssh to the FI instance using the copied pem key in our tmp directory:
	```sh
	ssh -i tmp/"A19_Project1.pem" ec2-user@11.80.3.34
	```
  
### Step 5: Connect to the RDS using MySQL client and create a database user account to use IAM authentication
1. From the FI instance we install the MySQL client:
	```sh
	sudo yum update
	sudo yum install -y https://dev.mysql.com/get/mysql57-community-release-el7-11.noarch.rpm
	sudo yum install -y mysql-community-client
	# yum install curl mysql -y
	mysql --version
	```
	# and start some necessary services
	#sudo service mysqld start
	#sudo chkconfig mysqld on
	
2. Using MySQL client we connect to the RDS instance using the admin user and the Endpoint URL (you need to type the password when it asks):
	```sh
	# for host use the Endpoint from the Connectivity & Security tab of RDS
	RDS_HOST="dbmysqla19.cuzs16qcrkta.us-east-1.rds.amazonaws.com"
	mysql -u admin -p -h ${RDS_HOST}
	```
  	![Alt text](pics/mysql_client_conn.png?raw=true "MySQLClient")
	
3. Create a database user account that uses an AWS authentication token instead of a password:
	Attention: the specified database account should have the same name as the IAM user or role. (here we use EC2_CONNECT_RDS) (attention, because we do not use localhost but we connect from a remote server, we put '@'%' )
	```sh
	CREATE USER 'EC2_CONNECT_RDS'@'%' IDENTIFIED WITH AWSAuthenticationPlugin as 'RDS';
	ALTER USER 'EC2_CONNECT_RDS'@'%' REQUIRE SSL;
	FLUSH PRIVILEGES;
	```
5. Exit the MySQL connection:
	```sh
	exit
  	```
	
### Step 6: Add an IAM inline policy that maps the database user to the IAM role

1.    From the IAM role list, choose the newly created IAM role.

2.    From the "Permissions" tab click on "Add inline policy".

3.    Paste the following code to the JSON tab:
Note: Be sure to edit the Resource value with the details of your database resources, such as your DB instance identifier and database user name. 
```json
{
  "Version" : "2012-10-17",
  "Statement" :
  [
    {
      "Effect" : "Allow",
      "Action" : ["rds-db:connect"],
      "Resource" : ["arn:aws:rds-db:us-east-1:298381820603:dbuser:db-S2V7RS2HWS5MPQEXCCYTPP5CPE/EC2_CONNECT_RDS"]
    }
  ]
}
```             

### Step 7: Attach the IAM role to the EC2 instance

1.    Open the Amazon EC2 console.

2.    Choose the EC2 instance that you'll use to connect to Amazon RDS. (here we choose the FI instance of the Project1)

3.    From the Actions menu choose "Instance Settings" and "Attach/Replace IAM role" 

4.    Attach your newly created IAM role **EC2_CONNECT_RDS** to the EC2 instance and click "Apply"


### Step 8: Connect to the FI Instance (over the Jump Box) and download the SSL Certificates
1. We issue the following command to shh to the Bastion Server (the pem key is saved in the Downloads folder):
	```sh 
	ssh -i Downloads/"A19_Project1.pem" ec2-user@18.234.101.88
	```
1. From here, we issue the following command to ssh to the FI instance using the copied pem key in our tmp directory:
	```sh
	ssh -i tmp/"A19_Project1.pem" ec2-user@11.80.3.34
	```
1. Download the RDS SSL Certificate pem file
	```sh
	mkdir ssl-aws-cert
	cd ssl-aws-cert
	wget https://s3.amazonaws.com/rds-downloads/rds-combined-ca-bundle.pem
	```


### Step 9: Generate an AWS authentication token to identify the IAM role
1.  Use the following AWS CLI command to generate an authentication token. (This token expires within 15 minutes of creation)
	```sh
	RDS_HOST="dbmysqla19.cuzs16qcrkta.us-east-1.rds.amazonaws.com"
	REGION="us-east-1"
	TOKEN="$(aws rds generate-db-auth-token --hostname ${RDS_HOST} --port 3306 --region ${REGION} --username EC2_CONNECT_RDS)"
	```

### Step 10: Connect to the DB using the IAM authentication token	
```sh
mysql --host="${RDS_HOST}" --port=3306 --ssl-ca=/home/ec2-user/ssl-aws-cert/rds-combined-ca-bundle.pem --ssl-mode=VERIFY_IDENTITY --enable-cleartext-plugin --user=EC2_CONNECT_RDS --password="$TOKEN"
```

ERROR 1045 (28000): Access denied for user 'EC2_CONNECT_RDS'@'11.80.3.34' (using password: YES)

