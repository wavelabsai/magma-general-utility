#!/usr/bin/env python3
# flake8: noqa
import argparse

from google.protobuf import struct_pb2
from google.protobuf.json_format import MessageToJson
from lte.protos.models.access_and_mobility_subscription_data_pb2 import (
    AccessAndMobilitySubscriptionData,
)
from lte.protos.models.am_policy_data_pb2 import AmPolicyData
from lte.protos.models.ambr_pb2 import Ambr
from lte.protos.models.ambr_rm_pb2 import AmbrRm
from lte.protos.models.arp_pb2 import Arp
from lte.protos.models.authentication_subscription_pb2 import (
    AuthenticationSubscription,
)
from lte.protos.models.dnn_configuration_pb2 import DnnConfiguration
from lte.protos.models.dnn_info_pb2 import DnnInfo
from lte.protos.models.dnn_route_selection_descriptor_pb2 import (
    DnnRouteSelectionDescriptor,
)
from lte.protos.models.ecgi_pb2 import Ecgi
from lte.protos.models.ncgi_pb2 import Ncgi
from lte.protos.models.nssai_pb2 import Nssai
from lte.protos.models.operator_specific_data_pb2 import OperatorSpecificData
from lte.protos.models.pdu_session_types_pb2 import PduSessionTypes
from lte.protos.models.plmn_id_pb2 import PlmnId
from lte.protos.models.plmn_route_selection_descriptor_pb2 import (
    PlmnRouteSelectionDescriptor,
)
from lte.protos.models.presence_info_pb2 import PresenceInfo
from lte.protos.models.sequence_number_pb2 import SequenceNumber
from lte.protos.models.service_subscription_pb2 import ServiceSubscriptionValue
from lte.protos.models.session_management_subscription_data_pb2 import (
    SessionManagementSubscriptionData,
)
from lte.protos.models.sm_policy_dnn_data_pb2 import SmPolicyDnnData
from lte.protos.models.sm_policy_snssai_data_pb2 import SmPolicySnssaiData
from lte.protos.models.smf_selection_subscription_data_pb2 import (
    SmfSelectionSubscriptionData,
)
from lte.protos.models.sms_management_subscription_data_pb2 import (
    SmsManagementSubscriptionData,
)
from lte.protos.models.sms_subscription_data_pb2 import SmsSubscriptionData
from lte.protos.models.snssai_info_pb2 import SnssaiInfo
from lte.protos.models.snssai_pb2 import Snssai
from lte.protos.models.snssai_route_selection_descriptor_pb2 import (
    SnssaiRouteSelectionDescriptor,
)
from lte.protos.models.ssc_modes_pb2 import SscModes
from lte.protos.models.subscribed_default_qos_pb2 import SubscribedDefaultQos
from lte.protos.models.subscriber_info_pb2 import QosProfileName
from lte.protos.models.tai_pb2 import Tai
from lte.protos.models.ue_policy_section_pb2 import UePolicySection
from lte.protos.models.ue_policy_set_pb2 import UePolicySet
from lte.protos.models.volume_accounting_pb2 import VolumeAccountingValue
from lte.protos.pmn_systems_pb2 import (
    PMNSubscriberData,
    SmData,
    SmDataPolicy,
    SmfSelection,
    SmsData,
    CurlEndpoint,
    APIInvokerID,
    Void,
)
from lte.protos.pmn_systems_pb2_grpc import PMNSubscriberConfigServicerStub
from lte.protos.subscriberdb_pb2 import SubscriberData, SubscriberID
from magma.common.rpc_utils import grpc_wrapper

def assemble_am1(args) -> AccessAndMobilitySubscriptionData:

    plmnAmData = struct_pb2.Struct()
    plmnAmData["{}-{}".format(args.mcc, args.mnc)] = {}

    return AccessAndMobilitySubscriptionData(
        nssai=Nssai(
            defaultSingleNssais=[Snssai(sst=args.st, sd=args.sd)],
        ),
        gpsis=["msisdn-{}".format(args.imsi[4:])],
        subscribedUeAmbr=AmbrRm(
            uplink=args.subs_ambr_ul,
            downlink=args.subs_ambr_dl,
        ),
        subscribedDnnList=[args.dnn_name],
        plmnAmData=plmnAmData,
    )


