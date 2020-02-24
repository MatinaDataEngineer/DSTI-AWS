# Connect to a private RDS instance over a private EC2 instance by assuming an IAM role
## Objective 
Using the private RDS MySQL instance created in the private subnet of the AWS architecture of [A19_Project2](/A19_Project2_readme.md), connect using Python, insert data and display it. (We added an optional step to use MySQL client for the same)
with 
  - DB Instance identifier: **DBMYSQLA19P2**
  -	Master username: **admin** and password: admin1234
 	-	Security Group: **SG_DB_A19P2**
 	-	Availability zone: **us-east-1a**
 	-	(Database port: 3306)
 	-	Password and IAM database authentication
connect to it over the private FI instance by assuming an IAM role with the managed policy: **AmazonRDSFullAccess** 
*(without using database username and password credentials)*
>ARN of RDS instance: arn:${Partition}:rds:${Region}:${Account}:{ResourceType}/${Resource}
e.g. "Resource": "arn:aws:rds:us-west-2:123456789012:db:dbtest"
All db instances in my account: "Resource": "arn:aws:ec2:us-east-1:123456789012:db:*"
assume-role* CLI commands.

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


### Step 3: Connect to the FI Instance (over the Jump Box)
1. We issue the following command to shh to the Bastion Server (the pem key is saved in the Downloads folder):
	```sh 
	ssh -i Downloads/"A19_Project1.pem" ec2-user@18.234.101.88
	```
1. From here, we issue the following command to ssh to the FI instance using the copied pem key in our tmp directory:
	```sh
	ssh -i tmp/"A19_Project1.pem" ec2-user@11.80.3.34
	```
  
### Step 4: Connect to the RDS using MySQL client and create a database user account to use IAM authentication
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
	Attention: the specified database account should have the same name as the IAM user or role. (here we use EC2_CONNECT_RDS) (attention, because we do not use localhost but we connect from a remote server, we put '@'%' )
	```sh
	CREATE USER 'EC2_CONNECT_RDS'@'%' IDENTIFIED WITH AWSAuthenticationPlugin as 'RDS';
	```
ATTENTION: we have moved over to step "Attach the IAM role to the EC2 instance" skipping the rest
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

4. 	  Attach your newly created IAM role **EC2_CONNECT_RDS** to the EC2 instance and click "Apply"


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
	aws rds generate-db-auth-token --hostname dbmysqla19p2.cuzs16qcrkta.us-east-1.rds.amazonaws.com --port 3306 --region us-east-1 --username EC2_CONNECT_RDS
	```
	RDS_HOST="dbmysqla19p2.cuzs16qcrkta.us-east-1.rds.amazonaws.com"
	REGION="us-east-1"
	TOKEN="$(aws rds generate-db-auth-token --hostname ${RDS_HOST} --port 3306 --region ${REGION} --username EC2_CONNECT_RDS)"
	
### Step 10: Connect to the DB using the IAM authentication token	
mysql --host=$RDSHOST --port=3306 --ssl-ca=/sample_dir/rds-combined-ca-bundle.pem --enable-cleartext-plugin --user=EC2_CONNECT_RDS --password=$TOKEN	

ERROR 2002 (HY000): Can't connect to local MySQL server through socket '/var/lib/mysql/mysql.sock' (2)

mysql --host="${RDS_HOST}" \
	    --port=3306 \
	    --user=EC2_CONNECT_RDS \
	    --ssl-ca=/home/ec2-user/ssl-aws-cert/rds-combined-ca-bundle.pem \
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
	
