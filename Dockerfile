FROM python:3.9
RUN rm -rf /usr/src/app && mkdir /usr/src/app && apt update -y && apt install ffmpeg -y && apt install aria2 -y
WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app
COPY . .
RUN pip install -r requirements.txt && mv "__main__ (1)" yt-dlp && rm /usr/local/bin/yt-dlp && mv yt-dlp /usr/local/bin/yt-dlp && chmod 777 /usr/local/bin/yt-dlp && mv mp4decrypt /usr/bin/mp4decrypt && chmod 777 /usr/bin/mp4decrypt 
RUN rm -rf /usr/local/lib/python3.9/site-packages/yt_dlp && cd /usr/local/lib/python3.9/site-packages/ && git clone https://github.com/aryanchy451/yt-dlp && mv yt-dlp/yt_dlp yt_dlp && rm -rf yt-dlp && chmod 777 /usr/src/app/spjc
CMD python main.py
