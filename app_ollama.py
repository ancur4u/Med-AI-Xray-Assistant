import streamlit as st
from PIL import Image
import base64
import requests
import io
import textwrap
from fpdf import FPDF
import os
import re

# Streamlit page setup
st.set_page_config(page_title="🧠 LLaVA X-ray Medical Assistant (Offline via Ollama)", layout="centered")

st.title("🧠 Med AI: X-ray Assistant")

# Get user location
@st.cache_data
def get_user_location():
    try:
        geo = requests.get("https://ipinfo.io").json()
        return f"{geo.get('city', '')}, {geo.get('region', '')}"
    except:
        return "Unknown Location"

class SafePDF(FPDF):
    """Custom PDF class with better error handling"""
    
    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=15)
        self.set_margins(20, 20, 20)  # Left, Top, Right margins
        self.font_styles = {
            'regular': '',
            'bold': 'B',
            'italic': 'I',
            'bold_italic': 'BI'
        }
        
    def safe_cell(self, w, h, txt='', border=0, ln=0, align='', fill=False, style='regular'):
        """Safe cell method with text cleaning and style support"""
        # Clean text and handle encoding
        clean_txt = self.clean_text(txt)
        
        # Set font style
        current_font = self.font_family
        self.set_font(current_font, self.font_styles.get(style, ''), self.font_size_pt)
        
        try:
            self.cell(w, h, clean_txt, border, ln, align, fill)
        except Exception as e:
            # Fallback: use simplified text
            fallback_txt = re.sub(r'[^\w\s-.,;:()!?]', '', clean_txt)[:50]
            self.cell(w, h, fallback_txt, border, ln, align, fill)
    
    def safe_multi_cell(self, w, h, txt, border=0, align='L', fill=False, style='regular'):
        """Safe multi_cell method with better text handling and style support"""
        # Clean and prepare text
        clean_txt = self.clean_text(txt)
        if not clean_txt.strip():
            return
        
        # Set font style
        current_font = self.font_family
        self.set_font(current_font, self.font_styles.get(style, ''), self.font_size_pt)
        
        # Use proper text wrapping with multi_cell
        try:
            self.multi_cell(w, h, clean_txt, border, align, fill)
        except Exception as e:
            # Fallback: split text manually
            lines = clean_txt.split('\n')
            for line in lines:
                if line.strip():
                    try:
                        self.multi_cell(w, h, line.strip(), border, align, fill)
                    except:
                        # Last resort: truncate and continue
                        self.multi_cell(w, h, line[:100] + "...", border, align, fill)
                    
    def add_logo(self, logo_path, x=None, y=None, w=50, h=50):
        """Add hospital logo to PDF"""
        try:
            if os.path.exists(logo_path):
                # Center the logo if x,y not provided
                if x is None:
                    x = (self.w - w) / 2
                if y is None:
                    y = 30
                
                self.image(logo_path, x, y, w, h)
                return True
            else:
                # Create a simple text logo if image not found
                self.set_font('Arial', 'B', 20)
                self.safe_cell(0, 10, "🏥 MEDICAL CENTER", ln=True, align='C', style='bold')
                return False
        except Exception as e:
            # Fallback to text logo
            self.set_font('Arial', 'B', 20)
            self.safe_cell(0, 10, "🏥 MEDICAL CENTER", ln=True, align='C', style='bold')
            return False
    
    def clean_text(self, text):
        """Clean text for PDF compatibility"""
        if not text:
            return ""
        
        # Remove problematic characters
        text = str(text)
        text = re.sub(r'[^\w\s\-.,;:()!?\n\r\u00A0-\u017F\u0100-\u024F]', '', text)
        
        # Replace multiple spaces/newlines
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'\n+', '\n', text)
        
        return text.strip()

