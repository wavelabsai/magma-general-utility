package main

import (
    "context"
    "fmt"
    protos "magma/lte/cloud/go/protos"
    models "magma/lte/cloud/go/protos/models"
    "google.golang.org/grpc"
    //"github.com/go-openapi/swag"
    "log"
)
type DefaultSingleNssais struct {
        Sst int
        Sd  string
}

type Subs_ambr struct {
        Ul_ambr string
        Dl_ambr string
}

func main() {
 fmt.Println("Hello client ...")

 opts := grpc.WithInsecure()
 cc, err := grpc.Dial("localhost:50051", opts)
 if err != nil {
  log.Fatal(err)
 }
 defer cc.Close()

 client := protos.NewPMNSubscriberConfigServicerClient(cc)
 var sgsiValue = []string{"Client", "Magma"}
 var dSingleNssai = []DefaultSingleNssais{{Sst: 1, Sd: "0002"}, {Sst: 2, Sd: "003"}}
 var supportedFeatures = "5G core"
 stored_ambr_val := Subs_ambr{"200 Mbps", "100 Mbps"}
 request := PMNConverter(supportedFeatures, stored_ambr_val, sgsiValue, dSingleNssai)
 client.PMNSubscriberConfig(context.Background(), request)
}

func PMNConverter(supportedFeature string, ambrval Subs_ambr, gpsisValue []string, dSingleNssai []DefaultSingleNssais) *protos.PMNSubscriberData {
        defaultNssaiData := []*models.Snssai{}
          for _, value := range dSingleNssai {
                  temp := new(models.Snssai)
                  temp.Sd = value.Sd
                  temp.Sst = int32(value.Sst)
                  defaultNssaiData = append(defaultNssaiData, temp)
          }

        sUeAmbr := &models.AmbrRm{
                Downlink: ambrval.Ul_ambr,
                Uplink:   ambrval.Dl_ambr,
        }
        nssai := &models.Nssai{
                DefaultSingleNssais: defaultNssaiData,
                SingleNssais:        nil,
        }

        amsd := &models.AccessAndMobilitySubscriptionData{
                SupportedFeatures: supportedFeature,
                Gpsis:             gpsisValue,
                SubscribedUeAmbr:  sUeAmbr,
                Nssai:             nssai,
                InternalGroupIds:       []string{},
                ForbiddenAreas:         nil,
                ServiceAreaRestriction: nil,
                PlmnAmData:             nil,
                RfspIndex:              76,
                SubsRegTimer:           488,
                UeUsageType:            43,
                MicoAllowed:            true,
                SubscribedDnnList:      []string{},
        }
        return &protos.PMNSubscriberData{
                Am1: amsd,
        }
}
