FROM python:alpine3.6

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY mock-requests.py ./

CMD python mock-requests.py
