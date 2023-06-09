#!/usr/bin/env python3

import argparse

from google.protobuf import struct_pb2
from lte.protos.pmn_systems_pb2 import PMNSubscriberData
from lte.protos.models.any_type_pb2 import AnyType
from lte.protos.models.access_and_mobility_subscription_data_pb2 import AccessAndMobilitySubscriptionData
from lte.protos.models.authentication_subscription_pb2 import AuthenticationSubscription
from lte.protos.pmn_systems_pb2_grpc import PMNSubscriberConfigServicerStub
from lte.protos.models.snssai_pb2 import Snssai
from lte.protos.models.nssai_pb2 import Nssai
from lte.protos.models.ambr_rm_pb2 import AmbrRm
from lte.protos.models.sequence_number_pb2 import SequenceNumber
from lte.protos.models.sign_pb2 import Sign
from lte.protos.models.smf_selection_subscription_data_pb2 import SmfSelectionSubscriptionData
from lte.protos.models.sms_management_subscription_data_pb2 import SmsManagementSubscriptionData
from lte.protos.models.ue_policy_set_pb2 import UePolicySet
from lte.protos.models.sms_subscription_data_pb2 import SmsSubscriptionData
from lte.protos.models.am_policy_data_pb2 import AmPolicyData
from lte.protos.models.session_management_subscription_data_pb2 import SessionManagementSubscriptionData
from lte.protos.models.smf_selection_subscription_data_pb2 import SmfSelectionSubscriptionData
from lte.protos.models.sm_policy_snssai_data_pb2 import SmPolicySnssaiData
from lte.protos.models.plmn_id_pb2 import PlmnId
from lte.protos.models.sm_policy_dnn_data_pb2 import SmPolicyDnnData
from lte.protos.models.dnn_info_pb2 import DnnInfo
from lte.protos.models.snssai_info_pb2 import SnssaiInfo
from lte.protos.models.ecgi_pb2 import Ecgi
from lte.protos.models.ncgi_pb2 import Ncgi
from lte.protos.models.tai_pb2 import Tai
from lte.protos.models.presence_info_pb2 import PresenceInfo
from lte.protos.models.dnn_configuration_pb2 import DnnConfiguration
from lte.protos.models.pdu_session_types_pb2 import PduSessionTypes
from lte.protos.models.pdu_session_type_pb2 import InternalPduSessionType
from lte.protos.models.ssc_mode_pb2 import InternalSscMode
from lte.protos.models.ssc_modes_pb2 import SscModes
from lte.protos.models.subscribed_default_qos_pb2 import SubscribedDefaultQos
from lte.protos.models.arp_pb2 import Arp
from lte.protos.models.ambr_pb2 import Ambr

def assemble_am1(args) -> AccessAndMobilitySubscriptionData:

    plmnAmData = struct_pb2.Struct()
    plmnAmData["{}-{}".format(args.mcc, args.mnc)]={}

    return AccessAndMobilitySubscriptionData(
              nssai=Nssai(defaultSingleNssais=[Snssai(sst=args.st, sd=args.sd)],
                          singleNssais=[Snssai(sst=args.st, sd=args.sd)]),
              subscribedUeAmbr=AmbrRm(uplink=args.subs_ambr_ul,
                                      downlink=args.subs_ambr_dl),
              subscribedDnnList=[args.dnn_name],
              plmnAmData=plmnAmData)

def assemble_plmnSmfSelData(args) -> SmfSelectionSubscriptionData:
    dnnInfos = [DnnInfo(dnn="{}.mcc{}.mnc{}.gprs".format(args.dnn_name, args.mcc, args.mnc),
                        iwkEpsInd=True),
                DnnInfo(dnn="ims.mcc{}.mnc{}.gprs".format(args.mcc, args.mnc),
                        iwkEpsInd=True)]

    return SmfSelectionSubscriptionData(
             subscribedSnssaiInfos=({"{}-{}".format(args.st, args.sd):
                                    SnssaiInfo(dnnInfos=dnnInfos)}))


