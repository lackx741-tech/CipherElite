# Use a lightweight Python image
FROM python:3.10-slim-bookworm



LABEL org.opencontainers.image.title="V26Userbot"
LABEL org.opencontainers.image.description="Advanced Telegram Userbot"
LABEL org.opencontainers.image.authors="V26 Dev"
LABEL org.opencontainers.image.source="https://github.com/lackx741-tech/V26Userbot"


RUN echo "====================================" && \
    echo "  __   _____  __                   " && \
    echo "  \ \ / /__ \/ /_                  " && \
    echo "   \ V /  / / '_ \                 " && \
    echo "    \_/  /_/|_.__/                 " && \
    echo "====================================" && \
    echo "      🚀  V 2 6  U S E R B O T      " && \
    echo "          Powered by V26            " && \
    echo "===================================="

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies
RUN echo "⚙️ Preparing System Dependencies..."
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install Python modules
COPY requirements.txt .
RUN echo "📦 Installing Python Modules..."
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of your bot's code into the container
COPY . .

# Final success message before starting
RUN echo "✅ Build Complete! Ready to launch."

# Command to start the bot
CMD ["python3", "main.py"]
