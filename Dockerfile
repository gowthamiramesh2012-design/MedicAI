FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy dependencies first (better caching, less pain)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Expose port Render expects
EXPOSE 10000

# Start the app with gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:10000", "app:app"]
