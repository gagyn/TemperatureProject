FROM python:3

WORKDIR /app

# This dockerfile should always get the entire ./src/ folder as context

COPY ./TemperatureScanner/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080
COPY . .
RUN pip install .

CMD ["uwsgi", "TemperatureScanner/app.ini"]