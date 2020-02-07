# A19 Project1
## Objective 
Create an AWS Architecture, consisting of 1 VPC, 3 Instances, 1 Internet Gateway using free tier in which:
1. 2 Instances are in the Public Subnet (one of which is the Jump Box "JB" and the other one the NAT instance "NAT") and 1 Instance "FI" is in the Private Subnet

## Architectural approach
* We will use 1 Region and 1 Availability Zone within it
* There will be 1 VPC with the following IP Range: 14.80.0.0/20, which means this VPC includes 4,096 IPs between 14.80.0.0 and 14.80.15.255
* We will attach an Internet Gateway to the VPC
* There will be 2 Subnets:
    * Public Subnet: 14.80.0.0/24 256 IPs (5 of which are reserved and unusable) IP range between 14.80.0.0 and 14.80.0.255
    * Private Subnet: 4.80.2.0/23 IP range between 14.80.2.0 and 14.80.3.255
* There will be 3 EC2 (free-tier) instances
    * Jump Box (or Bastion) which allows incoming ssh connections and has a public IP, being the unique point of contact from outside the VPC
    * NAT instance which allows outbound connections to the IGW and inbound connections from the Private Subnet
    * FI instance within the Private Subnet which can be accessed from the Internet over the JB and then from JB to FI with SGs and which can initiate Outbound traffic to NAT Instance and then to IGW to be able to ping addresses

## Step-by-step Tutorial
### Step 0: Login using aws.training:
1. We sign in to awseducate.com with our student account
1. From "My Classrooms" we select the "AWS Architecture Class" and we click on the button "Go to classroom"
1. On the pop-up that appears we click "Continue"
1. We click on "AWS" Console and we open that pop-up

### Step 1: create a VPC in 1 Region (e.g in US N.Virginia: us-east-1)
1. Select that Region from the upper right corner of AWS Management Console
2. From the Services search box click on VPC and then from the left tab click on "Your VPCs" and finally click the upper button "Create VPC"
	i. Name tag: DSTI_A19_Project1
    ii. IPv4 CIDR block: 14.80.0.0/20, which means this VPC includes 4,096 IPs between 14.80.0.0 and 14.80.15.255
	iii. We click on Close
### Step 2: create the Public Subnet
1. Click on "Subnets" from the left tab and then on the button "Create Subnet"
    i. Name tag: PublicSubnet1_A19_P1
	ii. VPC: we select the ID for the DSTI_A19_Project1 VPC
	iii. IPv4 CIDR block: 14.80.0.0/24 256 IPs (5 of which are reserved and unusable) IP range between 14.80.0.0 and 14.80.0.255
	iv. We click on Create and finally on Close

### Step 3: create the Internet Gateway	attached to VPC		
1. We click on "Internet Gateways" from the left tab and then on "Create internet gateway"
i. Name tag:  IGW_A19_P1
ii. Click on Create
1. It is detouched.  So, click on the menu button "Actions" and click "Attach to VPC". Then we select the ID for the DSTI_A19_Project1 VPC
i. Click on Attach

### Step 4: Connect the Public Subnet to the IGW for outbound traffic by modifying the route table
1. From the left tab list click on Subnets, click on PublicSubnet1_A19_P1, from down click on the tab "Route Table" and then click on the  link of the Route table ID"
1. click on the tab "Routes" and then on the button "Edit routes" and then on the button "Add route"
i. Destination: 0.0.0.0/0 (Anywhere)
ii. Target: Internet Gateway and then we select  IGW_A19_P1
1. Click on "save routes" and Close

### Step 5: Create the Private Subnet
1. We click on "Subnets" from the left tab and then on the button "Create Subnet"
i. Name tag: PrivateSubnet1_A19_P1
ii. VPC: select the ID for the DSTI_A19_Project1 VPC
iii. IPv4 CIDR block: 14.80.2.0/23 IP range between 14.800.2.0 and 14.80.3.255
1. Click on Create and finally on Close
1. Click on the "Route Table" tab to see that it got associated with the same route table as the Public subnet, which we need to change.
1. Click on the left tab list on "Route Tables" and then on the button "Create route table"
i. Name tag: Private_Access_A19_Project1
ii. VPC: select the ID for the DSTI_A19_Project1 VPC
iii. Click on Create and Close
1. Select it and click on the tab "Routes" which should allow only internal VPC traffic:
1. Click on the tab "Subnet Associations" and then on the button "edit subnet associations" and select the PrivateSubnet1_A19_P1 and then click on Save.

