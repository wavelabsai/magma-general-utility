# This is the README for the test program

## Building the solution
sudo docker compose build

## Launching of the main docker container
sudo docker compose up medical_db -d

## Launching the test utility
sudo docker compose up validate_medical_db -d

## Output and report
* Outut will be stored in test/report

## Additional information
* pytest logs can be enabled by following method

```
import logging
logging.info
pytest -o log_cli=true --log-cli-level=INFO --log-format="%(asctime)s %(levelname)s %(message)s" --log-date-format="%Y-%m-%d %H:%M" --junitxml=./output.xml
```

* Contents of response can be checked by response.text

## Unit test specific docker compose
* sudo docker compose up unittest_medical_db -d
* python3 -m unittest utmdeicaldb.py 