def create_pdf_report(results, location):
    """Create PDF report with better error handling"""
    pdf = SafePDF()
    
    # Try to add fonts, fallback to default if needed
    try:
        # Try common font paths
        font_paths = [
            "DejaVuSans.ttf",
            "/System/Library/Fonts/Helvetica.ttc",  # macOS
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Linux
            "C:/Windows/Fonts/arial.ttf"  # Windows
        ]
        
        font_loaded = False
        for font_path in font_paths:
            try:
                if os.path.exists(font_path):
                    pdf.add_font("CustomFont", "", font_path, uni=True)
                    pdf.add_font("CustomFont", "B", font_path, uni=True)  # Bold
                    pdf.add_font("CustomFont", "I", font_path, uni=True)  # Italic
                    pdf.add_font("CustomFont", "BI", font_path, uni=True)  # Bold Italic
                    pdf.set_font("CustomFont", "", 12)
                    font_loaded = True
                    break
            except:
                continue
        
        if not font_loaded:
            # Use built-in fonts
            pdf.set_font("Arial", "", 12)
            
    except Exception as e:
        st.warning(f"Font loading issue: {e}. Using default font.")
        pdf.set_font("Arial", "", 12)

    # Add title page with logo
    pdf.add_page()
    
    # Try to add hospital logo (place logo.png in the same directory)
    logo_added = pdf.add_logo("logo.png", w=60, h=60)
    
    if logo_added:
        pdf.ln(70)  # Space after logo
    else:
        pdf.ln(20)  # Space after text logo
    
    # Title
    pdf.set_font_size(18)
    pdf.safe_cell(0, 12, "X-RAY MEDICAL ANALYSIS REPORT", ln=True, align='C', style='bold')
    pdf.ln(10)
    
    # Subtitle
    pdf.set_font_size(12)
    pdf.safe_cell(0, 8, f"Generated for location: {location}", ln=True, align='C', style='italic')
    pdf.safe_cell(0, 8, f"Total images analyzed: {len(results)}", ln=True, align='C', style='italic')
    
    # Add timestamp
    from datetime import datetime
    timestamp = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    pdf.safe_cell(0, 8, f"Report generated on: {timestamp}", ln=True, align='C', style='italic')
    
    pdf.ln(15)
    
    # Add disclaimer box
    pdf.set_font_size(10)
    pdf.safe_multi_cell(0, 6, "IMPORTANT DISCLAIMER: This AI-generated analysis is for educational and informational purposes only. It should not be used as a substitute for professional medical diagnosis, treatment, or advice. Always consult with qualified healthcare professionals for medical decisions.", style='italic')

    # Add results for each image
    for i, (name, report) in enumerate(results, 1):
        pdf.add_page()
        
        # Image header with decorative line
        pdf.set_font_size(16)
        pdf.safe_cell(0, 10, f"ANALYSIS REPORT {i}", ln=True, align='C', style='bold')
        pdf.ln(3)
        pdf.set_font_size(12)
        pdf.safe_cell(0, 8, f"Image: {name}", ln=True, align='C', style='italic')
        
        # Add a line separator
        pdf.ln(8)
        pdf.line(20, pdf.get_y(), pdf.w-20, pdf.get_y())
        pdf.ln(8)
        
        # Reset font size for content
        pdf.set_font_size(11)
        
        # Process report content
        if report:
            # Process the entire report as one block for better formatting
            report_text = report.strip()
            
            # Split by double newlines first to get major sections
            major_sections = report_text.split('\n\n')
            
            for section in major_sections:
                if not section.strip():
                    continue
                    
                # Split each section by single newlines
                lines = section.split('\n')
                section_text = ""
                
                for line_idx, line in enumerate(lines):
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Check if this is a header line
                    is_header = (
                        any(keyword in line.lower() for keyword in ['medical analysis:', 'treatment plan:', 'suggested treatment', 'medications:', 'possible medications', 'emotional healing', 'healing message:']) or
                        line.endswith(':') or
                        '**' in line or
                        any(char in line for char in ['🩻', '🩺', '💊', '💙'])
                    )
                    
                    if is_header:
                        # If we have accumulated text, output it first
                        if section_text.strip():
                            pdf.set_font_size(10)
                            pdf.safe_multi_cell(0, 5, section_text.strip(), style='regular')
                            section_text = ""
                            pdf.ln(3)
                        
                        # Output header in dark blue and bold
                        clean_header = re.sub(r'\*\*([^*]+)\*\*', r'\1', line)
                        clean_header = re.sub(r'[🩻🩺💊💙]', '', clean_header).strip()
                        
                        pdf.set_font_size(12)
                        pdf.set_text_color(0, 51, 102)  # Dark blue color
                        pdf.safe_cell(0, 8, clean_header, ln=True, style='bold')
                        pdf.set_text_color(0, 0, 0)  # Reset to black
                        pdf.ln(2)
                    else:
                        # Accumulate regular content
                        if section_text:
                            section_text += " " + line
                        else:
                            section_text = line
                
                # Output any remaining accumulated text
                if section_text.strip():
                    pdf.set_font_size(10)
                    pdf.safe_multi_cell(0, 5, section_text.strip(), style='regular')
                    pdf.ln(4)  # Small space between sections

    # Add specialist advice page
    pdf.add_page()
    pdf.set_font_size(16)
    pdf.safe_cell(0, 10, "SPECIALIST RECOMMENDATIONS", ln=True, align='C', style='bold')
    pdf.ln(10)
    
    # Add a line separator
    pdf.line(20, pdf.get_y(), pdf.w-20, pdf.get_y())
    pdf.ln(10)
    
    pdf.set_font_size(11)
    pdf.set_text_color(0, 51, 102)  # Dark blue
    pdf.safe_cell(0, 8, "Recommended Next Steps:", ln=True, style='bold')
    pdf.set_text_color(0, 0, 0)  # Reset to black
    pdf.ln(3)
    
    pdf.set_font_size(10)
    
    # Format the specialist advice with better structure
    location_text = f"Based on your location: {location}, we recommend consulting with:"
    pdf.safe_multi_cell(0, 5, location_text, style='regular')
    pdf.ln(3)
    
    specialists = [
        "• Orthopedic specialists for bone-related findings",
        "• Radiologists for detailed image interpretation",
        "• General practitioners for initial consultation",
        "• Pulmonologists for chest X-ray findings"
    ]
    
    for specialist in specialists:
        pdf.safe_multi_cell(0, 5, specialist, style='regular')
        pdf.ln(1)
    
    pdf.ln(4)
    
    # How to find specialists section
    pdf.set_text_color(0, 51, 102)  # Dark blue
    pdf.safe_cell(0, 7, "How to Find Specialists:", ln=True, style='bold')
    pdf.set_text_color(0, 0, 0)  # Reset to black
    pdf.ln(2)
    
    find_methods = [
        "• Search 'specialist name + near me' in Google Maps",
        "• Use healthcare provider directories",
        "• Contact your insurance provider for in-network specialists",
        "• Consider telemedicine options for initial consultations"
    ]
    
    for method in find_methods:
        pdf.safe_multi_cell(0, 5, method, style='regular')
        pdf.ln(1)
    
    pdf.ln(4)
    
    # Emergency signs section
    pdf.set_text_color(0, 51, 102)  # Dark blue
    pdf.safe_cell(0, 7, "Emergency Signs to Watch For:", ln=True, style='bold')
    pdf.set_text_color(0, 0, 0)  # Reset to black
    pdf.ln(2)
    
    emergency_signs = [
        "• Severe or worsening pain",
        "• Difficulty breathing",
        "• Signs of infection (fever, redness, swelling)",
        "• Any concerning symptoms mentioned in the analysis above"
    ]
    
    for sign in emergency_signs:
        pdf.safe_multi_cell(0, 5, sign, style='regular')
        pdf.ln(1)
    
    pdf.ln(4)
    
    final_note = "Remember: Early consultation with healthcare professionals leads to better outcomes."
    pdf.safe_multi_cell(0, 5, final_note, style='regular')
    
    # Add footer
    pdf.ln(15)
    pdf.set_font_size(8)
    pdf.safe_cell(0, 5, "This report was generated using AI analysis and should be reviewed by medical professionals.", ln=True, align='C', style='italic')

    return pdf

