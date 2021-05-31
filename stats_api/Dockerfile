FROM python:3.8
WORKDIR /app
COPY . .
RUN pip install flask requests bs4
EXPOSE 5001
ENTRYPOINT ["python", "app.py"]