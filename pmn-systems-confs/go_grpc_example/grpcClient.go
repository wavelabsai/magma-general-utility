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
                 Amsd: &models.AccessAndMobilitySubscriptionData {
                       SupportedFeatures: "5G Core",
                       Gpsis: []string{"msisdn-001011234567534"},
                       InternalGroupIds: []string{"abcd1234-567-89-abcd"},
                       Nssai: &models.Nssai {
                           DefaultSingleNssais: []*models.Snssai {
                               {
                                   Sst: 1,
                                   Sd: "000001",
                               },
		           },
                           SingleNssais: []*models.Snssai {
                               {
                                   Sst: 1,
                                   Sd: "000001",
                               },
                               {
                                   Sst: 3,
                                   Sd: "000003",
                               },
                           },
                       },

		       SubscribedUeAmbr:&models.AmbrRm {
			   Downlink: "2000 Mbps",
                           Uplink: "1000 Mbps",
		       },
                       SubscribedDnnList: []string {"apn3"},
                       ForbiddenAreas:  []*models.Area {
			   {
                               Tacs: []string {"00069"},
		           },
		       },
		       ServiceAreaRestriction: &models.ServiceAreaRestriction {
                           RestrictionType: "ALLOWED_AREAS",
		       },
                 },
             }

 client.PMNSubscriberConfig(context.Background(), request)
}
