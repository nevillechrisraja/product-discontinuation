FROM python:3.8-slim

WORKDIR product-discontinuation

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "src/main.py"]