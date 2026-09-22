
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Hugging Face Spaces expose port 7860
EXPOSE 7860

# Start the FastAPI app on port 7860 using the app.py wrapper
CMD ["python", "app.py"]
