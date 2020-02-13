# A19 Project1
## Objective 
Create an AWS Architecture, consisting of 1 VPC, 3 Instances, 1 Internet Gateway using free tier in which:
2 Instances are in the Public Subnet (one of which is the Jump Box "JB" and the other one the NAT instance "NAT") and 1 Instance "FI" is in the Private Subnet. This final instance "FI" should be able to ping google.com and receive reply.

## Architectural approach
![Alt text](/P1Diagram.png?raw=true "Diagram")

* We will use 1 Region and 1 Availability Zone within it
* There will be 1 VPC with the following IP Range: **11.80.0.0/20**, which means this VPC includes 4,096 IPs between 11.80.0.0 and 11.80.15.255
* We will attach an Internet Gateway to the VPC
* There will be 2 Subnets:
    * Public Subnet: **11.80.0.0/24** 256 IPs (5 of which are reserved and unusable) IP range between 11.80.0.0 and 11.80.0.255
    * Private Subnet: **11.80.2.0/23** IP range between 11.80.2.0 and 11.80.3.255
* There will be 3 EC2 (free-tier) instances
    * Jump Box (or Bastion) which allows incoming ssh connections and has a public IP, being the unique point of contact from outside the VPC
    * NAT instance with Public IP which allows inbound traffic from the private subnet group and outbound connections to anywhere (ICMP included)
    * FI instance within the Private Subnet which can be accessed from the Internet over the JB  with ssh (inbound rule) and all Outbound traffic to the NAT Instance

## Step-by-step Tutorial
### Step 0: Login using aws.training:
1. We sign in to awseducate.com with our student account
1. From "My Classrooms" we select the "AWS Architecture Class" and we click on the button "Go to classroom"
1. On the pop-up that appears we click "Continue"
1. We click on "AWS" Console and we open that pop-up

### Step 1: Create a VPC in 1 Region (e.g in US N.Virginia: us-east-1)
1. Select that Region from the upper right corner of AWS Management Console
2. From the Services search box click on VPC and then from the left tab click on "Your VPCs" and finally click the upper button "Create VPC"
	1. Name tag: **VPC_A19P1**
	1. IPv4 CIDR block: **11.80.0.0/20**
	1. We click on Close
	
### Step 2: Create the Public Subnet
1. Click on "Subnets" from the left tab and then on the button "Create Subnet"
	1. Name tag: **PublicSubnet1_A19P1**
	1. VPC: we select the ID for the VPC_A19P1 VPC
	1. IPv4 CIDR block: **11.80.0.0/24** 
	1. Click on Create and finally on Close (note the AZ: e.g. us-east-1a)

### Step 3: Create the Internet Gateway	attached to VPC		
1. Click on "Internet Gateways" from the left tab and then on "Create internet gateway"
	1. Name tag:  **IGW_A19P1**
	1. Click on Create
1. It is detouched.  So, click on the menu button "Actions" and click "Attach to VPC". Then we select the ID for the VPC_A19P1 VPC
	1. Click on Attach

### Step 4: Connect the Public Subnet to the IGW for outbound traffic by modifying the route table
1. From the left tab list click on Subnets, click on PublicSubnet1_A19P1, from down click on the tab "Route Table" and then click on the  link of the Route table ID"
	1. Click on the tab "Routes" and then on the button "Edit routes" and then on the button "Add route"
	1. Destination: 0.0.0.0/0 (Anywhere)
	1.Target: Internet Gateway and then we select  IGW_A19P1
1. Click on "save routes" and Close

### Step 5: Create a Route Table for internal VPC traffic
1.. Click on the left tab list on "Route Tables" and then on the button "Create route table"
	1. Name tag: **Private_Access_A19P1**
	1. VPC: select the ID for the VPC_A19P1 VPC
	1. Click on Create click on its ID
1. On the tab "Routes" would now llow only internal VPC traffic.

### Step 6: Create the Private Subnet
1. Click on "Subnets" from the left tab and then on the button "Create Subnet"
	1. Name tag: **PrivateSubnet1_A19P1**
	1. VPC: select the ID for the VPC_A19P1 VPC
	1. Select the same Availability Zone as for the Public one (e.g. us-east-1a)
	1. IPv4 CIDR block: **11.80.2.0/23** 
1. Click on Create and finally on Close
1. Click on the "Route Table" tab to see that it got associated with the same route table as the Public subnet, which we need to change.
1. Click on the tab "Subnet Associations" and then on the button "edit subnet associations" and select the PrivateSubnet1_A19P1 and then click on Save.

### Step 7: Create a Bastion instance in the Public subnet
1. From the Services menu click on EC2
2. From the left tab list click on "Instances" and then on the button "Launch Instance"
	1. Check the checkbox "Free tier only"
	1. Select the first one
	1. Choose t2.micro instance type
