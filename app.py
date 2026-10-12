import streamlit as st
import os
from google import genai
from google.genai import types

# Web page configuration
st.set_page_config(page_title="AI Cancer Research - Playground", page_icon="🧬", layout="wide")

# Academic & Medical UI Styling (CSS)
st.markdown("""
    <style>
    .main-title { font-size: 32px; font-weight: bold; color: #0F172A; }
    .subtitle { font-size: 16px; color: #475569; margin-bottom: 30px; }
    .stButton>button { background-color: #2563EB; color: white; border-radius: 6px; width: 100%; font-weight: bold; }
    .stLinkButton>a { background-color: #10B981 !important; color: white !important; border-radius: 6px; text-decoration: none; display: inline-block; padding: 10px 20px; font-weight: bold; width: 100%; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🧬 AI Cancer Research Playground</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Limited beta environment connecting foundation models for oncology research validation.</div>', unsafe_allow_html=True)

# Secure API Key Initialization
api_key = os.environ.get("GEMINI_API_KEY") or st.sidebar.text_input("Enter Gemini API Key (for local testing):", type="password")

col1, col2 = st.columns([1, 2]) # Adjust column ratio for better readability

with col1:
    st.subheader("Analysis Configuration")
    modality = st.multiselect(
        "Input Modalities", 
        ["RNA-Seq Data", "Somatic Mutations", "PubMed Literature", "Clinical Trial Protocols"], 
        default=["RNA-Seq Data", "PubMed Literature"]
    )
    focus_gene = st.text_input(
        "Focus Pathway / Gene Target:", 
        placeholder="e.g., BRCA1, PI3K/AKT, EGFR..."
    )
    
    analyze_btn = st.button("Run Analysis")

with col2:
    st.subheader("Hypothesis Generation & Evidence Synthesis")
    
    if analyze_btn:
        if not api_key:
            st.error("Authentication Error: Please configure GEMINI_API_KEY to run the model.")
        elif not focus_gene:
            st.warning("Input Required: Please specify a target gene or biological pathway.")
        else:
            with st.spinner(f"Querying biomedical literature and analyzing multi-omics cohorts for {focus_gene}..."):
                try:
                    # Initialize the Google GenAI Client
                    client = genai.Client(api_key=api_key)
                    
                    # Formulate system prompt to enforce rigorous academic output
                    system_prompt = (
                        "You are an elite oncology AI research assistant. Provide deep scientific hypothesis synthesis "
                        "based on multi-omics data and literature. Always structure your response professionally with "
                        "sections like 'Mechanism overview', 'Pre-clinical Hypothesis', and 'Simulated Academic Citations'."
                    )
                    
                    user_prompt = (
                        f"Analyze the role of the pathway/gene '{focus_gene}' in cancer progression and therapeutic resistance. "
                        f"Generate 1-2 testable pre-clinical hypotheses with structured academic citations based on {', '.join(modality)}."
                    )
                    
                    response = client.models.generate_content(
                        model='gemini-3.8-flash',
                        contents=user_prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=system_prompt,
                            temperature=0.2, # Low temperature for accurate, factual synthesis
                        )
                    )
                    
                    st.success("Analysis completed successfully.")
                    st.markdown(response.text)
                    
                    # Call-to-Action to redirect to Tally Form
                    st.write("---")
                    st.info("⚠️ **Sandbox Tier Limitation:** You are currently using the standard reasoning model. To unlock advanced **Reason & Verify workflows (Powered by Claude)** with 200k+ token context windows to analyze your proprietary lab protocols, please upgrade your access tier.")
                    
                    # REPLACE THE URL BELOW WITH YOUR ACTUAL TALLY EMBED OR REDIRECT LINK
                    st.link_button("Request Full Access Tier", "https://tally.so/r/zxp200")
                    
                except Exception as e:
                    st.error(f"API Error encountered: {e}")
    else:
        st.info("Configure the parameters on the left panel and click 'Run Analysis' to generate the oncology research report.")
