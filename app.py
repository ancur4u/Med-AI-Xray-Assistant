import streamlit as st
from PIL import Image
import base64
import requests
import io

st.set_page_config(page_title="🩻 MedGemma LMStudio Assistant", layout="centered")
st.title("🧠 MedGemma X-ray Assistant (LM Studio)")

LMSTUDIO_API = "http://localhost:1234/v1/chat/completions"

uploaded_file = st.file_uploader("📤 Upload an X-ray image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded X-ray", use_container_width=True)

    # Convert image to base64
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_b64 = base64.b64encode(buffered.getvalue()).decode()

    # Define system prompt
    system_prompt = """
You are a highly capable and specialized medical imaging assistant trained on radiological data, anatomy, and clinical decision-making. Your task is to analyze medical images, particularly X-rays, and provide a precise, confident response.

When an X-ray image is uploaded:
1. Carefully inspect the image and identify relevant anatomical features, injuries, or abnormalities such as fractures, dislocations, calcifications, or soft tissue anomalies.
2. Based strictly on the image, generate a clear, clinical interpretation in confident medical language.
3. Suggest a possible treatment plan based on your findings. This may include conservative options, surgical recommendations, medications, or supportive care.
4. List any generic medications that may be typically prescribed in such conditions.
5. Include a concise, empathetic message to emotionally support the user — without downplaying the situation or deferring unnecessarily to human practitioners.
6. Never state that you are not a doctor or that an in-person consultation is required — unless the image is unreadable or missing.

Format your response as follows:

**🩻 Medical Analysis:**  
<Your confident X-ray interpretation>

**🩺 Suggested Treatment Plan:**  
<Treatment course including clinical advice>

**💊 Possible Medications:**  
<Generic medication names or supportive agents>

**💙 Emotional Healing Message:**  
<A compassionate message encouraging recovery and emotional strength>
"""

    # Define user prompt
    user_prompt = "Please analyze the uploaded X-ray and provide a medical interpretation, treatment plan, medications, and emotional healing message."

    if st.button("🧠 Analyze X-ray"):
        with st.spinner("Waiting for MedGemma via LM Studio..."):
            headers = {"Content-Type": "application/json"}
            payload = {
                "model": "medgemma-4b-it",
                "messages": [
                    { "role": "system", "content": system_prompt },
                    { "role": "user", "content": [
                        { "type": "text", "text": user_prompt },
                        { "type": "image_url", "image_url": { "url": f"data:image/jpeg;base64,{img_b64}" } }
                    ]}
                ],
                "temperature": 0.7,
                "max_tokens": 1024,
                "stream": False
            }

            try:
                res = requests.post(LMSTUDIO_API, headers=headers, json=payload)
                res.raise_for_status()
                result = res.json()
                content = result["choices"][0]["message"]["content"]
                st.markdown("### ✅ AI Medical Report")
                st.markdown(content)
            except Exception as e:
                st.error(f"❌ Error: {e}")
else:
    st.info("📎 Please upload an X-ray image to begin analysis.")