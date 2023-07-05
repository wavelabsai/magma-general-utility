from flask import Flask, request
import json

app = Flask(__name__)

bevo_msg_dict={}

def bevo_msg_update(module_json:str, request:str):
    print(" ------- Received JSON Message ------- ")
    bevo_msg_dict.update({module_json: request})
    json_object = json.dumps(bevo_msg_dict, indent=1)
    print(json_object + ",")

@app.route("/nudr-sp/v1/subs-<supi>/5gs/imsi-<imsi>/subscription-data/provisioned-data/am-data", methods=["PUT"])
def am_data(supi, imsi):
    bevo_msg_update("am1.json", request.json)
    return {
        "supi": supi,
        "imsi": imsi,
        "am-data": request.json
    }


@app.route("/nudr-sp/v1/subs-<supi>/5gs/imsi-<imsi>/subscription-data/provisioned-data/smf-selection-subscription-data",
           methods=["PUT"])
def smf_selection_subscription_data(supi, imsi):
    bevo_msg_update("smfSel.json", request.json)
    return {
        "supi": supi,
        "imsi": imsi,
        "smf-selection-subscription-data": request.json
    }


@app.route("/nudr-sp/v1/subs-<supi>/5gs/imsi-<imsi>/policy-data/sm-data", methods=["PUT"])
def policy_sm_data(supi, imsi):
    bevo_msg_update("sm-data-policy.json", request.json)
    return {
        "supi": supi,
        "imsi": imsi,
        "sm-data-policy": request.json
    }


@app.route("/nudr-sp/v1/subs-<supi>/5gs/imsi-<imsi>/subscription-data/authentication-subscription", methods=["PUT"])
def authentication_subscription(supi, imsi):
    bevo_msg_update("auth-subs-data.json", request.json)
    return {
        "supi": supi,
        "imsi": imsi,
        "auth-subs-data": request.json
    }


@app.route("/nudr-sp/v1/subs-<supi>/5gs/imsi-<imsi>/policy-data/operator-specific-data", methods=["PUT"])
def operator_specific_data(supi, imsi):
    bevo_msg_update("osd.json", request.json)
    return {
        "supi": supi,
        "imsi": imsi,
        "osd": request.json
    }


@app.route("/nudr-sp/v1/subs-<supi>/5gs/imsi-<imsi>/subscription-data/provisioned-data/sm-data", methods=["PUT"])
def sm_data(supi, imsi):
    bevo_msg_update("sm-data.json", request.json)
    return {
        "supi": supi,
        "imsi": imsi,
        "sm-data": request.json
    }


@app.route("/nudr-sp/v1/subs-<supi>/5gs/imsi-<imsi>/policy-data/am-data", methods=["PUT"])
def policy_am_data(supi, imsi):
    bevo_msg_update("am-policy-data.json", request.json)
    return {
        "supi": supi,
        "imsi": imsi,
        "am-policy-data": request.json
    }


@app.route("/nudr-sp/v1/subs-<supi>/5gs/imsi-<imsi>/policy-data/ue-policy-set", methods=["PUT"])
def ue_policy_set(supi, imsi):
    bevo_msg_update("ue-policy-data.json", request.json)
    return {
        "supi": supi,
        "imsi": imsi,
        "ue-policy-data": request.json
    }


@app.route("/nudr-sp/v1/subs-<supi>/5gs/imsi-<imsi>/subscription-data/provisioned-data/sms-data", methods=["PUT"])
def sms_data(supi, imsi):
    bevo_msg_update("sms-data.json", request.json)
    return {
        "supi": supi,
        "imsi": imsi,
        "sms-data": request.json
    }


@app.route("/nudr-sp/v1/subs-<supi>/5gs/imsi-<imsi>/subscription-data/provisioned-data/sms-mng-data", methods=["PUT"])
def sms_mng_data(supi, imsi):
    bevo_msg_update("sms-mng-data.json", request.json)
    return {
        "supi": supi,
        "imsi": imsi,
        "sms-mng-data": request.json
    }


if __name__ == '__main__':
    app.run(debug=True, port=5000)
