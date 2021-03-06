# MNIST Web Application
## Objective: Training a model on MNIST and consuming it in a Web page

- [Setup the networking environment](#STEP0)
1. [Install Jupiter on a **public** EC2 instance (**Dev**) and train the Neural Network model (this instance then terminates)](#STEP1)
2. [Save the model and deploy it on the Application Server (**Backend**) which is a **private** Ubuntu EC2 Instance](#STEP2)
3. [Serve it as a web app on a Web Server (**Frontend**) in a **public** EC2 instance](#STEP3)

>*Leo's GitHub is used to provide us with the deployment files:
>https://github.com/leodsti/AWS_Tutorials/tree/master/MNIST*

>*The dataset we will use it is called MNIST and is to be found here: http://yann.lecun.com/exdb/mnist/
>It contains 60k examples of handwritten numbers.
>Use case: write a number from 0 to 9. Using computer vision can it be recognized?
>The web page should allow the user to draw a number.
>Real use case: it has been used in american post office to recognize zip codes.*


### Step 0: Setup your Networking Environment in AWS consisting of 1 VPC, 2 Subnets, 1 IGW, 1 NAT <a name="STEP0"></a>
  We will reuse the Networking Environment of [A19_Project1](/A19_Project1_Readme.md), consisting of 1 VPC, 2 Subnets, 1 IGW, 1 Bastion Server, 1 NAT instance and extend it

### Step 1: Install Jupiter on a **public** EC2 instance (**Dev**) and train the Neural Network model <a name="STEP1"></a> 
*(normally must be done on a GPU machine) We will use keras and tensaflow. After training the model, you shut it down.*
1. Launch a public EC2 Instance
	1. Go to EC2 Service, to Instances screen and click on "Launch Instance" button
	2. Select **Amazon Linux 2 AMI (HVM), SSD Volume Type**
	3. Instance Type: use free tier t2.micro (we will upgrade it later, before training the model)
	4. VPC: **VPC_A19P1**
	5. Subnet: **PublicSubnet1_A19P1**
	6. Auto-assign IP: **enable**(because we will shut it down after training)
	7. Storage: **16 GB**
	8. Tag: Name **AI_Dev**
	9. New Security Group: **SG_AI_Dev** with 2 Inbound rules:
		1. SSH to port 22 from MyIP
		2. Custom TCP to port range 8888-8898 from Anywhere (for Jupyter)
	10. Click on Launch Instance (using an existing key pair e.g. A19_Project1.pem)
2. Install on it Anaconda 
	1. Connect with ssh to your instance
		```sh 
		ssh -i Downloads/"A19_Project1.pem" ec2-user@18.205.163.6
		```
	2. Update OS packages
		```sh 
		sudo yum update -y 
		```
	3. install Anaconda distribution for Linux (https://www.anaconda.com/distribution/) (copy link address and paste it to wget)
		```sh 
		wget  https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh
		bash Anaconda3-2019.10-Linux-x86_64.sh
		```
	![Alt text](pics/InstallingAnaconda.png?raw=true "InstallingAnaconda")
	
	4. Check Anaconda
		```sh
		conda init # if command not found, reconnect with ssh to the instance
		```
		
		*(another solution is to re-install it issuing bash Anaconda3-2019.10-Linux-x86_64.sh -u)*
		IF there is no disk space left, from the AWS console, you can select the EBS volume and from the Actions menu you can select "Modify volume" and set another size. Then you need to ssh to the server and issue:
			```sh
			lsblk
			sudo growpart /dev/xvda 1
			df -h
			sudo yum install xfsprogs
			sudo xfs_growfs -d /dev/xvda1
			```
3. Install and configure Jupyter Notebook
	1. install and run Jupyter Notebook *(after installing Python3 and pip3)*
		
		```sh
		sudo yum update -y  #update os packages
		sudo yum install python3-pip -y
		sudo pip3 install jupyter
		nohup jupyter notebook --ip=0.0.0.0 &
		less nohup.out
		```
	![Alt text](pics/JupiterNotebookLaunch.png?raw=true "JupiterNotebookLaunch")
	
	2. Connect to Jupyter Notebook from the browser by replacing the private ip in the first link from the nohup.out with the public ip of the instance (here: 18.205.163.6)
	
	*http://18.205.163.6:8888/?token=2eebba01bb157a866a6c3ae7ceb31bea0383da62db1d94dd*
	![Alt text](pics/JupyterNotebookBrowser.png?raw=true "JupyterNotebookBrowser")
	
4. Configure a virtual Anaconda environment of **Python 3.6** within Jupyter
	1. From the Jupyter Notebook in the browser click on the menu New and then select Terminal and type the following:
		```sh
		conda create --name my_envP3.6 python=3.6
		# if you want to remove it use:
		#conda remove --name my_envP3.6 --all
		#i if you want to list all the environments type:
		# conda info --envs
		```
	![Alt text](pics/condaenvs.png?raw=true "condaenvs")
	
	2. Install nb_conda which updates the conda package
		```sh
		conda install nb_conda
		```
	3. Activate your virtual anaconda environment of Python 3.6
		```sh
		conda activate my_envP3.6
		```
	4. Add (link) this environment to the Jupyter Notebook:
		```sh
		conda install ipykernel #this package is required for linking
		jupyter kernelspec list #to list your kernels in jupyter
		# jupyter kernelspec uninstall unwanted-kernel #to remove a kernel
		ipython kernel install --user --name=Python3.6_tf
		```
	![Alt text](pics/ipython.png?raw=true "ipython")
	
		If you refresh the browser page of the Jupyter, you will see the new environment:
	![Alt text](pics/newenv.png?raw=true "newenv")
	
5. Clone the GitHub repository of Leo to upload all the scripts and data
	1. Install Git
		```sh
		sudo yum install git
		```
	2. Go to  Leo's GitHub repository https://github.com/leodsti/AWS_Tutorials/tree/master/MNIST
	3. Click on Fork and click on the green button "Clone or download" and copy the URL: https://github.com/MatinaDataEngineer/AWS_Tutorials.git
	
	4. In the terminal of the Jupyter Notebook type
		```sh
		git clone https://github.com/MatinaDataEngineer/AWS_Tutorials.git
		```
	5. If we go back to the Jupyter browser and we refresh it, we see that the whole AWS_Tutorials repository is there:
	![Alt text](pics/Gitrepo.png?raw=true "Gitrepo")
	
6. Download the Jupiter Notebook which contains the trained model for MINST of Leo: 
	1. From the cloned repository of AWS_Tutorials inside the Jupyter we select the MNIST folder and we click on the Notebook "00-mnist-cnn.ipynb"
	2. We get a "Kernel not found" message and we select our virtual environment "Python3.6_tf"
	![Alt text](pics/kernelnotfound.png?raw=true "kernelnotfound")
	
	3. If we try to execute it, it does not work because we have not yet installed the needed packages in our virtual environment
	![Alt text](pics/notebookerror.png?raw=true "notebookerror")
		
7. Install in your virtual environment the provided Python environment setup in requirements.txt 
*(produced with pip freeze command)*
	```sh
	pip install -r AWS_Tutorials/MNIST/requirements.txt
	```
	![Alt text](pics/reqs.png?raw=true "reqs")
	
8. Go to the Jupyter Notebook (00-mnist-cnn) browser tab,  click on "Kernel" tab menu and then select "Restart"

9. Execute now the Notebook by clicking on "Run" button
	![Alt text](pics/notebookok.png?raw=true "notebookok")
	<br>
	- The main framework in Deep Learning is TensaFlow (in Cpp), then PyTorch…
	- Keras is a meta-framework and translates everything into TensaFlow, enabling easier syntax
	- Step2: tries to predict 10 classes (pictures 28pix * 28pix = 784 decision variables) and 60k rows. It downloads the minst data (x_train is the data, y_train are the variables 0..9)
	- Step3: multidimentional arrays (matrices). In IT they are arrays inside arrays inside arrays… makes the so-called "tensors" here the dimension is pixes per color (here we have black and white)
	- Step4: Normalizes everything from 0-255 to 0-1. Recasting, making sure that the columns are categorized correctly. (categorical data vs numerical data)
	- Step 5: the answer 0 means wrong and the answer 1 means right. (a vector)
	- Step 6: This is how you build your neural network in layers. Keras is designed to make it simplier. With add we just add a layer. We have a convolutional layer with a kernel 3x3. If you wanted to do the same with Tensor Flow, it is much more difficult. In the end you compile everything.
	
	![Alt text](pics/compiled.png?raw=true "compiled")
	
	It has actually more than 200k parameters!
	- Step 7: we change the number of epochs and times to change the weights. So, we will try to change 10 times these 200k parameters.
	- Step 8: we do fit, we are basically running the whole thing, training our model. From the very first epoch we have reached 97,8% accurracy
	- Step 9. It is the final test: 99.4% accuracy
	![Alt text](pics/finaltest.png?raw=true "finaltest")
	
	- Important is to reach the step 14 which does a save of the trained model (which contains the weights) here
	![Alt text](pics/trainedmodel.png?raw=true "trainedmodel")
	
	> We have finished with 1 and we have successfully saved the trained model (we should normally export it with scp and terminate the instance)
		
### Step 2: Save the model and deploy it on the Application Server (**Backend**) which is a **private** Ubuntu EC2 Instance <a name="STEP2"></a> 
>*We will use Flask which uses Python, which is an equivalent of NodeJS which uses JavaScript. (the deployable file should be a new keras_flask.py) The saved model is the file: http://18.205.163.6:8888/edit/AWS_Tutorials/MNIST/cnn-mnist*
 
1. Launch a private Ubuntu EC2 Instance 
	1. Go to EC2 Service, to Instances screen and click on "Launch Instance" button
	2. Select **Ubuntu Server 18.04 LTS (HVM), SSD Volume Type**
	3. Instance Type: use free tier t2.micro (we will upgrade it later, before training the model)
	4. VPC: **VPC_A19P1**
	5. Subnet: **PrivateSubnet1_A19P1**
	6. Auto-assign IP: **disable**(it is the backend)
	7. Storage: **16 GB**
	8. Tag: Name **AI_Backend**
	9. New Security Group: **SG_AI_Backend** with 1 Inbound rule:
		1. All traffic from the security group of the Jump Box (Bastion Server): SG_JB_A19P1
	10. Click on Launch Instance (using an existing key pair e.g. A19_Project1.pem)
	11. Note the private IP: 11.80.3.156
		
2. Connect with ssh to the AI_Backend over the Jump Box (Bastion Server), which needs to have also a copy of the pem key.
	```sh
	# connect to the JB
	ssh -i Downloads/"A19_Project1.pem" ec2-user@18.234.101.88
	# connect to the AI Backend
	ssh -i /tmp/"A19_Project1.pem" ubuntu@11.80.3.156
	```sh
	
3. We move over to the server the trained model from Leo's GitHub
	```sh
	sudo apt-get install git
	git clone https://github.com/MatinaDataEngineer/AWS_Tutorials.git
	```
	>We could alternatively upload our own trained model "cnn-mnist" to the Backend Server (over the JB) after downloading it from the Dev Server with SCP.
	![Alt text](pics/mytrained.png?raw=true "mytrained")

	
4. We prepare our Python Environment and deploy our API by running the script keras_flask.py (WARNING: The script from GitHub does not work. Replace its contents with this script here: [keras_flask_matina.py](pythonscripts/keras_flask_matina.py))
	```sh
	sudo apt-get update
	sudo apt install python3-pip   # installing pip3
	# Install Flask
	pip3 install Flask
	# Install Imageio
	sudo apt-get install python3-imageio 
	# install Keras
	pip3 install keras
	# install TensorFlow
	pip3 install tensorflow
	# CORS: to configure cross-origin resource sharing in the HTTP nodes because the Backend is in the private subnet and the traffic will be not done directly with the Frontend but through the NAT instance
	sudo pip3 install -U flask-cors
	# install a specific version of SciPy to be able to import imresize
	sudo pip3 install scipy==1.1.0 --user
	# install opencv
	sudo pip3 install opencv-python
	
	cd AWS_Tutorials/MNIST/
	python3 ./keras_flask.py &
	```
	![Alt text](pics/deployed.png?raw=true "deployed")
	
*It runs on port 5000 and it expects traffic (/predict request) from the Frontend server (Web application).*

	
### Step3: Serve it on a Web Server (**Frontend**) in a **public** EC2 instance <a name="STEP3"></a>
1. Launch a public UBUNTU EC2 Instance
	1. Go to EC2 Service, to Instances screen and click on "Launch Instance" button
	2. Select **Ubuntu Server 18.04 LTS (HVM), SSD Volume Type**
	3. Instance Type: use free tier t2.micro (we will upgrade it later, before training the model)
	4. VPC: **VPC_A19P1**
	5. Subnet: **PublicSubnet1_A19P1**
	6. Auto-assign IP: **enable** 
	7. Storage: t2.micro
	8. Tag: Name **AI_Frontend**
	9. New Security Group: **SG_AI_Frontend** (we will configure it later)
	10. Click on Launch Instance (using an existing key pair e.g. A19_Project1.pem)
2. You connect with ssh to it
	```sh
	ssh -i Downloads/"A19_Project1.pem" ubuntu@35.173.191.173
	```
3. You need to install Apache server
	```sh
	sudo apt-get update
	sudo apt install apache2
	sudo systemctl status apache2
	```
	![Alt text](pics/apachestart.png?raw=true "apachestart")
4. Download the Leo's GitHub for the frontend files:
	```sh
	sudo apt-get install git
	git clone https://github.com/MatinaDataEngineer/AWS_Tutorials.git
	```
5. We add our static folder to the Apache
	```sh
	sudo mv AWS_Tutorials/MNIST/static  /var/www/html/
	```
	1. We refresh our page to verify it works: 
	![Alt text](pics/apachewebpage.png?raw=true "apachewebpage")
6. We replace the starting webpage with our index.html
	```sh
	sudo mv AWS_Tutorials/MNIST/index.html /var/www/html/
	```
	1. We refresh our page to verify it works:
	![Alt text](pics/indexplain.png?raw=true "indexplain")
		
7. You need to modify now the Security Group: **SG_AI_Frontend**
	1. Allow Inbound HTTP from Anywhere
	2. Modify SSH to allow it only from your IP
	
8. Since the Backend is in the private subnet and cannot recieve traffic from the Internet, we will use the NAT Instance to receive the request from the index.html sript from the Frontend (made over the public internet). So, in the script **index.html** we need to add the public IP of the **NAT** 3.83.23.25 and an opened port on the NAT: 5000 used for this.
	1. Edit the index.html and replace the ip of the /predict request to match the public IP of the NAT instance
	```sh
	vi /var/www/html/index.html
	```
	![Alt text](pics/editedwebpage.png?raw=true "editedwebpage")
	
	2. Mofify the security group of the NAT instance (**SG_NAT_A19P1**) to accept inbound tcp traffic to port 5000 from **Anywhere** and also add a rule  for inbound ssh traffic from my IP

9. The NAT needs to route it to the Backend Instance (on port 5000) and will automaticaly route back the answer.
	1. We need to modify the **SG_AI_Backend** by adding another inbound rule to port 5000 from the **SG_NAT_A19P1**
	
10. We configure port-forwarding in the NAT instance
	1. Connect with ssh to the NAT instance
	```sh
	ssh -i Downloads/"A19_Project1.pem" ec2-user@3.83.23.25
	```
	2. Find the public network interface (here is eth0)
	```sh
	ip route show | grep default
	```
	3. Check if port forwarding is enabled in NAT instance
	```sh
	sudo sysctl -p
	```
	4. Enable it, if necessary by setting "net.ipv4.ip_forward = 1"
	```sh
	sudo vi /etc/sysctl.conf
	```
	![Alt text](pics/enablingportf.png?raw=true "enablingportf")
	
	5. Check if POSTROUTING is enabled in NAT Instance
	```sh
	sudo iptables -t nat -v -L POSTROUTING -n --line-number
	```
	![Alt text](pics/postrouting.png?raw=true "postrouting")
	
	6. Create the new rule for PREROUTING (to destination port and IP of the Backend)
	```sh
	sudo iptables -t nat -A PREROUTING -p tcp -i eth0 --dport 5000 -j DNAT --to-destination 11.80.3.156:5000
	sudo iptables -A FORWARD -p tcp -d 11.80.3.156 --dport 5000 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT
	#checking
	ip route
	```
	![Alt text](pics/forwd.png?raw=true "f")
	
	7. Reboot NAT instance

11. We now try to predict a handwritten number on our web application:
![Alt text](pics/predict7.png?raw=true "predict7")
![Alt text](pics/successminst.png?raw=true "successminst")

*Success!*

