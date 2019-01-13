FROM python:3.5

ADD . /app

WORKDIR /app

# Install our flask app dependencies
RUN pip install -r requirements.txt

# Setup the database
RUN python setup.py

# Run the app
EXPOSE 5000

ENTRYPOINT ["python", "main.py"]
