FROM python:3.7.2
MAINTAINER FilosoF

COPY requirements.txt /mnt/
RUN python3.7 -m venv /usr/share/python3/venv \
    && /usr/share/python3/venv/bin/pip install -U pip \
    && usr/share/python3/venv/bin/pip install -Ur /mnt/requirements.txt

WORKDIR /usr/share/python3/
COPY parse_sber_ats.py .

ARG param_search="проверка"
ENTRYPOINT ["python", "./parse_sber_ats.py", "param_search"]
