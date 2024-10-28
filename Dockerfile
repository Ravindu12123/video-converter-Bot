FROM python:3.9.2
RUN mkdir /app && chmod 777 /app
WORKDIR /app
ENV DEBIAN_FRONTEND=noninteractive
RUN apt -qq update && apt -qq install -y git python3 python3-pip ffmpeg
#COPY requirements.txt .
#RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
RUN pip3 install --no-cache-dir -r requirements.txt
CMD ["bash","convertor.sh"]
