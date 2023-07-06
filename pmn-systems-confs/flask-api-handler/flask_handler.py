from flask import Flask, request
import json

app = Flask(__name__)

bevo_msg_dict = {}


def bevo_msg_update(module_json: str, request, supi: str):
    if request.method == "PUT":
        print(" ------- Received JSON Message ------- ")
        bevo_msg_dict.update({module_json: request.json})
        json_object = json.dumps(bevo_msg_dict[module_json], indent=1)
        print(json_object + ",")
        print(f"Added {module_json} for {supi}")
    else:
        print(f"Deleted {module_json} for {supi}")


@app.route("/nudr-sp/v1/subs-<supi>/5gs/imsi-<imsi>/subscription-data/provis"
           "ioned-data/am-data", methods=["PUT", "DELETE"])
def am_data(supi, imsi):
    bevo_msg_update("am1.json", request, supi)
    if request.method == 'PUT':
        print(f"API Invoker ID: {request.headers.get('apiInvokerId')}")
        return request.json
    else:
        return {"Deleted am1.json for": supi}


@app.route("/nudr-sp/v1/subs-<supi>/5gs/imsi-<imsi>/subscription-data/provis"
           "ioned-data/smf-selection-subscription-data",
           methods=["PUT", "DELETE"])
def smf_selection_subscription_data(supi, imsi):
    bevo_msg_update("smfSel.json", request, supi)
    if request.method == 'PUT':
        return request.json
    else:
        return {"Deleted smfSel.json for": supi}


@app.route("/nudr-sp/v1/subs-<supi>/5gs/imsi-<imsi>/policy-data/sm-data",
           methods=["PUT", "DELETE"])
def policy_sm_data(supi, imsi):
    bevo_msg_update("sm-data-policy.json", request, supi)
    if request.method == 'PUT':
        return request.json
    else:
        return {"Deleted sm-data-policy.json for": supi}


@app.route("/nudr-sp/v1/subs-<supi>/5gs/imsi-<imsi>/subscription-data/authen"
           "tication-subscription", methods=["PUT", "DELETE"])
def authentication_subscription(supi, imsi):
    bevo_msg_update("auth-subs-data.json", request, supi)
    if request.method == 'PUT':
        return request.json
    else:
        return {"Deleted auth-subs-data.json for": supi}


@app.route("/nudr-sp/v1/subs-<supi>/5gs/imsi-<imsi>/policy-data/operator-speci"
           "fic-data", methods=["PUT", "DELETE"])
def operator_specific_data(supi, imsi):
    bevo_msg_update("osd.json", request, supi)
    if request.method == 'PUT':
        return request.json
    else:
        return {"Deleted osd.json for": supi}


@app.route("/nudr-sp/v1/subs-<supi>/5gs/imsi-<imsi>/subscription-data/provisio"
           "ned-data/sm-data", methods=["PUT", "DELETE"])
def sm_data(supi, imsi):
    bevo_msg_update("sm-data.json", request, supi)
    if request.method == 'PUT':
        return request.json
    else:
        return {"Deleted sm-data.json for": supi}


@app.route("/nudr-sp/v1/subs-<supi>/5gs/imsi-<imsi>/policy-data/am-data",
           methods=["PUT", "DELETE"])
def policy_am_data(supi, imsi):
    bevo_msg_update("am-policy-data.json", request, supi)
    if request.method == 'PUT':
        return request.json
    else:
        return {"Deleted am-policy-data.json for": supi}


@app.route("/nudr-sp/v1/subs-<supi>/5gs/imsi-<imsi>/policy-data/ue-policy-set",
           methods=["PUT", "DELETE"])
def ue_policy_set(supi, imsi):
    bevo_msg_update("ue-policy-data.json", request, supi)
    if request.method == 'PUT':
        return request.json
    else:
        return {"Deleted ue-policy-data.json for": supi}


@app.route("/nudr-sp/v1/subs-<supi>/5gs/imsi-<imsi>/subscription-data/provisi"
           "oned-data/sms-data", methods=["PUT", "DELETE"])
def sms_data(supi, imsi):
    bevo_msg_update("sms-data.json", request, supi)
    if request.method == 'PUT':
        return request.json
    else:
        return {"Deleted sms-data.json for": supi}


@app.route("/nudr-sp/v1/subs-<supi>/5gs/imsi-<imsi>/subscription-data/provisi"
           "oned-data/sms-mng-data", methods=["PUT", "DELETE"])
def sms_mng_data(supi, imsi):
    bevo_msg_update("sms-mng-data.json", request, supi)
    if request.method == 'PUT':
        return request.json
    else:
        return {"Deleted sms-mng-data.json for": supi}


if __name__ == '__main__':
    app.run(debug=True, port=5000)
