# box_server
Simple Flask Server to save and provide RFID-Uri Mapping to my client boxes

# Setup

````
$ cd /path/to/workspace/
$ git clone https://github.com/jebox/spotibox
$ cd spotibox
$ cd backend
````

Create a virtual Python environment and install dependencies:

````
$ virtualenv -p /usr/bin/python3 env
$ source env/bin/activate
(env) $ pip install -r requirements.txt
````
````
(env) $ python setup.py develop
(env) $ python box_rest_api/app.py
````
