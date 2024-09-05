FROM python:3.11
RUN mkdir /app
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["/app/run.sh"]