1. In the step "Configure Instance Details" for "Network" select the DSTI_A19P1 VPC and for "Subnet" select the PublicSubnet1_A19P1 and for "Auto-assign Public IP" select Enable
1. Click on the button "Add Storage" accept the defaults and click on the button "Add Tags"
1. Click on the button "Add Tag" and give values for Key: Name and for Value:  **JB_A19P1**
1. In the step "Configure Security Group" select "Create a new security group" and name it: **SG_JB_A19P1** and allow inbound SSH connections over TCP on port 22 from anywhere:
![Alt text](/Bastion.png?raw=true "Bastion")
1. Click on Review and Launch
1. Click on Launch
1. In the pop-up window select to Create a new key pair and name it: A19_Project1 and click on the "Download Key Pair"
1. And finally click on the button "Launch Instances"

### Step 8: Create and configure a NAT instance in the Public subnet
1. From the Services menu we click on EC2
1. From the left tab list click on "Instances" and then on the button "Launch Instance"
	1. Select Community AMIs and from the list search for **"amzn-ami-vpc-nat"** 
1. Choose t2.micro instance type
1. In the step "Configure Instance Details" for "Network" select the DSTI_A19P1 VPC and for "Subnet" select the PublicSubnet1_A19P1 and for "Auto-assign Public IP" select Enable
1. Click on the button "Add Storage" accept the defaults and click on the button "Add Tags"
1. Click on the button "Add Tag" and give values for Key: Name and for Value:  **NAT_A19P1**
1. In the step "Configure Security Group" select "Create a new security group" and name it: **SG_NAT_A19P1** and modify the existing rule to allow all traffic from the Private Subnet CIDR: 11.80.2.0/23:
![Alt text](/NAT.png?raw=true "NAT")
1. Click on Review and Launch
1. Click on Launch
1. In the pop-up window select to Choose an existing key pair: A19_Project1 and click on the checkbox
1. And finally click on the button "Launch Instances"
1. Select the NAT Instance on the Instaces list and from the Actions menu, click on Networking and then on "Change Source/Dest. Check"  and then on "Yes, Disable"
		
### Step 9: Create an instance "FI" in the Private Subnet
1. Services menu we click on EC2
1. From the left tab list click on "Instances" and then on the button "Launch Instance"
	1. Check the checkbox "Free tier only"
	1. Select the first one
1. Choose t2.micro instance type
1. In the step "Configure Instance Details" for "Network" select the DSTI_A19P1 VPC and for "Subnet" select the PrivateSubnet1_A19P1 (not having a public IP)
1. Click on the button "Add Storage" accept the defaults and click on the button "Add Tags"
1. Click on the button "Add Tag" and give values for Key: Name and for Value:  **FI_A19P1**
1. In the step "Configure Security Group" select "Create a new security group" and name it: **SG_FI_A19P1** and modify the rule allow all traffic from the JumpBox instance Security Group (by typing sg and then selecting SG_JB_A19P1 from the drop down list)
![Alt text](/FI.png?raw=true "FI")
1. Click on Review and Launch
1. Click on Launch
1. In the pop-up window select to Choose an existing key pair: A19_Project1 and click on the checkbox
1. And finally click on the button "Launch Instances"

### Step 10: Modify the Route Table of the private subnet to connect it to the NAT instance
1. Click on the left tab list on "Route Tables"
1. Select the "Private_Access_A1P1" route table and from the tab Routes click on "Edit routes"
1. Add a route from Destination: 0.0.0.0/0 to the ID of the NAT Instance and Save

### Step 11: Evaluate the Design by pinging Google.com from the "FI" instance
We need to connect to the instance FI. Based on our Architecture we can do it through the Bastion Server (JumpBox or JB), firstly we need to ssh to the Bastion Server and then from there we need to ssh to the FI Instance
1. We go to Instances, we select the JB_A19P1 and we note down its Public IP: 18.207.188.98
1. Similarly, we select the FI_A19_P1 and we note down its Private IP: 11.80.3.34
1. We open up a Terminal, we traverse to the directory that we have downloaded the key-pair file and we issue the following command to make our pem file accessible:
```sh
chmod 400 A19_Project1.pem
```
1. We issue the following command to shh to the Bastion Server (we select yes if we are aksed), we create a public directory tmp and we exit:
```sh 
ssh -i "A19_Project1.pem" ec2-user@18.207.188.98
mkdir –m777 tmp
exit
```
1. We issue the following scp command to copy our pem key over to the Bastion Server:
```sh 
scp -i "A19_Project1.pem" A19_Project1.pem ec2-user@18.207.188.98:/tmp
```
1. We issue the following command to shh again to the Bastion Server:
```sh 
ssh -i "A19_Project1.pem" ec2-user@18.207.188.98
```
1. From here, we issue the following command to ssh to the FI instance using the copied pem key in our tmp directory:
```sh
ssh -i /tmp/"A19_Project1.pem" ec2-user@11.80.3.34
```
1. From the FI instance we issue a ping command to google.com:
```sh
ping google.com
```
			
Here are the results for the validation:

![Alt text](/Results.png?raw=true "results")
			
**SUCCESS!** Issue twice the command "exit" in the terminal to close our ssh connections and stop the instances we have created in order not to incur unwanted billing.