def assemble_smPolicySnssaiData(args) -> SmPolicySnssaiData:
    apn_name1="{}.mnc{}.mcc{}.gprs".format(args.dnn_name, args.mcc, args.mnc)
    sm_policy_dnn_data1 = SmPolicyDnnData(dnn=apn_name1,
                                          allowedServices=["A", "B"],
                                          gbrUl="200kbps", gbrDl="100kbps",
                                          ipv4Index=2, ipv6Index=3,
                                          offline=False, online=True,
                                          subscCats=["Brass"])

    apn_name2="ims.mnc{}.mcc{}.gprs".format(args.mcc, args.mnc)
    sm_policy_dnn_data2 = SmPolicyDnnData(dnn=apn_name2,
                                          allowedServices=["A", "B"],
                                          gbrUl="200kbps", gbrDl="100kbps",
                                          ipv4Index=2, ipv6Index=3,
                                          offline=False, online=True,
                                          subscCats=["Brass"])


    snssai=Snssai(sst=args.st,sd=args.sd)
    return SmPolicySnssaiData(snssai=snssai,
                              smPolicyDnnData=({apn_name1:sm_policy_dnn_data1,
                                                apn_name2:sm_policy_dnn_data2}))

def assemble_plmnSmData(args) -> SessionManagementSubscriptionData:
    snssai=Snssai(sst=args.st,sd=args.sd)
    apn1_dnn_conf=DnnConfiguration(
          pduSessionTypes=PduSessionTypes(
            allowedSessionTypes=[InternalPduSessionType(pduSessTypes="IPV4V6")],
            defaultSessionType=InternalPduSessionType(pduSessTypes="IPV4")),
         internal_5gQosProfile=SubscribedDefaultQos(
            internal_5qi=9,
            arp=Arp(preemptCap="NOT_PREEMPT",preemptVuln="PREEMPTABLE",
                    priorityLevel=7)),
            sessionAmbr=Ambr(downlink="2000 Mbps", uplink="1000 Mbps"),
            sscModes=SscModes(
                     defaultSscMode=InternalSscMode(sscModes="SSC_MODE_1"),
                     allowedSscModes=[InternalSscMode(sscModes="SSC_MODE_1"),
                                      InternalSscMode(sscModes="SSC_MODE_2"),
                                      InternalSscMode(sscModes="SSC_MODE_3")]))

    ims_dnn_conf=DnnConfiguration(
          pduSessionTypes=PduSessionTypes(
            allowedSessionTypes=[InternalPduSessionType(pduSessTypes="IPV4V6")],
            defaultSessionType=InternalPduSessionType(pduSessTypes="IPV4")),
         internal_5gQosProfile=SubscribedDefaultQos(
            internal_5qi=5,
            arp=Arp(preemptCap="NOT_PREEMPT",preemptVuln="PREEMPTABLE",
                    priorityLevel=7)),
            sessionAmbr=Ambr(downlink="2000 Mbps", uplink="1000 Mbps"),
            sscModes=SscModes(
                     defaultSscMode=InternalSscMode(sscModes="SSC_MODE_1"),
                     allowedSscModes=[InternalSscMode(sscModes="SSC_MODE_1"),
                                      InternalSscMode(sscModes="SSC_MODE_2"),
                                      InternalSscMode(sscModes="SSC_MODE_3")]))

    return SessionManagementSubscriptionData(singleNssai=Snssai(sst=args.st,sd=args.sd),
                                             dnnConfigurations=({"apn1": apn1_dnn_conf,
                                                                 "ims": ims_dnn_conf}))

