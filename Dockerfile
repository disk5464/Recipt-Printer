FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8505

#https://medium.com/@dongaresuyash/dockerizing-your-streamlit-app-a-beginner-friendly-guide-b63d1214d0ad