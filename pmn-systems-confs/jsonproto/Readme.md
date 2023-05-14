# Experiments with openapi, json and protobuf

## Tools for various purposes

### For converting between Swagger & Openapi3
* https://github.com/LucyBot-Inc/api-spec-converter
* Pros:
  - Easy to install and use
* Cons:
  - Converting from swagger to openapi3 does not gives accurate
    results especally for component and schem.
* Installation & Running
  - Checkout the code
  - sudo docker build . -t opengenerator-api
  - sudo docker run -it opengenerator-api bash
  - sudo docker run -v ${PWD}/standard:/app/standard -it opengenerator-api bash

```
Usage: 
   api-spec-converter --from=swagger_2 --to=openapi_3  --syntax=yaml --order=alpha ./swagger-common.yml > orc8r-swagger-common.yml
   api-spec-converter --from=swagger_2 --to=openapi_3  --syntax=yaml --order=alpha ./swagger.v1.yml > ConvertPolicy.yml
```


### For creating protobuf from 5G Core yamls
  - Use openapi-generator-cli for the purpose.
  - Use the Docker file attached
  - Usage (Pre-requsites - mkdir OUT_PROTOBUF
```
   git clone https://github.com/jdegre/5GC_APIs.git
   cd 5GC_APIs
   git checkout Rel-16

   OPTION-1:
      java -jar openapi-generator-cli.jar generate -i  TS29503_Nudm_SDM.yaml -g openapi-yaml  -o OUT_YAML

      java -jar openapi-generator-cli.jar generate -i  TS29503_Nudm_SDM.yaml -g protobuf-schema   -o OUT_PROTOBUF

      root@0b4ef667ca7e:/app/5GC_APIs/OUT_PROTOBUF# ls
      README.md  models  services
      root@0b4ef667ca7e:/app/5GC_APIs/OUT_PROTOBUF# ls models/*proto | wc -l
      221
      root@0b4ef667ca7e:/app/5GC_APIs/OUT_PROTOBUF#
   
   OPTION-2:
       java -jar /openapi-generator-cli.jar  generate -i  TS29505_Subscription_Data.yaml -g protobuf-schema  -o /app/standard/gen_protos/OUT_PROTOBUF
```

### Additional tools for bundling, removing refs
   - npm install -g @apidevtools/swagger-cli
   
### Creating protobuf files
* Install pip3 : apt-get -y install python3-pip
* Install grpc tools : pip install grpcio-tools==1.46.3
* Directory layout
   - All protos : /app/5GC_APIs/OUT_PROTOBUF/models
   - Encasulating proto : /app/5GC_APIs/OUT_PROTOBUF/SubscriberDB

```
Root : /app/5GC_APIs/OUT_PROTOBUF
CreateDir : mkdir /app/5GC_APIs/OUT_PROTOBUF/gen_protos/
python3.9 -m grpc_tools.protoc -I=. --python_out=./gen_protos models/*
python3.9 -m grpc_tools.protoc -I=. --python_out=./gen_protos dbsubscriber/*

root@731ad8c93c1d:/app/5GC_APIs/OUT_PROTOBUF# ls gen_protos/
dbsubscriber  models

```
