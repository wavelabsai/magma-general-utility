FROM python:3.7

WORKDIR /app

RUN mkdir /app/logs

COPY . /app

RUN pip install -r requirements.txt

#CMD ["/bin/sh"]

CMD pytest -o log_cli=true --log-cli-level=INFO --log-format="%(asctime)s %(levelname)s %(message)s" --log-date-format="%Y-%m-%d %H:%M" --junitxml=/app/logs/output-$(date +"%Y%m%d_%H%M%S").xml

#CMD ["sh", "-c", "pytest -o --junitxml=./test_report/output-_$(date +"%Y%m%d_%H%M%S").xml"]
#CMD ["sh", "-c", "pytest -s test_login.py --env=stag && pytest -s test_send_ecard.py --env=stag"]
