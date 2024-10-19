# Use the official Python image as the base image
FROM python:3.9-slim

RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install any dependencies specified in requirements.txt
COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Expose port 7860 for the FastAPI app
EXPOSE 7860

# Especifica el comando predeterminado a ejecutar cuando se inicie el contenedor
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
