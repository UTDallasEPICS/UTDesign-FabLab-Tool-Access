## Website Overview

The website neatly displays the time log of anyone who have successfully turned on a machine with their comet card. It was made for admins of the Fab-Lab to quickly view the usage of the machines and potentially narrow down issues. 

#### Key features

- Sort log by machine type
- Sort log by month and day
- Download desired log data as a CSV file
- Deletion of machine if needed
- Automatically updates machine list from database
- Optimized connections using SQL pooling

## Get started

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

### Setup FabFivePi.py to auto start in Pi (Optional)

Create a new startup script (or use the one provided)

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
______________________________________________

For server side management (Node.js), highly recommend pm2:

https://pm2.keymetrics.io/docs/usage/quick-start/
