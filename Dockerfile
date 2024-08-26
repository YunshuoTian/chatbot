FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY extra-certs.pem /tmp/extra-certs.pem

RUN cat /tmp/extra-certs.pem >> $(python -m certifi)

RUN rm /tmp/extra-certs.pem

COPY . /app

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENV FLASK_APP=run.py

EXPOSE 5000

ENTRYPOINT ["/entrypoint.sh"]

CMD ["flask", "run", "--host=0.0.0.0"]