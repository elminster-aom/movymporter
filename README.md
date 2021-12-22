# Coding Exercise: Parse & Post

## Prerequisites 
In addition to cloning this repository, you will need network access to install the application dependencies as part of the setup process, including `docker`.

## Expectations
We ask that you spend no more than ~2-3 hours on this exercise. We value your time and don't want to set unreasonable expectations on how long you should work on this exercise.

We ask that you complete this exercise to build a service on your own time, rather than in an in-person interview because the Ops Engineering team at GitHub is distributed, and async communication/collaboration is highly valued (though we love to pair program too!)

## Scenario
We have a CSV file containing movie metadata that we want to "import" into a web service using a supplied endpoint. This endpoint only accepts one object at a time. We don't know how accurate the data is so we'll need to validate it. But we still want to send as much valid data as possible into the server. Our priority is to get a working import solution first. If we have time, we can optimize process. We'll have plenty of time to discuss improvements during a code review / retro interview.

Write and submit a PR implementing this behavior; please use whatever language you are comfortable with and add comments and details in the PR explaining your approach.

## Setup
  
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

## Helper Commands

| Command | Description |
| --- | --- |
| `bin/setup` | Builds and start the service that you'll be writing a script against |
| `bin/reset` | Restarts the service to reset prometheus metrics |
| `bin/log` | Display logs from server |
| `bin/clean` | Stops and remove docker containers |
| `bin/destroy` | Destroy all local docker artifacts. *Use with caution* |


## How it works
The main program `tagsdump.py` has two execution modes:
```shell
$ python3 movymporter
```


## How to install
1. Clone or download a ZIP of this project, e.g.:
```shell
$ git clone git@github.com:github-interviews/elminster-aom-parse-and-post-platform-ops-eng.git
```
2. Ensure that you have the right version of Python (v3.9, see below)
3. Create and activate Python Virtual Environment and install required packages, e.g.:
```shell
$ python3 -m venv movymporter \
&& source movymporter/bin/activate \
&& python3 -m pip install --requirement movymporter/requirements.txt
```
4. Move into the new environment:
```shell
$ cd movymporter
```

## Additional considerations
1. Only Unix-like systems are supported
2. The code has been tested with Python 3.9.4
3. For a detailed list of Python modules check out the [requirements.txt]
4. Concepts like tunning or replication are out of the scope of this exercise

## Areas of improvement
* In Build
