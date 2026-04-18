FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY manage.py .
COPY photoupload ./photoupload
COPY gallery ./gallery

RUN chgrp -R 0 /app && chmod -R g=u /app

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "photoupload.wsgi"]