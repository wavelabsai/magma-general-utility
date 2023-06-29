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
