FROM python:3.9-buster

RUN apt-get update -y && apt-get upgrade -y

COPY . /app

RUN apt-get install -y git libboost-all-dev libgoogle-perftools-dev \
    && mkdir /apps \
    && cd /apps \
	# sparsehash is required by Gargantua
    && git clone https://github.com/sparsehash/sparsehash.git \
	&& cd sparsehash \
	&& ./configure \
	&& make \
	&& make install \
	&& cd /apps \
	# Gargantua is used to align subtitles
    && git clone https://github.com/braunefe/Gargantua.git \
	&& cd Gargantua \
	&& chmod u+x clean.sh \
	&& chmod u+x prepare-data.sh \
	&& ./prepare-filesystem.sh \
	&& cd src \
	&& make \
	&& cd /apps 

WORKDIR /app

RUN useradd -ms /bin/bash gargantua_user \
    && chown -R gargantua_user /apps \
    && chown -R gargantua_user /app
USER gargantua_user

RUN pip install -r requirements.txt

EXPOSE 80

CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
