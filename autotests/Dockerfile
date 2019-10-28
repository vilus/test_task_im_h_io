FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /autotests
RUN mkdir /autotests/front

WORKDIR /autotests
COPY requirements.txt ./
COPY ./front/requirements.txt ./front/

RUN pip install --no-cache-dir -r requirements.txt

COPY ./front .

CMD ["pytest"]
