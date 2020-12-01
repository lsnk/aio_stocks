FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev libxml2-dev libxslt-dev libffi-dev libz-dev python3-dev \
    build-essential

# Install python packages using `no-binary`
# to make builds there's no wheels for ARM
COPY requirements.txt .
RUN pip install -r requirements.txt --no-binary :all:

# Remove system build dependencies
RUN apt-get remove -y build-essential

# Copy project source
COPY src/ .
ENV PYTHONPATH=/app

# Copy scripts and make them executable
ENV USR_LOCAL_BIN=/usr/local/bin/
COPY ./docker/scripts/*.sh $USR_LOCAL_BIN/
RUN for i in $USR_LOCAL_BIN/*.sh; do \
    sed -i 's/\r//' $i; \
    chmod +x $i; \
    done

EXPOSE 8000

ENTRYPOINT ["entrypoint.sh"]
