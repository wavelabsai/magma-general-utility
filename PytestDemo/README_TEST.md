# This is the README for the test program

## Building the solution
sudo docker compose build

## Launching of the main docker container
sudo docker compose up medical_db -d

## Launching the test utility
sudo docker compose up validate_medical_db -d

## Output and report
* Outut will be stored in test/report
