from flask import Flask, request
import json

app = Flask(__name__)


@app.route("/nudr-sp/v1/subs-<supi>/5gs/imsi-<imsi>/subscription-data/provis"
           "ioned-data/am-data", methods=["PUT", "DELETE"])
def am_data(supi, imsi):
    if request.method == 'PUT':
        json_object = json.dumps(request.json, indent=4)
        print(json_object)
        return {
            "supi": supi,
            "imsi": imsi,
            "am-data": request.json
        }
    else:
        return {"Deleted am-data for": supi}


@app.route("/nudr-sp/v1/subs-<supi>/5gs/imsi-<imsi>/subscription-data/provis"
           "ioned-data/smf-selection-subscription-data",
           methods=["PUT", "DELETE"])
def smf_selection_subscription_data(supi, imsi):
    if request.method == 'PUT':
        json_object = json.dumps(request.json, indent=4)
        print(json_object)
        return {
            "supi": supi,
            "imsi": imsi,
            "smf-selection-subscription-data": request.json
        }
    else:
        return {"Deleted smf-selection-subscription-data for": supi}


@app.route("/nudr-sp/v1/subs-<supi>/5gs/imsi-<imsi>/policy-data/sm-data",
           methods=["PUT", "DELETE"])
def policy_sm_data(supi, imsi):
    if request.method == 'PUT':
        json_object = json.dumps(request.json, indent=4)
        print(json_object)
        return {
            "supi": supi,
            "imsi": imsi,
            "sm-data-policy": request.json
        }
    else:
        return {"Deleted sm-data-policy for": supi}


@app.route("/nudr-sp/v1/subs-<supi>/5gs/imsi-<imsi>/subscription-data/authen"
           "tication-subscription", methods=["PUT", "DELETE"])
def authentication_subscription(supi, imsi):
    if request.method == 'PUT':
        json_object = json.dumps(request.json, indent=4)
        print(json_object)
        return {
            "supi": supi,
            "imsi": imsi,
            "auth-subs-data": request.json
        }
    else:
        return {"Deleted auth-subs-data for": supi}


@app.route("/nudr-sp/v1/subs-<supi>/5gs/imsi-<imsi>/policy-data/operator-speci"
           "fic-data", methods=["PUT", "DELETE"])
def operator_specific_data(supi, imsi):
    if request.method == 'PUT':
        json_object = json.dumps(request.json, indent=4)
        print(json_object)
        return {
            "supi": supi,
            "imsi": imsi,
            "osd": request.json
        }
    else:
        return {"Deleted osd for": supi}


@app.route("/nudr-sp/v1/subs-<supi>/5gs/imsi-<imsi>/subscription-data/provisio"
           "ned-data/sm-data", methods=["PUT", "DELETE"])
def sm_data(supi, imsi):
    if request.method == 'PUT':
        json_object = json.dumps(request.json, indent=4)
        print(json_object)
        return {
            "supi": supi,
            "imsi": imsi,
            "sm-data": request.json
        }
    else:
        return {"Deleted sm-data for": supi}


@app.route("/nudr-sp/v1/subs-<supi>/5gs/imsi-<imsi>/policy-data/am-data",
           methods=["PUT", "DELETE"])
def policy_am_data(supi, imsi):
    if request.method == 'PUT':
        json_object = json.dumps(request.json, indent=4)
        print(json_object)
        return {
            "supi": supi,
            "imsi": imsi,
            "am-policy-data": request.json
        }
    else:
        return {"Deleted am-policy-data for": supi}


@app.route("/nudr-sp/v1/subs-<supi>/5gs/imsi-<imsi>/policy-data/ue-policy-set",
           methods=["PUT", "DELETE"])
def ue_policy_set(supi, imsi):
    if request.method == 'PUT':
        json_object = json.dumps(request.json, indent=4)
        print(json_object)
        return {
            "supi": supi,
            "imsi": imsi,
            "ue-policy-data": request.json
        }
    else:
        return {"Deleted ue-policy-data for": supi}


@app.route("/nudr-sp/v1/subs-<supi>/5gs/imsi-<imsi>/subscription-data/provisi"
           "oned-data/sms-data", methods=["PUT", "DELETE"])
def sms_data(supi, imsi):
    if request.method == 'PUT':
        json_object = json.dumps(request.json, indent=4)
        print(json_object)
        return {
            "supi": supi,
            "imsi": imsi,
            "sms-data": request.json
        }
    else:
        return {"Deleted sms-data for": supi}


@app.route("/nudr-sp/v1/subs-<supi>/5gs/imsi-<imsi>/subscription-data/provisi"
           "oned-data/sms-mng-data", methods=["PUT", "DELETE"])
def sms_mng_data(supi, imsi):
    if request.method == 'PUT':
        json_object = json.dumps(request.json, indent=4)
        print(json_object)
        return {
            "supi": supi,
            "imsi": imsi,
            "sms-mng-data": request.json
        }
    else:
        return {"Deleted sms-mng-data for": supi}


if __name__ == '__main__':
    app.run(debug=True, port=5000)
