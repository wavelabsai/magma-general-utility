from flask import Flask, request

app = Flask(__name__)


@app.route("/nudr-sp/v1/subs-<supi>/5gs/imsi-<imsi>/subscription-data/provisioned-data/am-data", methods=["PUT"])
def am_data(supi, imsi):
    return {
        "supi": supi,
        "imsi": imsi,
        "am-data": request.json
    }


@app.route("/nudr-sp/v1/subs-<supi>/5gs/imsi-<imsi>/subscription-data/provisioned-data/smf-selection-subscription-data",
           methods=["PUT"])
def smf_selection_subscription_data(supi, imsi):
    return {
        "supi": supi,
        "imsi": imsi,
        "smf-selection-subscription-data": request.json
    }


@app.route("/nudr-sp/v1/subs-<supi>/5gs/imsi-<imsi>/policy-data/sm-data", methods=["PUT"])
def policy_sm_data(supi, imsi):
    return {
        "supi": supi,
        "imsi": imsi,
        "sm-data-policy": request.json
    }


@app.route("/nudr-sp/v1/subs-<supi>/5gs/imsi-<imsi>/subscription-data/authentication-subscription", methods=["PUT"])
def authentication_subscription(supi, imsi):
    return {
        "supi": supi,
        "imsi": imsi,
        "auth-subs-data": request.json
    }


@app.route("/nudr-sp/v1/subs-<supi>/5gs/imsi-<imsi>/policy-data/operator-specific-data", methods=["PUT"])
def operator_specific_data(supi, imsi):
    return {
        "supi": supi,
        "imsi": imsi,
        "osd": request.json
    }


@app.route("/nudr-sp/v1/subs-<supi>/5gs/imsi-<imsi>/subscription-data/provisioned-data/sm-data", methods=["PUT"])
def sm_data(supi, imsi):
    pass


@app.route("/nudr-sp/v1/subs-<supi>/5gs/imsi-<imsi>/policy-data/am-data", methods=["PUT"])
def policy_am_data(supi, imsi):
    return {
        "supi": supi,
        "imsi": imsi,
        "am-policy-data": request.json
    }


@app.route("/nudr-sp/v1/subs-<supi>/5gs/imsi-<imsi>/policy-data/ue-policy-set", methods=["PUT"])
def ue_policy_set(supi, imsi):
    return {
        "supi": supi,
        "imsi": imsi,
        "ue-policy-data": request.json
    }


@app.route("/nudr-sp/v1/subs-<supi>/5gs/imsi-<imsi>/subscription-data/provisioned-data/sms-data", methods=["PUT"])
def sms_data(supi, imsi):
    return {
        "supi": supi,
        "imsi": imsi,
        "sms-data": request.json
    }


@app.route("/nudr-sp/v1/subs-<supi>/5gs/imsi-<imsi>/subscription-data/provisioned-data/sms-mng-data", methods=["PUT"])
def sms_mng_data(supi, imsi):
    return {
        "supi": supi,
        "imsi": imsi,
        "sms-mng-data": request.json
    }


if __name__ == '__main__':
    app.run(debug=True, port=5000)
