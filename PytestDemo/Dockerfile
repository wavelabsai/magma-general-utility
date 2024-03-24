FROM python:3.7 AS python_base
RUN     pip install --no-cache \
            Flask==2.2.2 \
            Flask-RESTful==0.3.9

FROM python_base AS runner
WORKDIR /opt/api
COPY ./medical_db_api.py ./
ENTRYPOINT ["./medical_db_api.py"]
