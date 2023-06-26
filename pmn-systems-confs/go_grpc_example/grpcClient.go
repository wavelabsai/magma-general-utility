package main

import (
        "context"
        "fmt"
        protos "magma/lte/cloud/go/protos"
        models "magma/lte/cloud/go/protos/models"
        structpb "google.golang.org/protobuf/types/known/structpb"
        "google.golang.org/grpc"
        "google.golang.org/protobuf/encoding/protojson"
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

type Sequence struct {
        SqnScheme   string
        Sqn         string
        LastIndexes map[string]int32
        IndLength   int32
        DifSign     int32
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
        //request := PMNConverter()
        request := &protos.PMNSubscriberData{
                Am1:          GetAccessAndMobilitySubscription(),
                AuthSubsData: GetAuthenticationSubscription(),
                SmData:       GetSmData(),
        }
        client.PMNAddSubscriberConfig(context.Background(), request)
}

// func PMNConverter() *protos.PMNSubscriberData {
//      return &protos.PMNSubscriberData{
//              Am1:          GetAccessAndMobilitySubscription(),
//              AuthSubsData: GetAuthenticationSubscription(),
//      }
// }

func GetAccessAndMobilitySubscription() *models.AccessAndMobilitySubscriptionData {
        var gpsisValue = []string{"Client", "Magma"}
        var dSingleNssai = []DefaultSingleNssais{{Sst: 1, Sd: "0002"}, {Sst: 2, Sd: "003"}}
        var supportedFeature = "5G core"
        ambrval := Subs_ambr{"200 Mbps", "100 Mbps"}
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

        return &models.AccessAndMobilitySubscriptionData{
                SupportedFeatures:      supportedFeature,
                Gpsis:                  gpsisValue,
                SubscribedUeAmbr:       sUeAmbr,
                Nssai:                  nssai,
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
}

func GetAuthenticationSubscription() *models.AuthenticationSubscription {
        var ktab = "AUTHSUBS"
        var algorithmId = "MILENAGE.1"
        sequence_num := Sequence{"NON_TIME_BASED", "000000000ac0", map[string]int32{}, 5, 0}
        var encOpcKey = "A3782F73B17811F4043EE66EBFD62519"
        var encTopcKey = "5E4AB35891375D2AEE812E67C309A629"
        var supi = "SUPI"

        return &models.AuthenticationSubscription{
                KTAB:                  ktab,
                EncPermanentKey:       "",
                ProtectionParameterId: "none",
                SequenceNumber: &models.SequenceNumber{
                        SqnScheme:   sequence_num.SqnScheme,
                        Sqn:         sequence_num.Sqn,
                        LastIndexes: sequence_num.LastIndexes,
                        IndLength:   sequence_num.IndLength,
                        //DifSign:     models.Sign.Sign_Sign_NEGATIVE,
                },
                AuthenticationManagementField: "8000",
                AlgorithmId:                   algorithmId,
                EncOpcKey:                     encOpcKey,
                EncTopcKey:                    encTopcKey,
                VectorGenerationInHss:         true,
                N5GcAuthMethod:                &models.AuthMethod{},
                RgAuthenticationInd:           true,
                Supi:                          supi,
        }
}

func GetSmData() *protos.SmData {
        var dnnConfigurations1 = &models.DnnConfiguration {
                                  PduSessionTypes: &models.PduSessionTypes{
                                                  DefaultSessionType: "IPV4",
                                                  AllowedSessionTypes: []string{"IPV4V6"},},
                                  Internal_5GQosProfile: &models.SubscribedDefaultQos{
                                                       Internal_5Qi: 9,
                                                       Arp: &models.Arp{
                                                            PriorityLevel: 7,
                                                            PreemptCap: "NOT_PREEMPT",
                                                            PreemptVuln: "PREEMPTABLE",},},
                                  SessionAmbr: &models.Ambr{Uplink: "200 Mbps", Downlink: "100 Mbps"},
                                  SscModes: &models.SscModes{
                                           DefaultSscMode: "SSC_MODE_1",
                                           AllowedSscModes: []string{"SSC_MODE_1", "SSC_MODE_2", "SSC_MODE_3"},},
                               }

        var dnnConfigurations2 = &models.DnnConfiguration {
                                  PduSessionTypes: &models.PduSessionTypes{
                                                    DefaultSessionType: "IPV4",
                                                    AllowedSessionTypes: []string{"IPV4V6"},},
                                  Internal_5GQosProfile: &models.SubscribedDefaultQos{
                                                        Internal_5Qi: 5,
                                                        Arp: &models.Arp{
                                                             PriorityLevel: 7,
                                                             PreemptCap: "NOT_PREEMPT",
                                                             PreemptVuln: "PREEMPTABLE",},},
                                  SessionAmbr: &models.Ambr{Uplink: "1 Mbps", Downlink: "1 Mbps"},
                                  SscModes: &models.SscModes{
                                            DefaultSscMode: "SSC_MODE_1",
                                            AllowedSscModes: []string{"SSC_MODE_1", "SSC_MODE_2", "SSC_MODE_3"},},
                               }

         var sessionManagementSubscriptionData = &models.SessionManagementSubscriptionData {
                                                  DnnConfigurations: map[string]*models.DnnConfiguration {
                                                    "apn1": dnnConfigurations1,
                                                    "ims": dnnConfigurations2,
                                                  },
                                                  SingleNssai: &models.Snssai{Sst: 1, Sd: "000001",},}
        return &protos.SmData{
                 PlmnSmData: map[string]*structpb.ListValue {
                     "001-01": {
                         Values: []*structpb.Value {
                                 { Kind:  &structpb.Value_StringValue{StringValue:
                                 protojson.Format(sessionManagementSubscriptionData)}},
                         },
                     },
                 },
              }
}
