# Project Overview

This project creates an access system for the operation of power tools in FabLab, creating a safer environment by ensuring that only trained students can access the equipment for a limited time. 

## Website Overview

The website neatly displays the time log of anyone who have successfully turned on a machine with their comet card. It was primarily made for Tim to quickly view the usage of the machines and potentially narrow down issues. 

### Key features

- Sort log data by machine type
- Sort log data by month and day
- Download desired logs as a CSV file
- Deletion of machine if needed
- Automatically updates machine list from database
- Optimized connections using SQL pooling

### Frameworks

- Node, express, mySQL

_____

# Get started

Clone main branch:
`git clone https://github.com/UTDallasEPICS/UTDesign-FabLab-Tool-Access.git`

###Setup server:

Install Node (using nvm):

```
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash 
nvm install node
```

If the database & server is not locally hosted:

1. Configure mySQL connection in `database.js` & `FFServer.py`
2. Change the IP address to bind:
  - In server.js: `const hostname = "<IP address>";`
  - In FFServer.py: `ServerIP = '<IP address>'`
  - In FabFivePi.py: `server_address = ('<IP address', 2222)`



To start website:
`node server.js`

Make sure to also run `python3 FFServer.py`

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
