# Jupyter
## Objective 
Create a public UBUNTU EC2 instance and install Python and Jupyter. 
Create and manage Virtual Python Environments (using both PEW and ANACONDA) and use them in Jupyter Browser by keeping it available even if you disconnect from the EC2 instance.

### Step 1: Launch an UBUNTU 18.x (latest) EC2 instance on the free tier
1. From the EC2 Screen We click on Launch Instance
2. Select Ubuntu Server 18.04 LTS (HVM), SSD Volume Type - ami-07ebfd5b3428b6f4d (64-bit x86) 
3. t2.micro (free tier)
4. VPC: We reuse an existing one with attached IGW: **TestFirstA19** within its unique public subnet
5. Autoassign Public IP: Disable (we will use an Elastic IP)
6. Name tag: **Jupiter_A19P3**
7. EBS: 16GB
8. New security Group: **SG_JUP_A19P3**
9. Configure it for SSH from MyIP and Custom TCP for the port-range **8888-8898 from 0.0.0.0/0** for the Jupyter application		
10. Launch using the existing Key pair: A19_Project1 (you may change this to your own)

### Step 2: Attach a Public IP to the Instance
1. Click on Elastic Ips -> Allocate Elastic IP address
2. Menu Actions -> Associate Elastic IP address -> Instance: **Jupiter_A19P3**
3. Note the public IP is: *3.210.6.84*

### Step 3: Connect to the Instance and test Python
1. Connect with ssh to the instance
```sh 
ssh -i Downloads/"A19_Project1.pem" ubuntu@3.210.6.84
```
1. Check for Python
```sh 
python --version
python3 --version
```
1. Execute a small python script
```sh 
python3
print('Hello, my name is Matina')
```
You yould put it in a file and copy it over using scp (or WinSCP which needs to load the connection from Putty) (or CyberDuck)
using as host: 3.210.6.84 and username: ubuntu with SFTP to port 22:
![Alt text](pics/CyberDuck.png?raw=true "CyberDuck")
You can also use vi to type it into a file and execute it:
```sh 
mkdir pythonscripts
chmod 777 pythonscripts/
vi pythonscripts/hello.py
cat pythonscripts/hello.py
python3 pythonscripts/hello.py
print('Hello, my name is Matina')
```
![Alt text](pics/pythontest.png?raw=true "pythontest")
		
### Step 4: Install pip (after updating all the packages)   
1. Install pip3 (Python package installer)
```sh 
	sudo apt-get update -y
	sudo apt-get install python3-pip -y
```

### Step 5: Install Jupyter
1. Install Jupyter (https://jupyter.org/install)
```sh 
		sudo pip3 install jupyter
		#jupyterlab
```
### Step 6: Launch Jupyter
```sh 
		jupyter notebook
```
![Alt text](pics/LaunchJupyterNotebook.png?raw=true "LaunchJupyterNotebook")		
	
### Step 7: Connect to Jupyter Notebook using your browser
1. We open a local browser and we paste the first URL: http://localhost:8888/?token=f35044e9f6404299471274be805fe006b82db74c25107bbc but it does not work because localhost is not the right ip address
1. So, we replace this with our public ip but again it does not work because the port 8888 binds to localhost (127.0.0.0) of the distant machine
1. So, we need to call Jupyter notebook differently to bind it to every ip possible, which makes it bind to the private ip of the instance, which is automatically connected in the background to ist public ip:
```sh 
jupyter notebook --ip=0.0.0.0
```
1. Now, it works as soon as we replace the ip with the public ip: http://3.210.6.84:8888/?token=f35044e9f6404299471274be805fe006b82db74c25107bbc
1. From New-> Terminal you can open multiple terminals that stay in your list and are accessible from your browser

### Step 8: Execute Jupyter Notebook in a way that the os process remains running even if you disconnect from the ec2 (e.g. you shut down your pc or your session times out)
(https://askubuntu.com/questions/348836/keep-the-running-processes-alive-when-disconneting-the-remote-connection)
1. **nohup** will run it in another env and & will run it in the background
```sh 
			nohup jupyter notebook --ip=0.0.0.0 &		
```
1. So, in the browser you just type: **http://3.210.6.84:8889/login**  (notice that the first part is the public ip of the instance and the port it runs to)
1. To find your token, in the terminal type: 
```sh
jupyter notebook list
```
![Alt text](pics/JupiterNohup.png?raw=true "JupiterNohup")
1. You copy paste the token in the login page of the browser. 
![Alt text](pics/JupyterLoggedIN.png?raw=true "JupyterLoggedIN")
The Jupyter remains accessible, even if the ssh terminal connections dies. 
(you could also find it if you do ls and then cat nohup.out)
If you want to terminate it, you need to type:  "jupyter notebook stop"

### Step 9: Create Virtual Environments (https://janakiev.com/blog/jupyter-virtual-envs/)
		Pip3 install --user virtualenv
		Python3 -m venv myenv
		source myenv/bin/activate
		a. Using ANACONDA (https://www.digitalocean.com/community/tutorials/how-to-install-anaconda-on-ubuntu-18-04-quickstart)
			i. Go to anaconda.com/distribution and copy the link for the latest anaconda distribution on linux: 
			https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh
			ii. Open a terminal from the Jupyter browser
			iii. Create a temp folder: 
				1) mkdir tmp
				2) cd tmp
			iv. Download the latest anaconda version using:
			curl -O https://repo.anaconda.com/archive/Anaconda3-2019.10-Linux-x86_64.sh
			v. Execute the installation script after making ls:
			bash Anaconda3-2019.10-Linux-x86_64.sh
			vi. df
		b. Second option, using PEW
			i. Open a new terminal in the Jupyter browser
				pip3 install pew
				pew
				pew new matinapew
				
			ii. It takes you to that new launched environment. To get out, type: exit
			iii. To see which environments you have type: ew ls
			pew workon matinapew
			iv. Create another environment in another terminal: matinatf
			v. Now we will freeze:
				Pip3 freeze. (lists the python packages you have installed in your environment)
				Pip3 install pandas
				Pip3 freeze (pandas is shown)
		C. Link it with Jupyter:
		i. We go to each of our virtual environment from the terminals and we issue: 
			pip3 install ipykernel
			python3 -m ipykernel install --user --name=MatinaPewEnv
			
		ii. (after reloading the page)
		iii. Export you environment packages into a file:
			 pip3 freeze > matinapewenv.txt
			cat matinapewenv.txt
	10. We work from the same file directory and Pew takes care of the python environment
	11. Create a new environment as a clone of matinapewenv.txt
		i. Open a new terminal
		pew rm matinatf (this is how you delete an environment)
		pew new matinapewclone
		pip3 install -r matinapewenv.txt
		python3 -m ipykernel install --user --name=MatinaPewEnv2
		

