
import logging.config

import os
import sys
import serial
import time

import requests
from requests.exceptions import ConnectionError
from requests.packages.urllib3.exceptions import MaxRetryError
from requests.packages.urllib3.exceptions import ProxyError as urllib3_ProxyError

import spotipy
import spotipy.util as util

from spotibox import settings

logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)

def main():
    time_since_pause=time.time()
    previous_playing=""
    currently_playing=""
    token = ""
    deviceId=""

    if len(sys.argv) > 1:
        username = sys.argv[1]
        client_id = sys.argv[2]
        client_secret = sys.argv[3]
        redirect_uri = sys.argv[4]
        device_name = sys.argv[5]

        token = util.prompt_for_user_token(username, settings.SPOTIFY_SCOPE, client_id, client_secret, redirect_uri, settings.SPOTIFY_USER_TOKEN_STORE)
    else:
        log.info( "Usage: %s username client_id client_secret redirect_uri device_name", sys.argv[0])
        sys.exit()

    if token:
        spotify_client = spotipy.Spotify(auth=token)

        rm6300 = serial.Serial(settings.RM6300_SERIAL_PORT, 9600, timeout=1.0)

        while True:
            if deviceId == "":
                time.sleep(5)
                os.system("aplay "+os.path.normpath(os.path.join(os.path.dirname(__file__), '../resources/search_device.wav')))
                try:
                    spotify_devices = spotify_client.devices()
                except ConnectionError:
                    log.warning("Can not reach %s:%s", settings.SPOTIBOX_SERVER_HOST, settings.SPOTIBOX_SERVER_PORT)
                    continue
                except MaxRetryError:
                    log.warning("Can not reach %s:%s", settings.SPOTIBOX_SERVER_HOST, settings.SPOTIBOX_SERVER_PORT)
                    continue
                 
                log.info('Wait for device %s to appear in device list: %s', device_name, spotify_devices)

                for device in spotify_devices["devices"]:
                    if device["name"]==device_name:
                        log.info("found device")
                        deviceId=device["id"]
                        os.system("aplay "+os.path.normpath(os.path.join(os.path.dirname(__file__), '../resources/found_device.wav')))
                continue

            rfid = ""

            read_byte = rm6300.read()

            if read_byte == "\x02".encode():
                # reading EM4100 protocol (125khz RFID)
                # http://www.priority1design.com.au/em4100_protocol.html
                # 8 bit version       	D00 	D01 	D02 	D03 	 P0  	
                # or customer ID. 		D04 	D05 	D06 	D07 	 P1  	
                #				        D08 	D09 	D10 	D11 	 P2  	Each group of 4 bits
                #				        D12 	D13 	D14 	D15 	 P3  	is followed by an Even
                # 32 Data Bits 	        D16 	D17 	D18 	D19 	 P4  	parity bit
                #				        D20 	D21 	D22 	D23 	 P5  	
                #				        D24 	D25 	D26 	D27 	 P6  	
                #				        D28 	D29 	D30 	D31 	 P7  	
                #				        D32 	D33 	D34 	D35 	 P8  	
                #       				D36 	D37 	D38 	D39 	 P9  	
                # 4 column Parity bits 	PC0 	PC1 	PC2 	PC3 	 S0 	   1 stop bit (0)     

                # reading is done as hex value

                for Counter in range(12):
                    rfid += str(rm6300.read().decode())

                # remove P0 and P1 and P8 and P9
                rfid = rfid[4:10]
                rfid = str(int(rfid,16))

                if previous_playing == rfid and (time.time() - time_since_pause) < 5 :
                    log.info("Resume Playback!")
                    try:
                        spotify_client.start_playback(deviceId, None, None, None)
                        currently_playing = previous_playing    
                        previous_playing = ""
                    except ConnectionError:
                        log.warning("Can not reach spotify api")
                        continue
                    except MaxRetryError:
                        log.warning("Can not reach spotify api")
                        continue
                    continue

                if currently_playing != rfid:
                    try:
                    	r = requests.get(settings.SPOTIBOX_SERVER_HOST + ":" + settings.SPOTIBOX_SERVER_PORT + "/api/box/mapping/" + rfid)
                    except ConnectionError:
                        log.warning("Can not reach %s:%s", settings.SPOTIBOX_SERVER_HOST, settings.SPOTIBOX_SERVER_PORT)
                    except MaxRetryError:
                        log.warning("Can not reach %s:%s", settings.SPOTIBOX_SERVER_HOST, settings.SPOTIBOX_SERVER_PORT) 

                    if r.status_code == 200:
                        album_meta = r.json()

                        if album_meta["rfid"]==rfid and currently_playing != rfid:
                            # start_playback(device_id=None, context_uri=None, uris=None, offset=None)
                            # Start or resume user’s playback.
                            # Provide a context_uri to start playback or a album, artist, or playlist.
                            # Provide a uris list to start playback of one or more tracks.
                            # Provide offset as {“position”: <int>} or {“uri”: “<track uri>”} to start playback at a particular offset.
                            # Parameters:
                            #     device_id - device target for playback
                            #     context_uri - spotify context uri to play
                            #     uris - spotify track uris
                            #     offset - offset into context by index or track

                            spotify_uri = str(album_meta["uri"])
                            log.info( "Provided Spotify_uri: %s", spotify_uri )

                            # examples for spotify_uris
                            # spotify:track:1QXZfEOtzM3Mzoy3VRTdXv
                            # spotify:album:0w0yDx8rVJeCtDbzovPveH

                            # we have to call playback depending on the track elements...

                            spotify_uri_elements = spotify_uri.split(":")

                            if len(spotify_uri_elements) >= 1:
                                spotify_uri_type = spotify_uri_elements[1]
                                
                                if spotify_uri_type == 'track':
                                    log.info("Play Track")
                                    try:
                                        spotify_client.start_playback(deviceId, None,[spotify_uri],None)
                                        currently_playing=rfid
                                    except ConnectionError:
                                        log.warning("Can not reach spotify api")
                                    except MaxRetryError:
                                        log.warning("Can not reach spotify api")                                 

                                elif spotify_uri_type == 'album':
                                    log.info("Play Album")
                                    try:  
                                        spotify_album_offset = album_meta['offset']
                                        offset={}
                                        offset['position'] = album_meta['offset']
                                        spotify_client.start_playback(deviceId, spotify_uri, None, offset)
                                        currently_playing = rfid
                                    except ConnectionError:
                                        log.warning("Can not reach spotify api")
                                    except MaxRetryError:
                                        log.warning("Can not reach spotify api")                                 

                                else:
                                    log.warning("Not handled URI type: %s for uri %s ",spotify_uri_type, spotify_uri)
                            else:
                                log.warning("Unkown URI format: %s ", spotify_uri)


                                # else do nothing
            else:
                # log.info("Nothing found.")
                if read_byte=="".encode() and currently_playing != "":
                    #removed rfid card
                    try:
                        spotify_client.pause_playback(deviceId)
                        previous_playing=currently_playing
                        currently_playing=""
                        time_since_pause=time.time()
                    except ConnectionError:
                        log.warning("Can not reach spotify api")
                    except MaxRetryError:
                        log.warning("Can not reach spotify api")                                 
            continue

    else:
        log.error('Cant get token for {} -> Quit'.format(username))


if __name__ == "__main__":
    main()
    

