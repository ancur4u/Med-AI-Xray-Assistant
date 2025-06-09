# 🩻 Med AI: X-ray Assistant

**A powerful AI-driven X-ray analysis tool that provides instant medical imaging insights using LLaVA vision models with professional PDF report generation.**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![LLaVA](https://img.shields.io/badge/Model-LLaVA-green.svg)](https://github.com/haotian-liu/LLaVA)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

## 🚀 Latest Updates - v3.0 (Professional Release)

### ✨ New Features
- **🏥 Hospital Branding**: Custom logo integration on PDF reports
- **🎨 Professional PDF Formatting**: Dark blue headers, proper spacing, clean layout
- **📄 Enhanced Reports**: Comprehensive medical analysis with treatment recommendations
- **⚡ Batch Processing**: Analyze multiple X-ray images simultaneously
- **🌍 Location-Based Recommendations**: Automatic specialist referrals based on user location
- **🔒 HIPAA Compliant**: Local processing via Ollama (no cloud dependency)

## 🎯 Key Features

### 🩻 **Advanced X-ray Analysis**
- **Instant AI Analysis**: Results in under 60 seconds using LLaVA models
- **Multi-Modal Processing**: Upload multiple X-ray formats (PNG, JPG, JPEG)
- **Comprehensive Reports**: Medical findings, treatment plans, medication suggestions
- **Emotional Support**: Empathetic patient care messages included

### 📄 **Professional PDF Reports**
- **Hospital Branding**: Custom logo integration (60x60px recommended)
- **Medical-Grade Formatting**: Dark blue headers, proper typography
- **Structured Layout**: Organized sections with clean spacing
- **Timestamp & Location**: Automatic report metadata
- **Disclaimer Integration**: Proper medical disclaimers

### 🔒 **Security & Privacy**
- **Local Processing**: All analysis runs locally via Ollama
- **No Cloud Dependency**: Complete data privacy and security
- **HIPAA Compliance**: Suitable for healthcare environments
- **Offline Capability**: Works without internet connection

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Ollama installed and running
- LLaVA model downloaded

### Installation

```bash
# Clone the repository
git clone https://github.com/ancur4u/Med-AI-Xray-Assistant.git
cd med-ai-xray-assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install and setup Ollama
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llava

# Add your hospital logo (optional)
cp your_hospital_logo.png logo.png

# Run the application
streamlit run app_ollama.py
```

## 💻 Usage

### Basic Workflow
1. **🚀 Launch**: Run the Streamlit application
2. **📤 Upload**: Select X-ray images (supports multiple files)
3. **🔄 Analyze**: AI processes images using LLaVA model
4. **📋 Review**: Examine detailed analysis results
5. **📄 Export**: Generate professional PDF reports

## 📊 Performance Metrics

| Metric | Value | Notes |
|--------|-------|-------|
| **Analysis Time** | <60 seconds | Per X-ray image |
| **Supported Formats** | PNG, JPG, JPEG | Standard medical imaging formats |
| **Batch Capacity** | 100+ images | Limited by system memory |
| **PDF Generation** | <5 seconds | Professional report creation |
| **Memory Usage** | ~2GB | Including LLaVA model |
| **Accuracy** | Educational use | Not for clinical diagnosis |

## 🩺 Medical Disclaimer

⚠️ **IMPORTANT MEDICAL DISCLAIMER** ⚠️

This AI tool is designed for **educational and screening purposes only**. It should **NOT** be used as a substitute for professional medical diagnosis, treatment, or advice. Always consult qualified healthcare professionals for medical decisions.

**Key Points:**
- ✅ Educational and training use
- ✅ Preliminary screening assistance
- ✅ Medical research support
- ❌ Not for clinical diagnosis
- ❌ Not FDA approved
- ❌ Not a replacement for radiologists

## 🤝 Contributing

We welcome contributions from the medical and AI community!

See [Contributing.md](Contributing.md) for detailed guidelines.

## 📜 License

This project is licensed under the MIT License - see the [MIT](LICENSE) file for details.

## 📞 Support & Contact

- 📧 **Email**: ankr.prshr.ai@gmail.com

---

**🏥 Advancing healthcare through intelligent technology - one X-ray at a time!**