def assemble_smfSel(args) -> SmfSelection:
    mnc=args.mnc.rjust(3, "0")
    dnnInfos = [
        DnnInfo(
            dnn="{}.mnc{}.mcc{}.gprs".format(args.dnn_name, mnc, args.mcc),
            iwkEpsInd=True,
        ),
    ]

    smfSelectionSubscriptionData =\
        SmfSelectionSubscriptionData(
            subscribedSnssaiInfos=({
                "{}-{}".format(args.st, args.sd):
                SnssaiInfo(dnnInfos=dnnInfos),
            }),
        )

    return SmfSelection(
        plmnSmfSelData=({"{}-{}".format(args.mcc, args.mnc): smfSelectionSubscriptionData}),
    )


def assemble_smDataPolicy(args) -> SmDataPolicy:
    mnc=args.mnc.rjust(3, "0")
    apn_name1 = "{}.mnc{}.mcc{}.gprs".format(args.dnn_name, mnc, args.mcc)
    sm_policy_dnn_data1 = SmPolicyDnnData(
        dnn=apn_name1,
        allowedServices=["A"],
        gbrUl="200kbps", gbrDl="100kbps",
    )

    smPolicySnssaiData = SmPolicySnssaiData(
        snssai=Snssai(sst=args.st, sd=args.sd),
        smPolicyDnnData=({
            apn_name1: sm_policy_dnn_data1,
        }),
    )

    return SmDataPolicy(
        smPolicySnssaiData=({"{}-{}".format(args.st, args.sd): smPolicySnssaiData}),
    )


def assemble_smData(args) -> SmData:
    apn1_dnn_conf = DnnConfiguration(
        pduSessionTypes=PduSessionTypes(
            allowedSessionTypes=["IPV4V6"],
            defaultSessionType="IPV4",
        ),
        internal_5gQosProfile=SubscribedDefaultQos(
            internal_5qi=9, arp=Arp(
                preemptCap="NOT_PREEMPT", preemptVuln="PREEMPTABLE",
                priorityLevel=7,
            ),
        ),
        sessionAmbr=Ambr(downlink="2 Mbps", uplink="1 Mbps"),
        sscModes=SscModes(
            defaultSscMode="SSC_MODE_1",
            allowedSscModes=["SSC_MODE_1", "SSC_MODE_2", "SSC_MODE_3"],
        ),
    )

    sessionManagementSubscriptionData = SessionManagementSubscriptionData(
        singleNssai=Snssai(sst=args.st, sd=args.sd),
        dnnConfigurations=({"apn1": apn1_dnn_conf}),
    )

    listValue = struct_pb2.ListValue()
    listValue.extend([MessageToJson(sessionManagementSubscriptionData)])
    return SmData(plmnSmData=({"{}-{}".format(args.mcc, args.mnc): listValue}))


def assemble_am_policy_data(args) -> AmPolicyData:
    trackingAreaList = [
        Tai(plmnId=PlmnId(mcc=args.mcc, mnc=args.mnc), tac="0001"),
    ]

    presenceInfo = PresenceInfo(
        trackingAreaList=trackingAreaList
    )

    return AmPolicyData(
        praInfos=({"ad__3": presenceInfo}),
    )


