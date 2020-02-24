# A19 Project2
## Objective 
Using the private RDS MySQL instance created in the private subnet of the AWS architecture of [A19_Project2](/A19_Project2_readme.md), connect using Python, insert data and display it. (We added an optional step to use MySQL client for the same)
with 
  - DB Instance identifier: **DBMYSQLA19P2**
  -	Master username: **admin** and password: admin1234
 	-	Security Group: **SG_DB_A19P2**
 	-	Availability zone: **us-east-1a**
 	-	(Database port: 3306)
 	-	Password and IAM database authentication
connect to it over the FI instance by assuming an IAM role with the managed policy: AmazonRDSFullAccess 
*(without using database username and password credentials)*
>ARN of RDS instance: arn:${Partition}:rds:${Region}:${Account}:{ResourceType}/${Resource}
e.g. "Resource": "arn:aws:rds:us-west-2:123456789012:db:dbtest"
All db instances in my account: "Resource": "arn:aws:ec2:us-east-1:123456789012:db:*"
assume-role* CLI commands.

### Step 1: Create an IAM role that allows Amazon RDS access

1.    Open the IAM console, and choose Roles from the navigation pane.

2.    Choose Create role, choose AWS service, and then choose EC2.

3.    For Select your use case, choose EC2, and then choose Next: Permissions.

4.    In the Filter policies drop down, select "Managed". Then, choose the **AmazonRDSFullAccess** policy.

5.    Choose Next: Review.

6.    For Role Name, enter a name for this IAM role: EC2_TO_RDS  #(e.g. RDS_Full_A19P2)

7.    Choose Create Role.
![Alt text](pics/IAM_RDS_Role.png?raw=true "Role")

### Step 2: Connect to the FI Instance (over the Jump Box)
1. We issue the following command to shh to the Bastion Server (the pem key is saved in the Downloads folder):
	```sh 
	ssh -i Downloads/"A19_Project1.pem" ec2-user@18.234.101.88
	```
1. From here, we issue the following command to ssh to the FI instance using the copied pem key in our tmp directory:
	```sh
	ssh -i /tmp/"A19_Project1.pem" ec2-user@11.80.3.34
	```
  
### Step 3: Connect to the RDS using MySQL client and create a database user account to use IAM
1. From the FI instance we install the MySQL client:
	```sh
	sudo yum update
	sudo yum install -y https://dev.mysql.com/get/mysql57-community-release-el7-11.noarch.rpm
	sudo yum install -y mysql-community-client
	mysql --version
	```
2. Using MySQL client we connect to the RDS instance using the admin user and the Endpoint URL (you need to type the password when it asks):
	```sh
	mysql -u admin -p -h dbmysqla19p2.cuzs16qcrkta.us-east-1.rds.amazonaws.com
	```
  	![Alt text](pics/mysql_client_conn.png?raw=true "MySQLClient")
