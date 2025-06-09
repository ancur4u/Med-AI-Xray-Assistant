# 📋 Installation Guide

## System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, macOS 10.15+, Ubuntu 18.04+
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 10GB free space (for models and dependencies)
- **Internet**: Required for initial setup and model download

### Recommended Requirements
- **OS**: Latest stable versions
- **Python**: 3.10 or 3.11
- **RAM**: 16GB or more
- **Storage**: 20GB+ free space
- **GPU**: CUDA-compatible GPU (optional, for faster processing)

## Step-by-Step Installation

### 1. Install Python

#### Windows
1. Download Python from [python.org](https://python.org)
2. Run installer and check "Add Python to PATH"
3. Verify installation: `python --version`

#### macOS
```bash
# Using Homebrew (recommended)
brew install python@3.11

# Or download from python.org
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
```

### 2. Install Ollama

#### Windows
1. Download Ollama from [ollama.ai](https://ollama.ai)
2. Run the installer
3. Open Command Prompt and verify: `ollama --version`

#### macOS
```bash
# Download and install
curl -fsSL https://ollama.ai/install.sh | sh

# Or using Homebrew
brew install ollama
```

#### Linux
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 3. Download LLaVA Model

```bash
# Start Ollama service
ollama serve

# In a new terminal, download LLaVA
ollama pull llava

# Verify model installation
ollama list
```

### 4. Clone Repository

```bash
git clone https://github.com/ancur4u/Med-AI-Xray-Assistant.git
cd med-ai-xray-assistant
```

### 5. Set Up Virtual Environment

#### Windows
```cmd
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### 6. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 7. Configure Application

#### Add Hospital Logo (Optional)
```bash
# Copy your logo file
cp /path/to/your/logo.png logo.png
```

#### Set Environment Variables (Optional)
```bash
# Create .env file
echo "OLLAMA_HOST=localhost:11434" > .env
echo "HOSPITAL_NAME=Your Medical Center" >> .env
```

### 8. Run Application

```bash
streamlit run app_ollama.py
```

The application will open in your default browser at `http://localhost:8501`

## Docker Installation (Alternative)

### Prerequisites
- Docker Desktop installed
- Docker Compose available

### Quick Setup
```bash
# Clone repository
git clone https://github.com/ancur4u/Med-AI-Xray-Assistant.git
cd med-ai-xray-assistant

# Build and run
docker-compose up -d

# Access application
open http://localhost:8501
```

### Docker Configuration

#### docker-compose.yml
```yaml
version: '3.8'
services:
  ollama:
    image: ollama/ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    environment:
      - OLLAMA_ORIGINS=*

  med-ai:
    build: .
    ports:
      - "8501:8501"
    depends_on:
      - ollama
    volumes:
      - ./logo.png:/app/logo.png
    environment:
      - OLLAMA_HOST=ollama:11434

volumes:
  ollama_data:
```

#### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app_ollama.py", "--server.address", "0.0.0.0"]
```

## Verification

### Test Installation
```bash
# Check Python
python --version

# Check Ollama
ollama --version
ollama list

# Check Streamlit
streamlit --version

# Test application
streamlit run app_ollama.py
```

### Troubleshooting Common Issues

#### Ollama Connection Error
```bash
# Ensure Ollama is running
ollama serve

# Check if LLaVA model is available
ollama list

# Test model
ollama run llava "Hello"
```

#### Port Already in Use
```bash
# Use different port
streamlit run app_ollama.py --server.port 8502
```

#### Permission Errors (Linux/macOS)
```bash
# Fix permissions
chmod +x setup.sh
sudo chown -R $USER:$USER ~/.ollama
```

#### Memory Issues
```bash
# Reduce image processing size
# Edit app_ollama.py and change MAX_WIDTH to 600
```

## Platform-Specific Notes

### Windows
- Use Command Prompt or PowerShell
- Antivirus software may interfere with Ollama
- Windows Defender might flag the application

### macOS
- May need to allow Ollama in Security & Privacy settings
- Use Terminal application
- Consider using Homebrew for easier package management

### Linux
- May need to install additional system packages
- Consider using systemd for Ollama service management
- Ensure proper user permissions for Docker

## Production Deployment

### Environment Variables
```bash
export OLLAMA_HOST=your-ollama-server:11434
export HOSPITAL_NAME="Your Hospital"
export DEBUG=false
export LOG_LEVEL=INFO
```

### Reverse Proxy Setup (Nginx)
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

### SSL Configuration
```bash
# Using Let's Encrypt
sudo certbot --nginx -d your-domain.com
```

## Next Steps

1. **Test the Application**: Upload sample X-ray images
2. **Customize Branding**: Add your hospital logo
3. **Configure Settings**: Adjust analysis parameters
4. **Read User Guide**: Understand all features
