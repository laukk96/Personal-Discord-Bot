FROM python:3.13.1

# set the working directory in the docker container
WORKDIR /code

# copy dependencies file from my repo to working directory
COPY requirements.txt .
COPY .env .

# RUN command for dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

CMD ["python", "./dbot.py"]