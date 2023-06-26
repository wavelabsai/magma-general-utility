package main

import (
        "context"
        "fmt"
        "os"
        //"go_package/protos/models"
        protos "magma/lte/cloud/go/protos"
        "google.golang.org/grpc"
        "log"
        "net"
        "google.golang.org/protobuf/encoding/protojson"
        "google.golang.org/protobuf/proto"
)

type server struct {
    protos.UnimplementedPMNSubscriberConfigServicerServer
}


func example3(m proto.Message) string {
   return protojson.Format(m)
}

var (
    outfile, _ = os.Create("/home/vagrant/GO_GRPC/test.log") // update path for your needs
    l      = log.New(outfile, "", 0)
)

func (*server) PMNAddSubscriberConfig(ctx context.Context, request *protos.PMNSubscriberData) (*protos.Void, error) {
  //uplink := request.models.Ambr
  //downlink := request.subscriberUeAmr.downlink
  //log.Printf(example3(request))
  fmt.Printf(example3(request))
  response := &protos.Void{}

  return response, nil
}


func main() {
        address := "0.0.0.0:50051"
        lis, err := net.Listen("tcp", address)
        if err != nil {
                log.Fatalf("Error %v", err)
        }
        fmt.Printf("Server is listening on %v ...", address)

        s := grpc.NewServer()
        protos.RegisterPMNSubscriberConfigServicerServer(s, &server{})

        s.Serve(lis)
}
