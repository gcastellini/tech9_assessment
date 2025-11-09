# ===============================
# 1. Base image
# ===============================
FROM python:3.11-slim

# ===============================
# 2. Install system dependencies
# ===============================
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ===============================
# 3. Install Ollama CLI
# ===============================
RUN curl -fsSL https://ollama.ai/install.sh | sh

# ===============================
# 4. Create project directory
# ===============================
WORKDIR /app

# ===============================
# 5. Copy project files
# ===============================
COPY . .

# ===============================
# 6. Install Python dependencies
# ===============================
RUN pip install --no-cache-dir -r requirements.txt

# ===============================
# 7. Expose Ollama API port
# ===============================
EXPOSE 11434

# ===============================
# 8. Environment setup
# ===============================
ENV PYTHONUNBUFFERED=1

# ===============================
# 9. Run Ollama and the app (pull model dynamically)
# ===============================
CMD ["bash", "-c", "ollama serve & sleep 5 && ollama pull mistral && python main.py"]