### Step 6: Create a Bastion instance in the Public subnet
1. From the Services menu click on EC2
2. From the left tab list click on "Instances" and then on the button "Launch Instance"
i. Check the checkbox "Free tier only"
ii. Select the first one
iii. Choose t2.micro instance type
1. In the step "Configure Instance Details" for "Network" select the DSTI_A19_Project1 VPC and for "Subnet" select the PublicSubnet1_A19_P1 and for "Auto-assign Public IP" select Enable
1.  Click on the button "Add Storage" accept the defaults and click on the button "Add Tags"
1. Click on the button "Add Tag" and give values for Key: Name and for Value:  JB_A19_P1
1. In the step "Configure Security Group" select "Create a new security group" and name it: SSH_SG_A19_P1 and allow SSH connections over TCP on port 22 from anywhere:
1. Click on Review and Launch
1. Click on Launch
1. In the pop-up window select to Create a new key pair and name it: A19_Project1 and click on the "Download Key Pair"
1. And finally click on the button "Launch Instances"
i. Note this Bastion instance ID: i-060f0d75920f0e8d8

### Step 7: Create a NAT instance in the Public subnet
1. From the Services menu we click on EC2
1. From the left tab list click on "Instances" and then on the button "Launch Instance"
i. Check the checkbox "Free tier only"
ii. Select the first one
1. Choose t2.micro instance type
1. In the step "Configure Instance Details" for "Network" select the DSTI_A19_Project1 VPC and for "Subnet" select the PublicSubnet1_A19_P1
1. Click on the button "Add Storage" accept the defaults and click on the button "Add Tags"
1. Click on the button "Add Tag" and give values for Key: Name and for Value:  NAT_A19_P1
1. In the step "Configure Security Group" select "Create a new security group" and name it: PING_SG_A19_P1 and allow ICMTP traffic from anywhere:
1.Click on Review and Launch
1. Click on Launch
1. In the pop-up window select to Choose an existing key pair: A19_Project1 and click on the checkbox
1. And finally click on the button "Launch Instances"
i. Note this NAT instance ID: i-0e1c24a2937b8a993 
		
### Step 8: Create an instance "FI" in the Private Subnet
1. Services menu we click on EC2
1. From the left tab list click on "Instances" and then on the button "Launch Instance"
i. Check the checkbox "Free tier only"
ii. Select the first one
1. Choose t2.micro instance type
1. In the step "Configure Instance Details" for "Network" select the DSTI_A19_Project1 VPC and for "Subnet" select the PrivateSubnet1_A19_P1
1. Click on the button "Add Storage" accept the defaults and click on the button "Add Tags"
1. Click on the button "Add Tag" and give values for Key: Name and for Value:  FI_A19_P1
1. In the step "Configure Security Group" select "Create a new security group" and name it: PING_SG_A19_P1 and allow All traffic from within our VPC CIDR range:14.80.0.0/20
1. Click on Review and Launch
1. Click on Launch
1. In the pop-up window select to Choose an existing key pair: A19_Project1 and click on the checkbox
1. And finally click on the button "Launch Instances"
		xiv. Note this NAT instance ID: i-0e1c24a2937b8a993 

### Step 8: Evaluate the Design by pinging Google.com from the "FI" instance
We need to connect to the instance FI. Based on our Architecture we can do it through the Bastion Server, firstly we need to ssh to the Bastion Server and then from there we need to ssh to the FI Instance
1. We go to Instances, we select the JB_A19_P1 and we note down ist Public IP: 54.146.87.81
1. Similarly, we select the FI_A19_P1 and we note down ist Private IP: 14.80.2.213
1. We open up a Terminal, we traverse to the directory that we have downloaded the key-pair file and we issue the following command to make our pem file accessible:
```sh
chmod 400 A19_Project1.pem
```
1. We issue the following command to shh to the Bastion Server (we select yes if we are aksed):
```sh 
ssh -i "A19_Project1.pem" ec2-user@54.146.87.81
```
1. From here, we issue
```sh
ssh -i "A19_Project1.pem" ec2-user@14.80.2.213
```
1. From the FI instance we issue a ping command to google.com:
```sh
Ping google.com
```
			
Here are the results for the validation:
			
SUCCESS!
We issue twice the command "exit" in the terminal to close our ssh connections.
We now stop the instances we have created in order not to incur unwanted billing.
