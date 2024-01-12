FROM python:3.11.4

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


COPY main.py /app/

EXPOSE 8004

CMD ["uvicorn", "main:ctms", "--host", "0.0.0.0", "--port", "8004"]