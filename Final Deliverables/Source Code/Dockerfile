FROM python:3.10.1
WORKDIR /app
ADD . /app

COPY requirements.txt /app
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python"]
CMD ["app.py"]