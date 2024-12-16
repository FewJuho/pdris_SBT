FROM python:3.9-slim

WORKDIR /pdris

COPY requirements.txt requirements-test.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r requirements-test.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
