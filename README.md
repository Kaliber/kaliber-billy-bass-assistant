# Billy Bassistant
Using the [Google Assistant SDK](https://github.com/googlesamples/assistant-sdk-python/)

Resources:
- https://gist.github.com/aarmea/f3010fd58629acda9c458e883ee010b5
- https://github.com/googlesamples/assistant-sdk-python/tree/master/google-assistant-sdk/googlesamples/assistant/library

## Parts used

- List will be added shortly

## First start
1. Enable _'SSH'_ (using `sudo raspi-config`)
2. `sudo apt-get update`
3. `sudo apt-get upgrade`
4. `sudo reboot`

## Remove onboard sound card
1. `cd /etc/modprobe.d`
2. `sudo nano alsa-blacklist.conf`
3. Add line: `blacklist snd_bcm2835`
4. Save file and reboot

## Configure USB Speaker and USB Microphone
Follow instructions on this page: [Configure and Test the Audio](https://developers.google.com/assistant/sdk/guides/service/python/embed/audio)

Make sure you increase the record volume of the microphone to 100%. Also set the output of the speaker at 80%.

## Setting up Google Voice Assistant
1. Follow steps from: https://developers.google.com/assistant/sdk/guides/service/python/

2. After following the installation steps from developers.google.com, follow the steps in this Github page: https://github.com/googlesamples/assistant-sdk-python/tree/master/google-assistant-sdk/googlesamples/assistant/library

**Note:** You should be in your virtual environment. You should see the prefix (env) in your terminal (If not, run command `source env/bin/activate`)

3. Run command: pip3 install --upgrade -r requirements.txt
4. Run command: python3 -m hotword --project-id YOUR_PROJECT_ID --device-model-id YOUR_MODEL_ID
5. Device should be registrerd to your Google account and you can config the Assistant using the Google Home app on your mobile device.

To make sure the SDK also works outside the virtual environment, run the command `pip3 install --upgrade -r requirements.txt` after a reboot (inside the git folder)

## Setting up PulseAudio
1. `sudo apt install -y pulseaudio paprefs pavucontrol`
2. `sudo reboot`
3. `cd /etc/pulse`
4. Make a backup of the default files by using the commands:  
`sudo cp daemon.conf daemon.conf.bak`  
`sudo cp default.pa default.pa.bak`

**@TODO**: Add changes you need to make (maybe add config files?)

## Installing Motor Hat software
https://learn.adafruit.com/adafruit-dc-and-stepper-motor-hat-for-raspberry-pi/installing-software
https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi

## Setting up Wi-Fi
Let's use the command for this `wpa_passphrase "YOUR_SSID_HERE"` (after running this command, fill in your password and press _Enter_). This will generate output that can be used in the `wpa_supplicant.conf` file. For example:

Edit the following file and paste the output from the previous command and the end of the file:  
`sudo nano /etc/wpa_supplicant/wpa_supplicant.conf`

More info: [Setting WiFi up via the command line](https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md)

## Start scripts after boot (services)

### Google Assistant script
Let's create a new service using the following command:  
`sudo systemctl edit --force --full start-google-assistant.service`

Paste the following code:
```
[Unit]
Description=Google Assistant Service
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/kaliber-billy-bassistant/
ExecStart=/home/pi/kaliber-billy-bassistant/start_google_assistant.sh

[Install]
WantedBy=multi-user.target
```

Save and exit the file.

Check the status of the service:  
`systemctl status start-google-assistant.service`

Enable the service:  
`sudo systemctl enable my_script.service`

Start the service:  
`sudo systemctl start my_script.service`

### Mouth script
Let's create a new service using the following command:  
`sudo systemctl edit --force --full start-mouth-script.service`

Paste the following code:
```
[Unit]
Description=Billy Bass Mouth Service
After=sound.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/kaliber-billy-bassistant/
ExecStart=/home/pi/kaliber-billy-bassistant/start_mouth_script.sh

[Install]
WantedBy=multi-user.target
```

Save and exit the file.

Check the status of the service:  
`systemctl status start-mouth-script.service`

Enable the service:  
`sudo systemctl enable start-mouth-script.service`

Start the service:  
`sudo systemctl start start-mouth-script.service`

More information: [Running a script after an internet connection is established](https://raspberrypi.stackexchange.com/questions/78991/running-a-script-after-an-internet-connection-is-established)

---

## Credits:

- [aarmea](https://github.com/aarmea) - For his `animatronic_mouth.py` script (Which we have adapted to our needs)
