## Orchestrator
### To Build: 
- sudo PWD=$PWD ./build.py --all 

### To Generate pb.go or swaggergen files: 
- sudo PWD=$PWD ./build.py -g 

### Unit Test: 
- sudo PWD=$PWD ./build.py -m 
- It will redirect to /src/magma/orc8r/cloud 
    - make test

### Lint test:
- sudo PWD=$PWD ./build.py --lint

## CWAG
### Unit Test:
- Directory: feg/gateway/docker
- sudo ./build.py --test
- If the above step failes then
    - sudo docker exec -it test bash
    - go install gotest.tools/gotestsum@latest
    - make test

### Lint Test
- Directory: feg/gateway/docker
- sudo ./build.py --lint
- golangci-lint run -c ~/PMN-SYSTEMS/pmn-systems//.golangci.yml (from feg/radius/src)
- If Lint test fails use the following command to fix the regular errors:
- gofmt -s -w ./gateway/services/aaa/servicers/accounting.go (from Host Machine need to fix for every file which got lift errors)

### To run all the test files in a specific directory, go to that Dir
- go test -v ./...

### To run a specific unit test, go to that file Path
- go test -v -run <*test_case_name*> 
