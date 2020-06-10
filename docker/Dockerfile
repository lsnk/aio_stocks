FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src/ .

ENV PYTHONPATH=/app

ENV USR_LOCAL_BIN=/usr/local/bin/
COPY ./docker/scripts/*.sh $USR_LOCAL_BIN/
RUN for i in $USR_LOCAL_BIN/*.sh; do \
    sed -i 's/\r//' $i; \
    chmod +x $i; \
    done

EXPOSE 8000

ENTRYPOINT ["entrypoint.sh"]
