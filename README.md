# jserver
A dummy server for testing purposes


- How to use

* install dependencies using pip
pip install -r requirements.txt

* start
python main.py

Three endpoints are available on any ip interface (0.0.0.0) on port 7777

/token (serves a new token in json format)

/api1 needs the token as bearertoken to return a 200

/api2 same as api1

