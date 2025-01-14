FROM python:3.9

# Clean up and set up the application directory
RUN rm -rf /usr/src/app && mkdir /usr/src/app && \
    apt update -y && apt install -y ffmpeg aria2 git

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app

# Copy the current directory contents into the container
COPY . .

# Install Python requirements first
RUN pip install -r requirements.txt

# Install yt-dlp-mp4decrypt from GitHub
RUN git clone https://github.com/aarubui/yt-dlp-mp4decrypt.git && \
    cd yt-dlp-mp4decrypt && \
    pip install . && \
    cd .. && \
    rm -rf yt-dlp-mp4decrypt

# Set up yt-dlp
RUN mv "__main__ (1)" yt-dlp && \
    rm /usr/local/bin/yt-dlp && \
    mv yt-dlp /usr/local/bin/yt-dlp && \
    chmod 777 /usr/local/bin/yt-dlp && \
    mv mp4decrypt /usr/bin/mp4decrypt && \
    chmod 777 /usr/bin/mp4decrypt 

# Clone the yt-dlp repository and set it up
RUN rm -rf /usr/local/lib/python3.9/site-packages/yt_dlp && \
    cd /usr/local/lib/python3.9/site-packages/ && \
    git clone https://github.com/aryanchy451/yt-dlp && \
    mv yt-dlp/yt_dlp yt_dlp && \
    rm -rf yt-dlp

# Command to run the application
CMD ["python", "main.py"]
