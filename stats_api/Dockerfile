FROM python:3.8
WORKDIR /app
COPY . .
RUN pip install flask bs4 requests pytest pytest-cov
EXPOSE 5000
ENTRYPOINT ["python", "app.py"]