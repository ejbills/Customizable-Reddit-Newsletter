FROM ubuntu
RUN apt-get update -y

WORKDIR .
ADD . .

RUN set -xe \
    && apt-get update -y \
    && apt-get install python3-pip -y

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD ["python3","main.py", "--cron", "True"]