def assemble_am_policy_data(args) -> AmPolicyData:
    ecgiList=[Ecgi(eutraCellId="C2e48fF", plmnId=PlmnId(mcc=args.mcc, mnc=args.mnc)),
              Ecgi(eutraCellId="6a3ec6C", plmnId=PlmnId(mcc=args.mcc, mnc=args.mnc)),
              Ecgi(eutraCellId="65edbeF", plmnId=PlmnId(mcc=args.mcc, mnc=args.mnc)),
              Ecgi(eutraCellId="93B6efC", plmnId=PlmnId(mcc=args.mcc, mnc=args.mnc))]

    ncgiList=[Ncgi(nrCellId="E70D48fE7", plmnId=PlmnId(mcc=args.mcc, mnc=args.mnc)),
              Ncgi(nrCellId="E70D48fE7", plmnId=PlmnId(mcc=args.mcc, mnc=args.mnc)),
              Ncgi(nrCellId="04Aca187a", plmnId=PlmnId(mcc=args.mcc, mnc=args.mnc)),
              Ncgi(nrCellId="8b5e06e21", plmnId=PlmnId(mcc=args.mcc, mnc=args.mnc))]

    trackingAreaList=[Tai(plmnId=PlmnId(mcc=args.mcc, mnc=args.mnc), tac="EAdd"),
                      Tai(plmnId=PlmnId(mcc=args.mcc, mnc=args.mnc), tac="2f491F"),
                      Tai(plmnId=PlmnId(mcc=args.mcc, mnc=args.mnc), tac="19e8b9"),
                      Tai(plmnId=PlmnId(mcc=args.mcc, mnc=args.mnc), tac="e17BA6"),
                      Tai(plmnId=PlmnId(mcc=args.mcc, mnc=args.mnc), tac="FFA2")]

    presenceInfo=PresenceInfo(ecgiList=ecgiList, ncgiList=ncgiList, praId="yyrueiii")

    return AmPolicyData(praInfos=({"ad__3":presenceInfo}),
                        subscCats=["Brass", "sit", "bronze"])

def assemble_ue_policy_data(ue_policy_data):
    plmnId = PlmnId(mcc="001",mnc="01")
    snssai=Snssai(sst=1,sd="000001")
    ue_policy_data.subscCats.MergeFrom(["Categorieslist"])
    ue_policy_data.upsis.MergeFrom(["UpsiInfo1"])
    mapEntry = ue_policy_data.uePolicySections["ade"]
    mapEntry.uePolicySectionInfo = bytes("C0RF",'utf-8')
    mapEntry.upsi = "UPSI-Data"
    mapEntry = ue_policy_data.allowedRouteSelDescs["deserunt38"]
    mapEntry.servingPlmn.CopyFrom(plmnId)
    arrayEntry = mapEntry.snssaiRouteSelDescs.add()
    arrayEntry.snssai.CopyFrom(snssai)
    subArrayEntry = arrayEntry.dnnRouteSelDescs.add()
    subArrayEntry.dnn = "apn1.mnc001.mcc001.gprs"
    arrayEntry = subArrayEntry.sscModes.add()
    arrayEntry.sscModes = "SSC_MODE_1"
    arrayEntry = subArrayEntry.pduSessTypes.add()
    arrayEntry.pduSessTypes="IPV4"
    arrayEntry = subArrayEntry.pduSessTypes.add()
    arrayEntry.pduSessTypes="IPV4V6"

def assemble_sms_data(sms_data):
    sms_data.smsSubscribed=True

def assemble_sms_mng_data(sms_mng_data):
    # sms_mng_data.supportedFeatures =
    sms_mng_data.mtSmsSubscribed=True
    sms_mng_data.mtSmsBarringAll=True
    sms_mng_data.mtSmsBarringRoaming=True
    # sms_mng_data.moSmsSubscribed =
    # sms_mng_data.moSmsBarringAll =
    sms_mng_data.moSmsBarringRoaming=True

def assemble_auth_subs_data(args) -> AuthenticationSubscription:
    return AuthenticationSubscription(KTAB="AUTHSUBS", algorithmId="MILENAGE.1",
                                      authenticationManagementField="8000",
                                      authenticationMethod="5G_AKA",
                                      encOpcKey=args.opc,
                                      encPermanentKey=args.auth_key,
                                      protectionParameterId="none",
                                      sequenceNumber=\
                                       SequenceNumber(difSign=Sign.Sign_POSITIVE,
                                                      indLength=5,
                                                      lastIndexes=({"ausf":22}),
                                                      sqn="000000000ac0"))

