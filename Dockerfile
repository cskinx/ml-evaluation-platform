FROM python:3.8

WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV TF_CPP_MIN_LOG_LEVEL=3

CMD ["python", "./src/dataloader.py"]