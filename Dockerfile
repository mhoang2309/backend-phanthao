
FROM python:3.8-slim

# install dependencies
RUN apt-get update -y && apt install -y build-essential python-dev \
                        libpq-dev zlib1g-dev libtiff5-dev libjpeg62-turbo-dev libfreetype6-dev \
                        liblcms2-dev libwebp-dev graphviz-dev gettext ffmpeg libsm6 libxext6 nginx
# set the working directory in the container
WORKDIR /code

# copy the dependencies file to the working directory
COPY requirements.txt .

# install requirements
RUN pip install -U pip wheel cmake
RUN pip install -r requirements.txt
# copy the content of the local src directory to the working directory
COPY . /code

RUN chmod +x Deploy.sh
# expose running port to outside container
EXPOSE 8000

# command to run on container start
CMD ./Deploy.sh
