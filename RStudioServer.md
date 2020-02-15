# RStudio Server Installation on Amazon Linux 2 AMI 2.0.20191217.0 x86_64 HVM gp2
## Instructions on how to install the latest RStudio Server (1.2.5033-x86_64) on the latest Amazon Linux AMI on the free-tier

1. Create a **VPC** (or use an existing one with IPv4 CIDR Range e.g.: 10.0.1.0/24)
1. Create an **Internet Gateway** and attach it to your VPC
1. Within this VPC create a **Public Subnet** (e.g. with IPv4 CIDR Range: 10.0.1.0/28) and edit its Route Table to allow traffic from Destination 0.0.0.0/0
to your Internet Gateway
1. Launch an **Amazon Linux 2 AMI Instance** in that VPC ( t2.micro instance type)
    1. In the step "Configure Instance Details" for "Network" select the your VPC and for "Subnet" select the Public Subnet you have created and for **"Auto-assign Public IP"** select Enable
    1. In the step "Configure Security Group" select "Create a new security group", name it however you like and attach it to your VPC
    1. In the Security Group Configuration allow SSH connections over TCP on port 22 from anywhere: 0.0.0.0/0 and add another **Custom TCP Rule** to allow TCP connections on the port **8787** from  Anywhere (0.0.0.0/0) because this is the port that For RServer uses to be able to open it from anywhere in your browser
   1. (We let the Outbound rules unchanged, to allow all Traffic)
1. Connect to your instance via ssh using your key-pair and its Public IP. e.g.:
```sh
ssh -i "Matina_Test_Linux_A19_KeyPair.pem" ec2-user@3.226.30.36
```
6. Update the installed packages of your instance:
```sh
Sudo yum -y update
```
7. Install R (It is boundled in the AWS extra packages as R3.4, noting that packages from extras can be installed with the “sudo amazon-linux-extras install ” command and the R):
```sh
sudo amazon-linux-extras install R3.4
```
8. Download RStudio Server
```sh
wget https://download2.rstudio.org/server/centos6/x86_64/rstudio-server-rhel-1.2.5033-x86_64.rpm
```
9. Install RStudio Server (Useful documentation: https://support.rstudio.com/hc/en-us/articles/200552306-Getting-Started)
```sh
sudo yum install rstudio-server-rhel-1.2.5033-x86_64.rpm
```
10. Since RStdio Server requests a user login in the browser, you need to set a password for the ec2-user:
```sh
sudo su
passwd ec2-user
```
Now, you will be able to open up a browser from your PC and open the RStudio Server by giving your Instance public IP address and the port 8787, where Rserver operates: e.g.: 3.226.30.36:8787
![Alt text](pics/RServerLogin.png?raw=true "RServerLogin")

In the Login Page, provide the user: ec2-user and the password you had just set and click on Login
![Alt text](pics/RServerSuccess.png?raw=true "RServerSuccess")
