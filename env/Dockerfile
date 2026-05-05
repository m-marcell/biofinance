FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ids.csv ./
COPY script.py ./
COPY .env ./

COPY . .

CMD [ "python", "./script.py" ]