def add_subscriber(client, args):

    am1 = assemble_am1(args)

    plmnSmfSelData = assemble_plmnSmfSelData(args)

    smPolicySnssaiData = assemble_smPolicySnssaiData(args)

    auth_subs_data = assemble_auth_subs_data(args)

    plmnSmData = assemble_plmnSmData(args)

    sms_data = SmsSubscriptionData()
    assemble_sms_data(sms_data)

    sms_mng_data = SmsManagementSubscriptionData()
    assemble_sms_mng_data(sms_mng_data)

    am_policy_data = assemble_am_policy_data(args)

    ue_policy_data = UePolicySet()
    assemble_ue_policy_data(ue_policy_data)

    pmn_subs_data=PMNSubscriberData(am1=am1,
                      plmnSmfSelData=\
                      ({"{}-{}".format(args.mcc, args.mnc):plmnSmfSelData}),
                      smPolicySnssaiData=\
                      ({"{}-{}".format(args.st, args.sd):smPolicySnssaiData}),
                      auth_subs_data=auth_subs_data,
                      plmnSmData=\
                      ({"{}-{}".format(args.mcc, args.mnc):plmnSmData}),
                      am_policy_data=am_policy_data,
                      ue_policy_data = ue_policy_data,
                      sms_data=sms_data,
                      sms_mng_data=sms_mng_data,
                      )

    from google.protobuf.json_format import MessageToJson
    print(MessageToJson(pmn_subs_data))
    #client.PMNSubscriberConfig(pmn_subs_data)

def create_parser():
    """
    Creates the argparse parser with all the arguments.
    """
    parser = argparse.ArgumentParser(
        description='Management CLI for PMN Subscriber',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Add subcommands
    subparsers = parser.add_subparsers(title="subcommands", dest="cmd")
    parser_add = subparsers.add_parser("add", help="Add a new subscriber")

    # Add arguments
    for cmd in [parser_add]:
        cmd.add_argument("--mcc", help="Mobile Country Code")
        cmd.add_argument("--mnc", help="Mobile Network Code")
        cmd.add_argument("--imsi", help="Subscriber ID")
        cmd.add_argument("--st", type=int, help="Slice type")
        cmd.add_argument("--sd", help="Slice differentiator")
        cmd.add_argument("--opc", help="encOpcKey")
        cmd.add_argument("--auth_key", help="encPermanentKey")
        cmd.add_argument("--subs_ambr_ul", help="Subscriber uplink Ambr")
        cmd.add_argument("--subs_ambr_dl", help="Subscriber downlink Ambr")
        cmd.add_argument("--dnn_name", help="Name of the dnn")
        cmd.add_argument("--dnn_ambr_ul", help="Dnn's uplink ambr")
        cmd.add_argument("--dnn_ambr_dl", help="Dnn's downlink ambr")
        cmd.add_argument("--qos_profile_5qi", help="Dnn's 5qi profile")


# Add function callbacks
    parser_add.set_defaults(func=add_subscriber)
    return parser

def main():
    parser = create_parser()

    # Parse the args
    args = parser.parse_args()
    if not args.cmd:
        parser.print_usage()
        exit(1)

    if args.cmd == 'add':
        if args.subs_ambr_dl is None or args.subs_ambr_ul is None or args.imsi is None\
                or args.sd is None or args.st is None or args.opc is None\
                or args.auth_key is None:
           parser.print_usage()
           exit(1)

    # Execute the subcommand function
    args.func(None, args)


if __name__ == "__main__":
    main()

#python3.9  pmn_subscriber_cli.py add --mcc 724 --mnc 99 --imsi 724990000000008 --st 1 --sd "fff" --opc E8ED289DEBA952E4283B54E88E6183CA --auth_key 465B5CE8B199B49FAA5F0A2EE238A6BC --subs_ambr_ul "10 Mbps" --subs_ambr_dl "20 Mbps" --dnn_name "apn1" --dnn_ambr_ul "10 Mbps"   --dnn_ambr_dl "20 Mbps" --qos_profile_5qi 5
