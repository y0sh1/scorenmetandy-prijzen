# Use an official Python runtime as a parent image
FROM python:3-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variable for Slack Webhook URL
ENV SLACK_WEBHOOK_URL="your_slack_webhook_url_here"

# Run main.py when the container launches
CMD ["python", "main.py"]