3. Create a database user account that uses an AWS authentication token instead of a password:
	Attention: the specified database account should have the same name as the IAM user or role. (here we use RDS_Full_A19P2) (attention, because we do not use localhost but we connect from a remote server, we put '@'%' )
	```sh
	CREATE USER RDS_Full_A19P2 IDENTIFIED WITH AWSAuthenticationPlugin as 'RDS';
	```
4. Optionally, run this command to require the user to connect to the database using SSL:
	```sh
	ALTER USER 'RDS_Full_A19P2'@'%' REQUIRE SSL;
	GRANT ALL PRIVILEGES ON dbmysqla19p2.* to 'RDS_Full_A19P2'@'%' REQUIRE X509;
	GRANT ALL ON `%`.* TO RDS_Full_A19P2@`%`;
	FLUSH PRIVILEGES; 
  	```
	Then you just issue a FLUSH PRIVILEGES; statement to apply the changes to the running server.
	
5. Exit the MySQL connection:
	```sh
	exit
  	```

### Step 4: Add an IAM inline policy that maps the database user to the IAM role

1.    From the IAM role list, choose the newly created IAM role.

2.    From the "Permissions" tab click on "Add inline policy".

3.    Paste the following code to the JSON tab:
		Note: Be sure to edit the Resource value with the details of your database resources, such as your DB instance identifier and database user name. 
arn:aws:rds-db:region:account-id:dbuser:DbiResourceId/db-user-name
(the details for region, account-id and DbiResourceID you find from the RDS page in the Configuration tab from the ARN. for example here:
ARN: arn:aws:rds:us-east-1:298381820603:db:dbmysqla19p2
Resource id: db-V6YTLZB2Q4LNKGREUYCBNVEQDQ
Account Number:  298381820603
Region: us-east-1
the db-user-name is the database user you have created earlier : RDS_Full_A19P2
)
                
```json
{
    "Version": "2012-10-17",
    "Statement": [
       {
          "Effect": "Allow",
          "Action": [
              "rds-db:connect"
          ],
          "Resource": [
		  	  "arn:aws:rds-db:us-east-1:ç:dbuser:*/*"
          ]
       }
    ]
}

```
{
  "Version" : "2012-10-17",
  "Statement" :
  [
    {
      "Effect" : "Allow",
      "Action" : ["rds-db:connect"],
      "Resource" : ["arn:aws:rds-db:us-east-1:298381820603:dbuser:db-V6YTLZB2Q4LNKGREUYCBNVEQDQ/RDS_Full_A19P2"]
    }
  ]
}


"arn:aws:rds-db:us-east-1:298381820603:dbuser:db-V6YTLZB2Q4LNKGREUYCBNVEQDQ/db_iam_user"
aws rds describe-db-instances --query "DBInstances[*].[DBInstanceIdentifier,DbiResourceId]" --region us-east-1
                    

4.    Choose Review policy.

5.    For Name, enter a policy name (e.g. EC2_TO_RDS_POLICY)
		![Alt text](pics/IAM_RDS_Policy.png?raw=true "Policy")

6.    Choose Create policy.


### Step 7: Attach the IAM role to the EC2 instance

1.    Open the Amazon EC2 console.

2.    Choose the EC2 instance that you'll use to connect to Amazon RDS. (here we choose the FI instance of the Project1)

3.    From the Actions menu choose "Instance Settings" and "Attach/Replace IAM role" 

4. 	  Attach your newly created IAM role **RDS_Full_A19P2** to the EC2 instance and click "Apply"


### Step 8: Connect to the FI Instance (over the Jump Box) and download the SSL Certificates
1. We issue the following command to shh to the Bastion Server (the pem key is saved in the Downloads folder):
	```sh 
	ssh -i Downloads/"A19_Project1.pem" ec2-user@18.234.101.88
	```
1. From here, we issue the following command to ssh to the FI instance using the copied pem key in our tmp directory:
	```sh
	ssh -i /tmp/"A19_Project1.pem" ec2-user@11.80.3.34
	```
1. Download the RDS SSL Certificate pem file
	```sh
	mkdir ssl-cert
	chmod 777 ssl-cert
	cd ssl-cert
	wget https://s3.amazonaws.com/rds-downloads/rds-combined-ca-bundle.pem
	```

## Step 9: Install MySQL Server (the MySQL client is not enough)
sudo yum install mysql-server

### Step 9: Generate an AWS authentication token to identify the IAM role
1.  Use the following AWS CLI command to generate an authentication token. (This token expires within 15 minutes of creation)
	```sh
	aws rds generate-db-auth-token --hostname dbmysqla19p2.cuzs16qcrkta.us-east-1.rds.amazonaws.com --port 3306 --region us-east-1 --username db_iam_user
	```
	RDS_HOST="dbmysqla19p2.cuzs16qcrkta.us-east-1.rds.amazonaws.com"
	REGION="us-east-1"
	TOKEN="$(aws rds generate-db-auth-token --hostname ${RDS_HOST} --port 3306 --region ${REGION} --username RDS_Full_A19P2)"
	
### Step 10: Connect to the DB using the IAM authentication token	
	mysql --host="${RDS_HOST}" \
	      --port=3306 \
	      --user=RDS_Full_A19P2 \
	      --ssl-ca=/home/ec2-user/ssl-cert/rds-combined-ca-bundle.pem \
	      --ssl-verify-server-cert \
	      --enable-cleartext-plugin \
	      --password="$TOKEN"

mysql --host="${RDS_HOST}" \
      --port=3306 \
      --user=RDS_Full_A19P2 \
      --ssl-ca=/home/ec2-user/ssl-cert/rds-combined-ca-bundle.pem \
      --enable-cleartext-plugin \
      --password="$TOKEN"
	  
(After attaching the policy AdministratorAccess, I was able on ec2 to create the user:
aws iam create-user --user-name RDS_Full_A19P2)
aws iam list-attached-user-policies --user-name RDS_Full_A19
# I have to do everything in aws CLI (because from the console, policies are not transferred)
	  
	  
	  
	  https://aws.amazon.com/premiumsupport/knowledge-center/iam-assume-role-cli/
	  aws iam create-user --user-name RDS_Full_A19P2
	  aws iam attach-user-policy --user-name RDS_Full_A19P2 --policy-arn "arn:aws:iam::298381820603:policy/example-policy"
	  aws iam list-attached-user-policies --user-name RDS_Full_A19P2
	  aws sts assume-role --role-arn "arn:aws:iam::298381820603:role/RDS_Full_A19P2" --role-session-name AWSCLI-Session
	  https://gist.github.com/apolloclark/b3f60c1f68aa972d324b
https://aws.amazon.com/premiumsupport/knowledge-center/users-connect-rds-iam/
https://aws.amazon.com/blogs/database/use-iam-authentication-to-connect-with-sql-workbenchj-to-amazon-aurora-mysql-or-amazon-rds-for-mysql/
RDSHOST="rdsmysql.cdgmuqiadpid.us-west-2.rds.amazonaws.com"
TOKEN="$(aws rds generate-db-auth-token --hostname $RDSHOST --port 3306 --region us-west-2 --username jane_doe )"

mysql --host=$RDSHOST --port=3306 --ssl-ca=/sample_dir/rds-combined-ca-bundle.pem --enable-cleartext-plugin --user=jane_doe --password=$TOKEN	  
	  
mysql -h dbmysqla19p2.cuzs16qcrkta.us-east-1.rds.amazonaws.com --ssl-ca=rds-ca-2019-root.pem -p -u admin
	  

mysql -u RDS_Full_A19P2 -p -h dbmysqla19p2.cuzs16qcrkta.us-east-1.rds.amazonaws.com --enable-cleartext-plugin
	
2. Copy and store the authentication token for later use in an environment variable:

RDSHOST="dbmysqla19p2.cuzs16qcrkta.us-east-1.rds.amazonaws.com"
TOKEN="$(aws rds generate-db-auth-token --hostname $RDSHOST --port 3306 --region us-east-1 --username RDS_Full_A19P2)"


3. Download the SSL root certificate file or certificate bundle file
wget https://s3.amazonaws.com/rds-downloads/rds-combined-ca-bundle.pem
#wget https://s3.amazonaws.com/rds-downloads/rds-ca-2019-root.pem

### Step 10: Connect to the RDS DB instance using the IAM authentication token
mysql --host=$RDSHOST --port=3306 --ssl-ca=rds-combined-ca-bundle.pem --enable-cleartext-plugin --user=RDS_Full_A19P2

mysql --host=$RDSHOST --port=3306 --ssl-ca=rds-combined-ca-bundle.pem --enable-cleartext-plugin --user=db_iam_user --password=$TOKEN

#mysql -h dbmysqla19p2.cuzs16qcrkta.us-east-1.rds.amazonaws.com --ssl-ca=rds-combined-ca-bundle.pem --ssl-verify-server-cert
mysql -h dbmysqla19p2.cuzs16qcrkta.us-east-1.rds.amazonaws.com --ssl-ca=rds-ca-2019-root.pem -p

1. You need to change/set the master user password (if you have not already done it on the FI instance):
sudo su
passwd ec2-user
1. Login back as ec2-user
sudo ec2-user
1. After you download the certificate file, run the following commands to connect to the RDS DB instance with SSL using the MySQL client:
https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.IAMDBAuth.html
(For the -h parameter, substitute the DNS name for your DB instance. For the --ssl-ca parameter, substitute the SSL certificate file name as appropriate.)

mysql -h dbmysqla19p2.cuzs16qcrkta.us-east-1.rds.amazonaws.com --ssl-ca=rds-ca-2019-root.pem --ssl-mode=VERIFY_IDENTITY -p
mysql -h dbmysqla19p2.cuzs16qcrkta.us-east-1.rds.amazonaws.com --ssl-ca=rds-ca-2019-root.pem -p
	
	
3. We issue the following SQL commands to create data:
   	- [test.sql](sqlscripts/test.sql)
   
4. We issue the following SQL command to retrieve data:
	```sh
	Select * from playgroundA19.test_A19;
	```
  	![Alt text](pics/SQL_Results1.png?raw=true "SQLResults1")

### Step 5: Connect to the RDS using Python and perform SQL
1. Being on the FI instance connected, we install Python:
	```sh
	sudo yum install python3
	```
2. We install a second component PyMSQL we found documented here: https://docs.aws.amazon.com/lambda/latest/dg/services-rds-tutorial.html
	```sh
	sudo python3 -m pip install PyMySQL
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

