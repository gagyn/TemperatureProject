FROM python:3

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN pip install ./src

CMD [ "python", "-u", "./src/TemperatureScanner/ScannerApiController.py" ]
