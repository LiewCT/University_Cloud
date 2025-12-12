# University_Cloud

sudo su  
yum install git -y  
git clone [http]  
yum install python-pip -y  
pip install flask pymysql boto3  


# Keep instance running

1. Create a systemd service file

sudo nano /etc/systemd/system/flaskapp.service

Inside:
[Unit]
Description=Flask App
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/yourproject
ExecStart=/usr/bin/python3 app.py
Restart=always

[Install]
WantedBy=multi-user.target


2. Reload systemd

sudo systemctl daemon-reload


3. Start the service

sudo systemctl start flaskapp


4. Enable at boot

sudo systemctl enable flaskapp
