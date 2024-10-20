# Stage 1: Build stage
FROM python:3.9-alpine AS builder

# Set the working directory
WORKDIR /home/data

# Copy the text files from the data directory into the container
COPY data/IF.txt data/AlwaysRememberUsThisWay.txt ./
COPY scripts.py ./

# Install necessary libraries
RUN pip install --no-cache-dir pandas

# Stage 2: Final image
FROM python:3.9-alpine

# Set the working directory
WORKDIR /home/data

# Copy only the required files from the builder stage
COPY --from=builder /home/data ./

# Create an output directory
RUN mkdir output

# Command to run the script
CMD ["python", "scripts.py"]