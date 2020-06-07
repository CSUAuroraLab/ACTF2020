FROM python:3
ENV PYTHONUNBUFFERED 1
COPY ./www/  /www/
WORKDIR /www
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple