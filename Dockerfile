FROM python:3.9-slim

WORKDIR /python_code

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY  python_code/ .  

ENTRYPOINT ["python", "main.py"]