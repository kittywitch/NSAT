```
888888ba  .d88888b   .d888888  d888888P 
88    `8b 88.    "' d8'    88     88    
88     88 `Y88888b. 88aaaaa88a    88    
88     88       `8b 88     88     88    
88     88 d8'   .8P 88     88     88    
dP     dP  Y88888P  88     88     dP                                         
```

# NSAT
A python3 network security analytics tool.

## Features

* Client server model
* TLS support, allowing self-signed certificates
* Twilio and Pushover notification support
* Token based authentication, accepted by the user at the console
* SSH successful login notifications
* Listen port listing notifications
* SSH and listen port listing do not work on Windows, do not enable check_ssh and check_ports in config.yaml on Windows.

## Dependencies

### Linux
```
sudo apt install python3 python3-dev python3-setuptools python3-pip
pip install pyopenssl pyyaml twisted configparser service_identity twilio
```

### Windows
Download [Python 3.7.3](https://www.python.org/downloads/release/python-373/)'s Windows x86-64 executable installer and install it, adding it to PATH and removing the PATH limitations.

Download [Build Tools for Visual Studio 2019](https://visualstudio.microsoft.com/downloads/) and install the Visual C++ build tools. Reboot.

```
pip install pyopenssl pyyaml twisted configparser service_identity twilio pywin32
```

## Self-signed TLS setup
```
cd server
openssl req -newkey rsa:2048 -nodes -keyout keys/server.key -out keys/server.crt
cat keys/server.crt keys/server.key > keys/server.pem
```

## Running

Please set up `server/config.yaml` and `client/config.yaml` appropriately before usage.

* Windows - Server - `python server/main.py`
* Windows - Client - `python client/main.py`
* Linux - Server - `python3 server/main.py`
* Linux - Client - `python3 client/main.py`
