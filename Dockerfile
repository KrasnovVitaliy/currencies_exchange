FROM python:3
WORKDIR /app
ADD currencies_exchange/* /app/
RUN pip install -r /app/requirements.txt
CMD [ "python", "./main.py" ]