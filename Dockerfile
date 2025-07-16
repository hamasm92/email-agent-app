# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy everything to the container
COPY . .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Set environment variable if needed
# ENV GOOGLE_API_KEY=your_key_here

# Expose the default port for Gradio
EXPOSE 7860

# Run the app
CMD ["python", "gradio_app.py"]
