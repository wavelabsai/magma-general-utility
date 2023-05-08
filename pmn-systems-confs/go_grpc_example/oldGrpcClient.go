package main

import (
	"context"
	"fmt"
	"go_package/protos"
	"go_package/protos/models"
	"google.golang.org/grpc"
	//"github.com/go-openapi/swag"
	"log"
)

func main() {
	fmt.Println("Hello client ...")

	opts := grpc.WithInsecure()
	cc, err := grpc.Dial("localhost:50051", opts)
	if err != nil {
		log.Fatal(err)
	}
	defer cc.Close()

	client := protos.NewPMNSubscriberServiceClient(cc)
	request := &protos.PMNSubscriberData{
		          SubscriberUeAmr: &models.Ambr {
			      Uplink: "200 Mbps",
			      Downlink: "100 Mbps",
		          },
                   }
	client.PMNSubscriberConfig(context.Background(), request)
}
