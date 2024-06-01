# Motor-controlling client
The solution is to be installed on the RPi-based computer.
The installation is possible on other machines, even non-Linux based but then `cardreader_writer.py` should be disabled and all mentions of it should also be removed from Python code.

## Installation
Clone this repository in any directory. Once it is done, create a virtual environment and install the following modules there:
 * `mfrc522`
 * `flask`
 * `flask-socketio`
 * `requests`
 * `json`

As this is done, via your virtual environment, you can run the directory in its `bin/python3` and specifying `host` (must be in format of `http://hostname:port/` with trailing slash and the protocol mentioned), `app_id` and `app_public_key` that is set in the database. It should be available at `http://localhost:5000/`

If you want the front-end to be available at other machines, you will need to add `host="0.0.0.0"` to the arguments when starting the program inside `__main__.py`, at `mgmt.app.run`

### Optional: run backend at the OS start (systemd)

This requires `sudo` access for creating files in `/etc/systemd/system/`.
You will need to create a file in `/etc/systemd/system/` that will end with `.service`, for example `/etc/systemd/system/login-screen.service`.

Here is an example of such. `/path/to/environment` and `/path/to/client` should be replaced with the correct ones. It is recommended to run GUI on vertical screen.
```
[Unit]
Description= Login screen
[Service]
Type=simple
WorkingDirectory=/path/to/client/
ExecStart=/path/to/environment/bin/python3 /path/to/client/ "http://hostname:port/" "APP_ID" "APP_PUBLIC_KEY"
[Install]
WantedBy=multi-user.target
```

### Optional: run front-end on the start of the RPi's GUI (Firefox)

This should be dne as a user, which is runs by default, not as a superuser. In order to find the name of it, run from the Terminal `echo $USER`.
In order to run the GUI, we need to run a web browser, we will use Firefox. In order to find the absolute path to firefox, you can run `which firefox` in Terminal. In my case, that path is `/usr/bin/firefox`. It also is used in the example file.

Then, under `/home/$USER/.config/autostart` (it should be created with `mkdir -p` if does not exist) create a file with ending `.desktop`, for example `/home/$USER/.config/autostart/login-screen.desktop`. The contents of the file should be as follows:
```
[Desktop Entry]
Type=Application
Exec=/usr/bin/firefox --kiosk http://localhost:5000/
Name=LoginScreen
```