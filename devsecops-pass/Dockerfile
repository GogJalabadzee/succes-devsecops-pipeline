FROM python:3.12-slim

# Secure: run as non-root.
RUN useradd -m appuser

WORKDIR /app
COPY app.py .

USER appuser
EXPOSE 8000

CMD ["python", "app.py"]
