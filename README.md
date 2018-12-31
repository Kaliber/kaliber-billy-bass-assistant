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

## Modify start_google_assistant.sh file
Edit the file `start_google_assistant.sh` with your own `--project-id` and `--device-model-id` you created in the previous steps.

## Setting up PulseAudio
1. `sudo apt install -y pulseaudio paprefs pavucontrol`
2. `sudo reboot`
3. `cd /etc/pulse`
4. Make a backup of the file default.pa by using the commands: `sudo cp default.pa default.pa.bak`

### Modify default.pa
This is our `default.pa` config file. The only things that has been changed are the default `set-default-sink` and `set-default-source` settings (see last 2 lines)
```
#!/usr/bin/pulseaudio -nF
#
# This file is part of PulseAudio.
#
# PulseAudio is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# PulseAudio is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with PulseAudio; if not, see <http://www.gnu.org/licenses/>.

# This startup script is used only if PulseAudio is started per-user
# (i.e. not in system mode)

.fail

### Automatically restore the volume of streams and devices
load-module module-device-restore
load-module module-stream-restore
load-module module-card-restore

### Automatically augment property information from .desktop files
### stored in /usr/share/application
load-module module-augment-properties

### Should be after module-*-restore but before module-*-detect
load-module module-switch-on-port-available

### Load audio drivers statically
### (it's probably better to not load these drivers manually, but instead
### use module-udev-detect -- see below -- for doing this automatically)
#load-module module-alsa-sink device=hw:0,0
#load-module module-alsa-source device=hw:1,0
#load-module module-oss device="/dev/dsp" sink_name=output source_name=input
#load-module module-oss-mmap device="/dev/dsp" sink_name=output source_name=input
#load-module module-null-sink
#load-module module-pipe-sink

### Automatically load driver modules depending on the hardware available
.ifexists module-udev-detect.so
load-module module-udev-detect
.else
### Use the static hardware detection module (for systems that lack udev support)
load-module module-detect
.endif

### Automatically connect sink and source if JACK server is present
.ifexists module-jackdbus-detect.so
.nofail
load-module module-jackdbus-detect channels=2
.fail
.endif

### Automatically load driver modules for Bluetooth hardware
.ifexists module-bluetooth-policy.so
load-module module-bluetooth-policy
.endif

.ifexists module-bluetooth-discover.so
load-module module-bluetooth-discover
.endif

### Load several protocols
.ifexists module-esound-protocol-unix.so
load-module module-esound-protocol-unix
.endif
load-module module-native-protocol-unix

### Network access (may be configured with paprefs, so leave this commented
### here if you plan to use paprefs)
#load-module module-esound-protocol-tcp
#load-module module-native-protocol-tcp
#load-module module-zeroconf-publish

### Load the RTP receiver module (also configured via paprefs, see above)
#load-module module-rtp-recv

### Load the RTP sender module (also configured via paprefs, see above)
#load-module module-null-sink sink_name=rtp format=s16be channels=2 rate=44100 sink_properties="device.description='RTP Multicast Sink'"
#load-module module-rtp-send source=rtp.monitor

### Load additional modules from GConf settings. This can be configured with the paprefs tool.
### Please keep in mind that the modules configured by paprefs might conflict with manually
### loaded modules.
.ifexists module-gconf.so
.nofail
load-module module-gconf
.fail
.endif

### Automatically restore the default sink/source when changed by the user
### during runtime
### NOTE: This should be loaded as early as possible so that subsequent modules
### that look up the default sink/source get the right value
load-module module-default-device-restore

### Automatically move streams to the default sink if the sink they are
### connected to dies, similar for sources
load-module module-rescue-streams

### Make sure we always have a sink around, even if it is a null sink.
load-module module-always-sink

### Honour intended role device property
load-module module-intended-roles

### Automatically suspend sinks/sources that become idle for too long
load-module module-suspend-on-idle

### If autoexit on idle is enabled we want to make sure we only quit
### when no local session needs us anymore.
.ifexists module-console-kit.so
load-module module-console-kit
.endif
.ifexists module-systemd-login.so
load-module module-systemd-login
.endif

### Enable positioned event sounds
load-module module-position-event-sounds

### Cork music/video streams when a phone stream is active
load-module module-role-cork

### Modules to allow autoloading of filters (such as echo cancellation)
### on demand. module-filter-heuristics tries to determine what filters
### make sense, and module-filter-apply does the heavy-lifting of
### loading modules and rerouting streams.
load-module module-filter-heuristics
load-module module-filter-apply

### Make some devices default
set-default-sink alsa_output.usb-Generic_USB2.0_Device_20130100ph0-00.analog-stereo
set-default-source alsa_input.usb-C-Media_Electronics_Inc._USB_PnP_Sound_Device-00.analog-mono
```

## Modify animatronic_mouth.py file
If needed, edit the file `animatronic_mouth.py` with your own PulseAudio monitor output.

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

### Credits:

- [aarmea](https://github.com/aarmea) - For his `animatronic_mouth.py` script (Which we have adapted to our needs)
