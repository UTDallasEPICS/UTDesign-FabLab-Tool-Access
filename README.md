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

> *Note: This guide assumes that you are cloning the repo into `home/pi/Desktop/` for raspberry pi.

Clone main branch:
```
git clone https://github.com/UTDallasEPICS/UTDesign-FabLab-Tool-Access.git
```

### Setup Tool Access System:

All files under /Raspberry_Pi. (Other dirctories can be deleted)

We'll be using xterm for our terminal output (used in startup_script.sh). You can use any terminal that supports detached terminal `-e` such as lxterminal.

```bash
sudo apt install xterm
```

Run the `FabFivePi.py` program and you should be done.

Check out [here](https://github.com/UTDallasEPICS/UTDesign-FabLab-Tool-Access?tab=readme-ov-file#setup-fabfivepipy-to-auto-start-in-pi-optional) to autostart the program at bootup.


### Setup server:

Install Node (using nvm):

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
```
```bash
nvm install node
```

Install dependencies:
```bash
npm ci
```

To start web server:
```
node server.js
```
Go to `http://127.0.0.1:3000/` to view the website

If the database & server is not locally hosted:

1. Configure mySQL connection in `database.js` & `FFServer.py`
2. Change the IP address to bind:
  - In server.js: `const hostname = "<IP address>";`
  - In FFServer.py: `ServerIP = '<IP address>'`
  - In FabFivePi.py: `server_address = ('<IP address>', 2222)`

Make sure to also run the python server module

```
python3 FFServer.py
```
_____________________

#### Using Docker Engine (Experimental)

A dockerfile is added to make it easier to automatically bundle the installation process for the website and the database. But currently FFServer.py has to be manually installed along with the dockerfile.
To build the dockerfile, run:
```bash
docker compose up --build
```
Read more `README.Docker.md`
___________________________________________

### Setup FabFivePi.py to auto start in Pi (Optional)

Create a new startup script (or use the one provided)

```bash
nano /home/pi/Desktop/UTDesign-FabLab-Tool-Access/Raspberry_Pi/startup_script.sh
```

Make the script executable

```bash
chmod +x /UTDesign-FabLab-Tool-Access/Raspberry_Pi/startup_script.sh
```


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
ExecStart=/bin/bash /home/pi/Desktop/UTDesign-FabLab-Tool-Access/Raspberry_Pi/startup_script.sh

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

__________________________________________

### Issues?

#### ModuleNotFound: RPLCD

Try installing the library globally

```
git clone https://github.com/dbrgn/RPLCD.git
```
Once in the cloned directory:
```
sudo python setup.py install
```