def assemble_ue_policy_data(args) -> UePolicySet:
    mnc=args.mnc.rjust(3, "0")
    plmnRouteSelectionDescriptor = PlmnRouteSelectionDescriptor(
        servingPlmn=PlmnId(mcc=args.mcc, mnc=args.mnc),
        snssaiRouteSelDescs=[
            SnssaiRouteSelectionDescriptor(
                snssai=Snssai(sst=args.st, sd=args.sd),
                dnnRouteSelDescs=[
                    DnnRouteSelectionDescriptor(
                        dnn="{}.mnc{}.mcc{}.gprs".format(
                            args.dnn_name, mnc, args.mcc,
                        ),
                        sscModes=["SSC_MODE_1"],
                        pduSessTypes=["IPV4", "IPV4V6"],
                    ),
                ],
            ),
        ],
    )

    return UePolicySet(
        subscCats=["Categorieslist"],
        uePolicySections=(
            {
                "ade": UePolicySection(
                    uePolicySectionInfo=bytes("C0RF", 'utf-8'),
                    upsi="UPSI-Data",
                ),
            }
        ),
        allowedRouteSelDescs=(
            {"deserunt38": plmnRouteSelectionDescriptor}
        ),
    )


def assemble_sms_data(args) -> SmsData:
    return SmsData(
        plmnSmsData=(
            {
                "{mcc}-{mnc}".format(mcc=args.mcc, mnc=args.mnc): SmsSubscriptionData(
                    smsSubscribed=True,
                ),
            }
        ),
    )


def assemble_sms_mng_data(args) -> SmsManagementSubscriptionData:
    plmnSmsMgmtSubsData = struct_pb2.Struct()
    plmnSmsMgmtSubsData["{mcc}-{mnc}".format(mcc=args.mcc, mnc=args.mnc)] = {"dummy": "mav1"}
    return SmsManagementSubscriptionData(
        mtSmsSubscribed=True,
        mtSmsBarringAll=True,
        mtSmsBarringRoaming=True,
        moSmsBarringRoaming=True,
        plmnSmsMgmtSubsData=plmnSmsMgmtSubsData,
    )


def assemble_auth_subs_data(args) -> AuthenticationSubscription:

    return AuthenticationSubscription(
        KTAB="AUTHSUBS", algorithmId="MILENAGE.1",
        authenticationManagementField="8000", authenticationMethod="5G_AKA",
        encOpcKey=bytes.fromhex(args.opc),
        encPermanentKey=bytes.fromhex(args.auth_key),
        protectionParameterId="none", sequenceNumber=SequenceNumber(
            difSign="POSITIVE",
            indLength=5,
            sqnScheme="NON_TIME_BASED",
        ),
    )


