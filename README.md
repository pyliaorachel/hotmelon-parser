## Usage

- Structure of thesis
	```
	<thesis>.tex
	<figures>/
	```

- Run program
	- `python3 hot_melon.py <path-to-latex-file>`  

- Run server
	- `python3 server.py`

## Thesis File API

```
POST /thesis
	- Request 
		- Header
			'Content-Type': 'application/octet-stream' # binary file
		- Body
			<zip file>
	- Response
		- Header
			'Content-Type': 'text/plain'
		- Body
			<key to DB>
```