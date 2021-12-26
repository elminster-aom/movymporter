# Coding Exercise: Parse & Post
# Basic description
From a CSV file containing movie metadata that we want to "import" into a web service using a supplied endpoint. This endpoint only accepts one object at
a time. 
Since data can be inaccurate, this code will run the main transformations needed for importing as much data (movies) as possible

## Prerequisites 
In addition to cloning this repository, you will need network access to install the application dependencies as part of the setup process, including `docker`.

# How it works
Our Python code `movymporter` reads a CSV file (declared on `CSV_IN`, see section bellow _How to set up and run_), runs transformations for 
increase the data accuracy (NOTE: If original data cannot be properly transformed, it will be substitute by `None`) and sends it to a WebServer, through a POST call.


# How to install
1. Clone or download a ZIP of this project, e.g.:
```shell
$ git clone git@github.com:github-interviews/elminster-aom-parse-and-post-platform-ops-eng.git
```
1. Ensure that you have the right version of Python (v3.9+)
1. Create and activate Python Virtual Environment and install required packages, e.g.:
```shell
$ python3 -m venv elminster-aom-parse-and-post-platform-ops-eng \
&& source elminster-aom-parse-and-post-platform-ops-eng/bin/activate \
&& python3 -m pip install --requirement elminster-aom-parse-and-post-platform-ops-eng/requirements.txt
```
4. Move into the new environment:
```shell
$ cd elminster-aom-parse-and-post-platform-ops-eng
```
# How to set up and run
1. Run `bin/setup`. This will run a web server at http://localhost:9009. Please leave this running! If you are using Windows, run all commands in the `bin` directory using PowerShell. For example, instead of `bin/setup` run `pwsh bin\setup`.

1. In a new terminal window, make a test POST call to the server.

  If you are using Linux or Mac OS the command is:
  ```bash
  curl http://localhost:9009/movies -d '{"year":1997, "length": 123, "title": "Face Off", "subject": "action", "actor": "Cage, Nicholas", "actress": "Allen, Joan", "director": "Woo, John", "popularity": 82, "awards": "No", "image": "NicholasCage.png"}'
  ```
  If you are using Windows the command is:
  ```
  Invoke-RestMethod -Method POST -Uri http://localhost:9009/movies -Body '{"year":1997, "length": 123, "title": "Face Off", "subject": "action", "actor": "Cage, Nicholas", "actress": "Allen, Joan", "director": "Woo, John", "popularity": 82, "awards": "No", "image": "NicholasCage.png"}'
  ```

  After you do this, you should see the request show up in the web server's output.

1. (optional) Check the monitoring endpoint: `curl http://localhost:9009/metrics` (`Invoke-RestMethod -Method GET -Uri http://localhost:9009/metrics` for Windows)
  - You should see 1 count for `sink_post_total`
  - Reset the metrics count by calling `bin/reset` (`pwsh bin\reset` for Windows) in the same window as the log

1. All available settings are based on an environment variables file in the home of our application. For its creation you can use this template:
```shell
$ nano .env

# copy-paste this content:
LOG_LEVEL = INFO
CSV_IN = backup.csv
URL_OUT = http://localhost:9009/movies
STOP_ON_ERRORS = 0

$ chmod 0600 .env
```
Where variables mean:
- `LOG_LEVEL`: Output detail level, possible values are (from more to less verbose): `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` and `NOTSET`
- `CSV_IN`: CSV File (including relative or absolute path) with data source
- `URL_OUT`: Full URL (including POST hook) for register data in our WebServer (DB)
- `STOP_ON_ERRORS`: Data import will stop after first registry error if value is different than `0`

1. Start the importing, run main program `movymporter`:
```shell
$ python3 movymporter
```

## Helper Commands
| Command | Description |
| --- | --- |
| `bin/setup` | Builds and start the service that you'll be writing a script against |
| `bin/reset` | Restarts the service to reset prometheus metrics |
| `bin/log` | Display logs from server |
| `bin/clean` | Stops and remove docker containers |
| `bin/destroy` | Destroy all local docker artifacts. *Use with caution* |


# Additional considerations
1. Only Unix-like systems are supported
2. The code has been tested with Python 3.9.4
3. For a detailed list of Python modules check out the [requirements.txt]
4. Concepts like tunning or replication are out of the scope of this exercise

# Areas of improvement
* `aiocsv` functionality needs to be provided by this code. Some additional transformations needs to operate the full
row as a binary string, before converting them to a dictionary
* Take profit of _Prometheus_ availability for increase visibility of the application, e.g.:
    - Ratio of total of movies registered against total of movies provided
    - processing time of the 3 phases, reading, transformation and posting
    - Ratio of movies with incomplete fields against total of movies provided
    - ...
