FROM python:3.11

RUN pip install --upgrade pip

# Set the working directory
RUN mkdir /workspace
WORKDIR /workspace