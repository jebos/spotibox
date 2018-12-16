# spotibox
A Spotify Connect Speaker for my Kids

## General Setup
### Hardware

* Raspberry Pi Zero W
* 8GB SD Card
* Speaker Phat + Custom Speaker (5W, 4o)
* RMD6300 RFID Card Reader (125kHz, serial port)
* RFID Cards

### Software
* DietPi
* Raspotify
* librespot-org (which basically comes with raspotify)
* python 3.x

## How to run

0. Make sure you can run your raspberry as connected speaker (you wont need anything from here to do that). You can controll your raspberry with your Spotify App.

1. Clone this repo, follow the readme in controller and backend.
2. To automate the startup create systemd service files

## Notes
To run the controller, you will provide the following informations:
Spotfy-Username,
Client-Id,
Client-Secret
redirect-uri
device-name.

The first time you run the contoller you will get a link to follow in your browser, just put the resulting / redirect link in the console to authenitcate your client.
You only need to do this once.

That's it.