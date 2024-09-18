# Use the official Python image.
FROM python:3.12-slim

# Set the working directory.
WORKDIR /app

# Copy the requirements.txt file.
COPY requirements.txt ./

# Install dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application.
COPY . .

# Expose the port that the app runs on.
EXPOSE 5000

# Command to run the application.
CMD ["flask", "run", "--host=0.0.0.0"]