def assemble_osd() -> OperatorSpecificData:
    osd = OperatorSpecificData()
    osd.SubscriberId.dataType = "string"
    osd.SubscriberId.value = "A"
    osd.SubscriberInfo.dataType = "object"
    osd.SubscriberInfo.value.PricingPlanType = ""
    osd.SubscriberInfo.value.PlanName = "199"
    osd.SubscriberInfo.value.HomeLocation = ""
    osd.SubscriberInfo.value.UserNotification = ""
    osd.SubscriberInfo.value.SubscriberEmailId = ""
    osd.SubscriberInfo.value.SubscriberValidity = ""
    osd.SubscriberInfo.value.SubscriberCategory = ""
    osd.SubscriberInfo.value.internal_PAYGConsent = "A"
    subscribedServices = ["", "", "", ""]
    osd.SubscriberInfo.value.TopupServicesSubscribed.MergeFrom(subscribedServices)

    qosProfileItem = QosProfileName()
    qosProfileItem.QosProfileName = "a"
    qosProfileItem.pcrfARPPrioLevel = "a"
    qosProfileItem.pcrfPreEmptionCap = "a"
    qosProfileItem.pcrfPreEmptionVuln = "a"
    qosProfileItem.pcrfQoSClassName = "a"
    qosProfileItem.pcrfMaxReqBrUL = "a"
    qosProfileItem.pcrfMaxReqBrDL = "a"
    qosProfileItem.pcrfGuarBrUL = "a"
    qosProfileItem.pcrfGuarBrDL = "a"
    qosProfileItem.pcrfAPNAggMaxBrUL = "a"
    qosProfileItem.pcrfAPNAggMaxBrDL = "a"
    osd.SubscriberInfo.value.QosProfileName.MergeFrom([qosProfileItem])

    ssValueItem1 = ServiceSubscriptionValue()
    ssValueItem1.ServiceName = "BasePlan"
    ssValueItem1.ServiceId = "12345"
    ssValueItem1.BillingStartDate = "a"
    ssValueItem1.BillingEndDate = "a"
    ssValueItem1.QuotaStartDate = "a"
    ssValueItem1.QuotaEndDate = "a"
    ssValueItem1.MonitoringKey = "a"
    ssValueItem1.RatingGroup = "a"
    ssValueItem1.TotalThreshold = "a"
    ssValueItem1.RecurringQuotaReset = "a"
    ssValueItem1.CurrentRolloverCount = "a"
    ssValueItem2 = ServiceSubscriptionValue()
    ssValueItem2.ServiceName = "Top-Up"
    ssValueItem2.ServiceId = "12346"
    ssValueItem2.BillingStartDate = "b"
    ssValueItem2.BillingEndDate = "b"
    ssValueItem2.QuotaStartDate = "b"
    ssValueItem2.QuotaEndDate = "b"
    ssValueItem2.MonitoringKey = "b"
    ssValueItem2.RatingGroup = "b"
    ssValueItem2.TotalThreshold = "b"
    ssValueItem2.RecurringQuotaReset = "b"
    ssValueItem2.CurrentRolloverCount = "b"
    osd.ServiceSubscription.dataType = "object"
    osd.ServiceSubscription.value.MergeFrom([ssValueItem1, ssValueItem2])

    vaValueItem1 = VolumeAccountingValue()
    vaValueItem1.ServiceName = "a"
    vaValueItem1.ServiceId = "a"
    vaValueItem1.TotalUsedQuota = "a"
    vaValueItem1.UlUsedQuota = "a"
    vaValueItem1.DlUsedQuota = "a"
    vaValueItem1.MonitoringKey = "a"
    vaValueItem1.GracePeriod = "a"

    vaValueItem2 = VolumeAccountingValue()
    vaValueItem2.ServiceName = "b"
    vaValueItem2.ServiceId = "b"
    vaValueItem2.TotalUsedQuota = "b"
    vaValueItem2.UlUsedQuota = "b"
    vaValueItem2.DlUsedQuota = "b"
    vaValueItem2.MonitoringKey = "b"
    vaValueItem2.GracePeriod = "b"

    osd.VolumeAccounting.dataType = "object"
    osd.VolumeAccounting.value.MergeFrom([vaValueItem1, vaValueItem2])
    return osd


@grpc_wrapper
def add_subscriber(client, args):
    am1 = assemble_am1(args)

    smfSel = assemble_smfSel(args)

    smDataPolicy = assemble_smDataPolicy(args)

    auth_subs_data = assemble_auth_subs_data(args)

    osd = assemble_osd()

    smData = assemble_smData(args)

    sms_data = assemble_sms_data(args)

    sms_mng_data = assemble_sms_mng_data(args)

    am_policy_data = assemble_am_policy_data(args)

    ue_policy_data = assemble_ue_policy_data(args)

    subscriber_data = SubscriberData()
    subscriber_data.sid.id = args.imsi[4:]

    pmn_subs_data = \
        PMNSubscriberData(
            subscriber_data=subscriber_data,
            am1=am1, smfSel=smfSel, smDataPolicy=smDataPolicy,
            auth_subs_data=auth_subs_data, osd=osd,
            smData=smData, am_policy_data=am_policy_data,
            ue_policy_data=ue_policy_data,
        )

    client.PMNAddSubscriberConfig(pmn_subs_data)


@grpc_wrapper
def delete_subscriber(client, args):
    subscriber_data = SubscriberData()
    subscriber_data.sid.id = args.imsi[4:]
    pmn_subs_data = PMNSubscriberData(subscriber_data=subscriber_data)
    client.PMNDelSubscriberConfig(pmn_subs_data)


