# Get started

Clone main branch:
`git clone https://github.com/UTDallasEPICS/UTDesign-FabLab-Tool-Access.git`

Install Node (using nvm):

```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash 
nvm install node
```

To start website:
`node server.js`

___________________________________________

### Setup FabFivePi.py to auto start in Pi

Creating a new startup script

`nano startup_script.sh`


Make the script executable


`chmod +x /path/startup_script.sh`


Make the script run from bootup using systemd
```bash
sudo nano /etc/systemd/system/startup_script.service
```
```ini
[Unit]
Description=Startup Script

[Service]
Type=simple
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/pi/.Xauthority
ExecStart=/bin/bash /home/pi/Desktop/startup_script.sh

[Install]
WantedBy=default.target
```

```bash
sudo systemctl daemon-reload
To test:
sudo systemctl start startup_script.service
sudo systemctl status startup_script.service
```
