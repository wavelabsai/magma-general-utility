#!/usr/bin/env python3
import sys
import time

from flask import Flask, request
from flask_restful import Api, Resource

admin_auth = {
    "username": "admin",
    "password": "password",
}

next_uids = {
    "doctors": 3,
    "patients": 3,
    "appointments": 5,
}

doctors = [
    {
        "full name": "Dr John Doe",
        "username": "paediatricianjohndoe",
        "speciality": "paediatrician",
        "unique_id": 1,
        "password": "DrJohnDoe",
    },
    {
        "full name": "Dr Jane Smith",
        "speciality": "dentist",
        "username": "dentistjanesmith",
        "unique_id": 2,
        "password": "DrJaneSmith",
    },
]
doctor_keys = [
    "full name",
    "username",
    "speciality",
    "unique_id",
    "password",
]

patients = [
    {
        "full name": "Jane Doe",
        "unique_id": 1,
        "username": "clientjanedoe",
        "password": "JaneDoe",
        "phone": "1234",
        "email": "janedoe@service.com",
    },
    {
        "full name": "John Smith",
        "username": "clientjohnsmith",
        "unique_id": 2,
        "password": "JohnSmith",
        "phone": "4524",
        "email": "johnsmit@example.com",
    },
]
patient_keys = [
    "full name",
    "unique_id",
    "username",
    "password",
    "phone",
    "email",
]

appointments = [
    {
        "doctor_uid": 1,
        "patient_uid": 1,
        "start_time": "2023-01-01T10:00",
        "unique_id": 1,
    },
    {
        "doctor_uid": 1,
        "patient_uid": 1,
        "start_time": "2023-01-10T10:00",
        "unique_id": 2,
    },
    {
        "doctor_uid": 2,
        "patient_uid": 1,
        "start_time": "2023-01-10T10:00",
        "unique_id": 3,
    },
    {
        "doctor_uid": 2,
        "patient_uid": 2,
        "start_time": "2023-01-10T10:05",
        "unique_id": 4,
    },
]
appointment_keys = [
    "doctor_uid",
    "patient_uid",
    "start_time",
    "unique_id",
]


class Doctors(Resource):
    def get(self, uid=0):
        sys.stderr.write(f"UID: {uid}\n")
        if uid == 0:
            data = [{y: x[y]} for y in ["full name", "speciality", "unique_id"] for x in doctors]
            sys.stderr.write(f"data: {data}\n")
            return data, 200

        doctor = list(filter(lambda x: x["unique_id"] == uid, doctors))

        if doctor:
            return doctor, 200

        return f"Doctor with uid {uid} not found", 400

    def post(self, uid=0):
        auth = request.authorization
        if not auth == admin_auth:
            return "You're not authorised to access this page. Please login as administrator", 404

        try:
            data = request.get_json()
        except Exception:
            return "Could not parse the request data as JSON", 400

        doctor = list(filter(lambda x: x["unique_id"] == uid, doctors))

        if doctor:
            doctor = doctor[0]
            doctor_index = doctors.index(doctor)
            update_dictionary = {x: data[x] for x in data.keys() if x in doctor_keys}
            doctors[doctor_index].update(update_dictionary)
            return f"Doctor {doctor['full name']}'s data has been updated with provided data", 200

        # Doctor not found, adding
        doctor = {}
        try:
            doctor["full name"] = data["full name"]
            doctor["username"] = data["username"]
            doctor["speciality"] = data["speciality"]
            doctor["password"] = data["password"]
        except Exception as e:
            return f"Couldn't create doctor with provided data. Error was: {type(e)}:{e}", 400
        else:
            doctor["unique_id"] = next_uids["doctors"]
            next_uids["doctors"] += 1
            doctors.append(doctor)
            return f"Created Doctor {doctor['full name']}'s profile", 200


class Patients(Resource):
    def get(self, uid=0):
        # This has to either be a doctor or administrator
        auth = request.authorization
        if not auth:
            auth = {"username": "", "password": ""}
        authorised = False
        if auth == admin_auth:
            authorised = True

        if not authorised:
            doctor = list(filter(lambda x: x["username"] == auth["username"], doctors))
            if doctor and doctor[0]["password"] == auth["password"]:
                authorised = True

        if uid == 0:
            if not authorised:
                return "You're not authorised to access this page. Please login as administrator or a doctor", 404
            data = [{y: x[y] for y in ["full name", "unique_id", "phone", "email"]} for x in patients]
            return data, 200

        patient = list(filter(lambda x: x["unique_id"] == uid, patients))

        if not patient:
            return "You're not authorised to access this page. Please login as administrator or a doctor", 404
        if not authorised:
            if not (patient[0]["username"] == auth["username"] and patient[0]["password"] == auth["password"]):
                return "You're not authorised to access this page. Please login as administrator or a doctor", 404
            authorised = True
        data = {}
        data["full name"] = patient[0]["full name"]
        data["username"] = patient[0]["username"]
        data["unique_id"] = patient[0]["unique_id"]
        data["phone"] = patient[0]["phone"]
        data["email"] = patient[0]["email"]
        return data, 200

    def post(self, uid=0):
        auth = request.authorization
        if not auth == admin_auth:
            return "You're not authorised to access this page. Please login as administrator", 404

        try:
            data = request.get_json()
        except Exception:
            return "Could not parse the request data as JSON", 400

        patient = list(filter(lambda x: x["unique_id"] == uid, patients))

        if patient:
            patient = patient[0]
            patient_index = patients.index(patient)
            update_dictionary = {x: data[x] for x in data.keys() if x in patient_keys}
            if update_dictionary.get("unique_id"):
                del update_dictionary["unique_id"]
            patients[patient_index].update(update_dictionary)
            return f"Patient {patient['full name']}'s data has been updated with provided data", 200

        # Patient not found, adding
        patient = {}
        try:
            patient["full name"] = data["full name"]
            patient["username"] = data["username"]
            patient["password"] = data["password"]
            patient["phone"] = data["phone"]
            patient["email"] = data["email"]
        except Exception as e:
            return f"Couldn't create patient with provided data. Error was: {type(e)}:{e}", 400
        else:
            patient["unique_id"] = next_uids["patients"]
            next_uids["patients"] += 1
            patients.append(patient)
            return f"Created Patient {patient['full name']}'s profile", 200


