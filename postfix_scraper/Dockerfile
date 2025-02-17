FROM python:3.9-slim

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "postfix_scraper.py"]
EXPOSE 9555