FROM python:3.8-slim

RUN apt update -y && apt install awscli -y

WORKDIR product-discontinuation

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "src/main.py"]