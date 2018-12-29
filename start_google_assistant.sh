#!/bin/bash

BIN_ROOT="/usr/bin"
APPLICATION_ROOT="/home/pi/kaliber-billy-bassistant"

# Start application
echo "Starting startup_motors.py"
$BIN_ROOT/python3 $APPLICATION_ROOT/startup_motors.py

echo "Starting Google Assistant"
$BIN_ROOT/python3 -m hotword --project-id billybassistant --device-model-id billybassistant-billybassistant2-ef1kwz
