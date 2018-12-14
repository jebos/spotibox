# Setup Guide

## Precondition
 * librespot is installed (+raspotify). You know that it works if you can find your device in spotify and play songs from remote
 * apt install python-pip
 * pip install setuptools
 * pip install wheel
 * pip install spotipy #follow https://spotipy.readthedocs.io/en/latest/#authorized-requests  (THIS IS IMPORTANT!)
                       # this app using Authorization Code Flow to authorize as a long running application,
 
 > pip install spotipy is outdated... if not > 2.0 then use master...
 
 * pip install git+https://github.com/plamere/spotipy.git --upgrade

## Running
 
# Setup

````
$ cd /path/to/workspace/
$ git clone https://github.com/jebox/spotibox
$ cd spotibox
$ cd controller
````

Create a virtual Python environment and install dependencies:

````
$ virtualenv -p /usr/bin/python3 env
$ source env/bin/activate
(env) $ pip install -r requirements.txt
````
````
(env) $ python setup.py develop
(env) $ python spotibox/app.py
````


