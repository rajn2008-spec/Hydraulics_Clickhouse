# Use official Python base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy only requirements first to leverage Docker layer caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Ensure Python treats 'app' and 'utils' as packages
RUN touch app/__init__.py
RUN touch utils/__init__.py

# Expose Flask port
EXPOSE 5000

# Run the app using module syntax
CMD ["python3", "-m", "app.main"]