class Appointments(Resource):
    def get(self, uid=0):
        # The administrator can see all appointments
        auth = request.authorization
        if not auth:
            return "You're not authorised to access this page. Please login", 404
        if auth == admin_auth:
            return appointments, 200

        doctor = list(
            filter(lambda x: x["username"] == auth["username"] and x["password"] == auth["password"], doctors)
        )
        if doctor:
            doctor = doctor[0]
            drs_appointments = [x for x in appointments if x["doctor_uid"] == doctor["unique_id"]]
            return f"Dr {doctor['full name']}'s appointments: {drs_appointments}", 200

        patient = list(
            filter(lambda x: x["username"] == auth["username"] and x["password"] == auth["password"], patients)
        )
        if patient:
            patient = patient[0]
            pts_appointments = [x for x in appointments if x["patient_uid"] == patient["unique_id"]]
            return f"{patient['full name']}'s appointments: {pts_appointments}", 200

        return "You're not authorised to access this page. Please login", 404

    def post(self, uid=0):
        auth = request.authorization
        if not auth:
            return "You're not authorised to access this page. Please login", 404
        if auth == admin_auth:
            return "Administrator account not enabled to create appointments", 405

        try:
            data = request.get_json()
            appointment_data = {
                "doctor_uid": data["doctor_uid"],
                "patient_uid": data["doctor_uid"],
                "start_time": data["start_time"],
            }
            time.strptime(data["start_time"], "%Y-%m-%dT%H:%M")
        except Exception:
            return "Malformed appointment data sent", 400

        doctor = list(
            filter(lambda x: x["username"] == auth["username"] and x["password"] == auth["password"], doctors)
        )
        if doctor:
            doctor = doctor[0]
            if not doctor["unique_id"] == appointment_data["doctor_uid"]:
                return "You're not authorised to create this resource.", 404
            appointment_data["unique_id"] = next_uids["appointments"]
            next_uids["appointments"] += 1
            appointments.append(appointment_data)
            return "Created appointment", 200

        patient = list(
            filter(lambda x: x["username"] == auth["username"] and x["password"] == auth["password"], patients)
        )
        if patient:
            patient = patient[0]
            if not patient["unique_id"] == appointment_data["patient_uid"]:
                return "You're not authorised to create this resource.", 404
            appointment_data["unique_id"] = next_uids["appointments"]
            next_uids["appointments"] += 1
            appointments.append(appointment_data)
            return "Created appointment", 200
        return "You're not authorised to perform this action.", 404

    def delete(self, uid=0):
        auth = request.authorization
        if not auth:
            return "You're not authorised to access this page. Please login", 404
        if auth == admin_auth:
            return "Administrator account not enabled to delete appointments", 405

        doctor = list(
            filter(lambda x: x["username"] == auth["username"] and x["password"] == auth["password"], doctors)
        )
        if doctor:
            doctor = doctor[0]
            appointment = list(
                filter(lambda x: x["unique_id"] == uid and x["doctor_uid"] == doctor["unique_id"], appointments)
            )

            if not appointment:
                return "You're not authorised to perform this action.", 404
            appointment = appointment[0]
            appointment_idx = appointments.index(appointment)
            del appointments[appointment_idx]
            return "Deleted appointment", 200

        patient = list(
            filter(lambda x: x["username"] == auth["username"] and x["password"] == auth["password"], patients)
        )

        if patient:
            patient = patient[0]
            appointment = list(
                filter(lambda x: x["unique_id"] == uid and x["patient_uid"] == patient["unique_id"], appointments)
            )

            if not appointment:
                return "You're not authorised to perform this action.", 404
            appointment = appointment[0]
            appointment_idx = appointments.index(appointment)
            del appointments[appointment_idx]
            return "Deleted appointment", 200

        return "You're not authorised to perform this action.", 404


app = Flask(__name__)
api = Api(app)

api.add_resource(Doctors, "/doctors/", "/doctors/<int:uid>")
api.add_resource(Patients, "/patients/", "/patients/<int:uid>")
api.add_resource(Appointments, "/appointments/", "/appointments/<int:uid>")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
