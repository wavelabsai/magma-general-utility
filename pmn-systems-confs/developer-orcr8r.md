## Running all the build, lint and pre-commit tests
[dir] orc8r/cloud/docker
- sudo PWD=$PWD ./build.py --m    ```(will take to the docker shell with all required tools pre-installed)```
  
      - make test       (for unit testing)
      - make lint       (for lint testing)    
      - make precommit  (automatically fixes the liniting issues)
      - make fullgen    (to generate swaggergen's and debug for any errors)

## Making complete builds
[dir] orc8r/cloud/docker
- sudo PWD=$PWD ./build.py --all   ```(Complete build)```

## To sync protos between Orc8r and AGW
[dir] orc8r/cloud/docker
- sudo PWD=$PWD ./build.py --g      ```(will generate pb.go files that can be used by orc8r code)```

## Run the lint test on AGW Python code
```export MAGMA_ROOT=/home/vagrant/pmn-systems/
cd lte/gateway/python/
./precommit.py
./precommit.py --lint -p lte/gateway/python/magma/subscriberdb/client.py
```
