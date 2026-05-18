FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8505

CMD ["streamlit", "run", "Recipt_Printer_V1.0.py", "--server.port=8505", "--server.address=0.0.0.0"]