@grpc_wrapper
def get_pmn_subscriber(client, args):
    subscriber_data = SubscriberData()
    subscriber_data.sid.id = args.imsi[4:]
    pmn_subs_data = PMNSubscriberData(subscriber_data=subscriber_data)
    obj = client.GetPMNSubscriber(pmn_subs_data)
    print(f'Get subscriber "{args.imsi}" response:')
    print(obj.pmn_data_json_str)


@grpc_wrapper
def set_endpoint(client, args):
    client.SetCurlEndpoint(CurlEndpoint(
        endpoint_ip=args.ip, endpoint_port=args.port))


@grpc_wrapper
def get_endpoint(client, args):
    obj = client.GetCurlEndpoint(Void())
    print(f"Configured Endpoint: {obj.endpoint_ip}:{obj.endpoint_port}")


@grpc_wrapper
def set_api_key(client, args):
    client.SetAPIInvokerID(APIInvokerID(
        api_invoker_id=args.api_key))


@grpc_wrapper
def get_api_key(client, args):
    obj = client.GetAPIInvokerID(Void())
    print(f"Configured API Invoker ID: {obj.api_invoker_id}")


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
    parser_del = subparsers.add_parser("delete", help="Delete a subscriber")
    parser_get = subparsers.add_parser("get", help="Get data for a subscriber")
    parser_set_endpoint = subparsers.add_parser("set_endpoint", help="Configure Curl Endpoint")
    parser_get_endpoint = subparsers.add_parser("get_endpoint", help="Get Curl Endpoint")
    parser_set_api_key = subparsers.add_parser("set_api_key", help="Configure API Invoker ID")
    parser_get_api_key = subparsers.add_parser("get_api_key", help="Get API Invoker ID")

    for cmd in [parser_add, parser_del, parser_get]:
        cmd.add_argument("--imsi",
                         help="Subscriber ID, for example: IMSI001010000000001",
                         required=True)

    # Add arguments
    parser_add.add_argument("--mcc", help="Mobile Country Code", required=True)
    parser_add.add_argument("--mnc", help="Mobile Network Code", required=True)
    parser_add.add_argument("--st", type=int, help="Slice type", required=True)
    parser_add.add_argument("--sd", help="Slice differentiator", required=True)
    parser_add.add_argument("--opc", help="encOpcKey", required=True)
    parser_add.add_argument("--auth_key", help="encPermanentKey", required=True)
    parser_add.add_argument("--subs_ambr_ul", help="Subscriber uplink Ambr", required=True)
    parser_add.add_argument("--subs_ambr_dl", help="Subscriber downlink Ambr", required=True)
    parser_add.add_argument("--dnn_name", help="Name of the dnn", required=True)
    parser_add.add_argument("--dnn_ambr_ul", help="Dnn's uplink ambr", required=True)
    parser_add.add_argument("--dnn_ambr_dl", help="Dnn's downlink ambr", required=True)
    parser_add.add_argument("--qos_profile_5qi", type=int, help="Dnn's 5qi profile", required=True)

    parser_set_endpoint.add_argument("--ip", help="curl endpoint IP address", required=True)
    parser_set_endpoint.add_argument("--port", help="curl endpoint port", required=True)

    parser_set_api_key.add_argument("--api_key", help="API Invoker ID", required=True)

# Add function callbacks
    parser_add.set_defaults(func=add_subscriber)
    parser_del.set_defaults(func=delete_subscriber)
    parser_get.set_defaults(func=get_pmn_subscriber)
    parser_set_endpoint.set_defaults(func=set_endpoint)
    parser_get_endpoint.set_defaults(func=get_endpoint)
    parser_set_api_key.set_defaults(func=set_api_key)
    parser_get_api_key.set_defaults(func=get_api_key)
    return parser


def main():
    parser = create_parser()

    # Parse the args
    args = parser.parse_args()
    if not args.cmd:
        parser.print_usage()
        exit(1)

    # Execute the subcommand function
    args.func(args, PMNSubscriberConfigServicerStub, 'subscriberdb')


if __name__ == "__main__":
    main()
