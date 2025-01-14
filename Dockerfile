FROM python:3.9
RUN rm -rf /usr/src/app && mkdir /usr/src/app && apt update -y && apt install ffmpeg -y && apt install aria2 -y
WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app
COPY . .
RUN pip install -r requirements.txt 
CMD python main.py
