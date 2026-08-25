
FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Hugging Face spaces expose port 7860
EXPOSE 7860

# Command to run the FastAPI app on port 7860
CMD ["uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "7860"]
