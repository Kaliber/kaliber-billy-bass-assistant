# Billy Bassistant
Using the [Google Assistant SDK](https://github.com/googlesamples/assistant-sdk-python/)

Resources:
- https://github.com/respeaker/mic_hat
- https://gist.github.com/aarmea/f3010fd58629acda9c458e883ee010b5
- https://github.com/googlesamples/assistant-sdk-python/tree/master/google-assistant-sdk/googlesamples/assistant/library

## First start
1. Enable 'SSH'
2. Login to pi
3. sudo apt-get update
4. sudo apt-get upgrade
5. reboot

## Install audio + mic card
https://github.com/respeaker/seeed-voicecard

1. git clone https://github.com/respeaker/seeed-voicecard
2. cd seeed-voicecard
3. sudo ./install.sh
4. sudo reboot

## Remove onboard sound card
1. cd /etc/modprobe.d
2. sudo nano alsa-blacklist.conf
3. Add line: `blacklist snd_bcm2835`
4. Save file and reboot

## Setting up Google Voice Assistant
1. Follow steps from: https://developers.google.com/assistant/sdk/guides/service/python/

2. After install steps from developers.google.com, see steps in Github page: https://github.com/googlesamples/assistant-sdk-python/tree/master/google-assistant-sdk/googlesamples/assistant/library
  Note: You should be in your virtual environment, you should see the prefix (env) in your terminal (If not, run command `source env/bin/activate`)
  2.1. Run command: pip3 install --upgrade -r requirements.txt
  2.2. Run command: python3 -m hotword --project-id YOUR_PROJECT_ID --device-model-id YOUR_MODEL_ID
  2.3. Device should be registrerd to your Google account and you can config the Assistant using the Google Home app on your mobile device.

To make sure the SDK also works outside the virtual environment, run the command `pip3 install --upgrade -r requirements.txt` after a reboot (inside the Git folder)

# Removing Seeed audio card and using recommended USB Mini Speaker & USB Microphone
1. cd ~/seeed-voicecard/
2. sudo ./uninstall.sh
3. sudo poweroff

Now you can remove Pi shield and plug in the USB speaker and microphone.

## Configure USB Speaker and USB Microphone
Follow instructions on this page: [Configure and Test the Audio](https://developers.google.com/assistant/sdk/guides/service/python/embed/audio)

Make sure you increase the record volume of the microphone to 100%. Also set the output of the speaker at 80%.

## Setting up PulseAudio
1. sudo apt install -y pulseaudio paprefs pavucontrol
2. sudo reboot
3. cd /etc/pulse
4. sudo cp daemon.conf daemon.conf.bak
5. sudo cp default.pa default.pa.bak

@TODO: Add configs

## Installing Motor Hat software
https://learn.adafruit.com/adafruit-dc-and-stepper-motor-hat-for-raspberry-pi/installing-software
https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi

# Creating mouth script
This is my code for now...

```python
#!/usr/bin/env python

"""
animatronic_mouth.py

This script animates a motorized mouth on a Raspberry Pi GPIO pin so that it
appears to be speaking alongside the audio on the specified PulseAudio source
(which usually should be a sink's monitor).

Find PA_SOURCE with `pactl list` and look for a monitor device that corresponds
to your output device.

See here for a detailed discussion: https://albertarmea.com/post/alexa-tree/
"""

import atexit
import time
import struct
import subprocess
from adafruit_motorkit import MotorKit

def turnoffmotor():
  kit.motor1.throttle = 0

atexit.register(turnoffmotor)
kit = MotorKit()

PA_SOURCE = "alsa_output.usb-Generic_USB2.0_Device_20130100ph0-00.analog-stereo.monitor"
MOUTH_STATE = 'closed'
SAMPLE_ARRAY = []

# We're not playing this stream back anywhere, so to avoid using too much CPU
# time, use settings that are just high enough to detect when there is speech.
PA_CHANNELS = 1 # Mono
PA_RATE = 1000 # Hz
PA_LATENCY=4

SAMPLE_THRESHOLD = 2
COUNTER = 0

# Capture audio using `pacat` -- PyAudio looked like a cleaner choice but
# doesn't support capturing monitor devices, so it can't be used to capture
# system output.
parec = subprocess.Popen(["/usr/bin/pacat", "--record", "--device="+PA_SOURCE,
    "--rate="+str(PA_RATE), "--channels="+str(PA_CHANNELS)], stdout=subprocess.PIPE)

while not parec.stdout.closed:
    # Mono audio with 1 byte per sample makes parsing trivial
    sample = ord(parec.stdout.read(1)) - 120
    COUNTER += 1
    SAMPLE_ARRAY.append(sample)

    if COUNTER % 50 == 0:
      sample_average = sum(SAMPLE_ARRAY, 0.0) / len(SAMPLE_ARRAY)
      #print(sample_average)

      if abs(sample_average) >= SAMPLE_THRESHOLD and MOUTH_STATE == 'closed':
        #print('open')
        kit.motor1.throttle = 1.0
        MOUTH_STATE = 'open'
      elif abs(sample_average) < SAMPLE_THRESHOLD and MOUTH_STATE == 'open':
        #print('close')
        kit.motor1.throttle = 0
        MOUTH_STATE = 'closed'

      SAMPLE_ARRAY = []
      COUNTER = 0
```

## Setting up WiFi (store WiFi credentials)
See: https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md

Edit file `sudo nano /etc/wpa_supplicant/wpa_supplicant.conf`

Use `wpa_passphrase "SSID_HERE"` command, this will generate output that can be used in the `wpa_supplicant.conf` file.

# Modify hotword script
So Google delivers a better script for the hotword project. So we use that script as default and implement the billy script into it.

.....

## Setting up script after boot and WiFi connection
More info: https://raspberrypi.stackexchange.com/questions/78991/running-a-script-after-an-internet-connection-is-established

### Google Assistant script

`sudo systemctl edit --force --full start-google-assistant.service`

Paste the following code

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

Check stutus of the service
`systemctl status start-google-assistant.service`

Enable the service
`sudo systemctl enable my_script.service`

Start the service
`sudo systemctl start my_script.service`

### Mouth script

`sudo systemctl edit --force --full start-mouth-script.service`

Paste the following code

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

Check stutus of the service
`systemctl status start-mouth-script.service`

Enable the service
`sudo systemctl enable start-mouth-script.service`

Start the service
`sudo systemctl start start-mouth-script.service`