location = get_user_location()
st.info(f"📍 Detected Location: {location}")

# Upload X-rays
uploaded_files = st.file_uploader("📤 Upload X-ray Images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
OLLAMA_API = "http://localhost:11434/api/generate"
results = []

# Process uploaded files
if uploaded_files:
    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file).convert("RGB")
        max_width = 800
        w, h = image.size
        if w > max_width:
            image = image.resize((max_width, int(h * max_width / w)))
        st.image(image, caption=uploaded_file.name)

        # Prepare image for Ollama
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")
        img_b64 = base64.b64encode(buffer.getvalue()).decode()

        prompt = """
You are a medical imaging assistant. Analyze this X-ray and generate a clinical report with:

**Medical Analysis:**  
<Your findings>

**Suggested Treatment Plan:**  
<Recommendations>

**Possible Medications:**  
<Generic drug names>

**Emotional Healing Message:**  
<Empathetic encouragement>

in bullet points word wrapped.

Use confident, medical language and respond only based on the image.
"""

        with st.spinner(f"Analyzing {uploaded_file.name}..."):
            try:
                response = requests.post(OLLAMA_API, json={
                    "model": "llava",
                    "prompt": prompt,
                    "images": [img_b64],
                    "stream": False
                })
                response.raise_for_status()
                result_text = response.json()["response"]
                results.append((uploaded_file.name, result_text))
                st.markdown(f"### 📝 Report for `{uploaded_file.name}`")
                st.markdown(result_text)
            except Exception as e:
                st.error(f"❌ Error analyzing {uploaded_file.name}: {e}")
                # Add a placeholder result for PDF generation
                results.append((uploaded_file.name, f"Analysis failed: {str(e)}"))

    # Generate PDF Report
    if results:
        st.markdown("---")
        st.subheader("📄 Generate PDF Report")
        
        if st.button("🔄 Generate PDF Report"):
            with st.spinner("Creating PDF report..."):
                try:
                    pdf = create_pdf_report(results, location)
                    pdf_path = "xray_report.pdf"
                    pdf.output(pdf_path)
                    
                    # Verify PDF was created successfully
                    if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
                        with open(pdf_path, "rb") as f:
                            pdf_data = f.read()
                        
                        st.success("✅ PDF report generated successfully!")
                        st.download_button(
                            label="📥 Download PDF Report", 
                            data=pdf_data,
                            file_name="xray_medical_report.pdf",
                            mime="application/pdf"
                        )
                        
                        # Clean up
                        try:
                            os.remove(pdf_path)
                        except:
                            pass
                    else:
                        st.error("❌ Failed to generate PDF report")
                        
                except Exception as e:
                    st.error(f"❌ Error creating PDF: {e}")
                    st.info("💡 Try using a simpler text format or check font installation")
else:
    st.info("📎 Upload at least one X-ray image to begin analysis.")

# Add some helpful information
st.markdown("---")
st.markdown("""
### ℹ️ About This Tool
- Uses LLaVA model running locally via Ollama
- Provides AI-assisted X-ray analysis for educational purposes
- Generates professional PDF reports with hospital branding
- **Disclaimer**: This tool is for educational purposes only and should not replace professional medical diagnosis or treatment.
- **Privacy**: All processing is done locally, no data is sent to external servers.
""")