import streamlit as st
from document_processor import extract_text_from_pdf, analyze_document_text
from image_analyzer import analyze_property_images
from risk_engine import evaluate_risk
import os

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="AI Property Risk Assessor",
    page_icon="🤖",
    layout="wide"
)

# --- File Size Limits ---
MAX_PDF_SIZE = 10 * 1024 * 1024  # 10MB
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_IMAGES = 5  # Max number of images

# --- App Header ---
st.title("🤖 AI-Powered Property Risk Assessor")
st.write("""
    Upload a property appraisal document (PDF) and up to 5 images (PNG, JPG, JPEG) to assess potential risks and compliance issues.
""")

# --- Main Application ---
col1, col2 = st.columns(2)

with col1:
    st.header("1. Upload Property Document")
    uploaded_pdf = st.file_uploader("Choose a PDF file", type="pdf")

with col2:
    st.header("2. Upload Property Images")
    uploaded_images = st.file_uploader("Choose image files", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

# --- Processing and Displaying Results ---
if st.button("Assess Property Risk", type="primary"):
    if uploaded_pdf is None or not uploaded_images:
        st.error("Please upload both a PDF document and at least one image.")
    else:
        try:
            # Validate file sizes
            if uploaded_pdf.size > MAX_PDF_SIZE:
                st.error(f"PDF file exceeds {MAX_PDF_SIZE // (1024 * 1024)}MB limit.")
            elif len(uploaded_images) > MAX_IMAGES:
                st.error(f"Please upload no more than {MAX_IMAGES} images.")
            elif any(img.size > MAX_IMAGE_SIZE for img in uploaded_images):
                st.error(f"One or more images exceed {MAX_IMAGE_SIZE // (1024 * 1024)}MB limit.")
            else:
                # Progress bar for better UX
                progress_bar = st.progress(0)
                status_text = st.empty()

                # Step 1 & 2: Process Document
                status_text.text("Extracting and analyzing document...")
                progress_bar.progress(25)
                doc_text = extract_text_from_pdf(uploaded_pdf)
                doc_analysis = analyze_document_text(doc_text)

                # Step 3: Process Images
                status_text.text("Analyzing images...")
                progress_bar.progress(50)
                image_analysis = analyze_property_images(uploaded_images)

                # Step 4, 5, 6: Evaluate Risk
                status_text.text("Evaluating risks...")
                progress_bar.progress(75)
                final_assessment = evaluate_risk(doc_analysis, image_analysis)

                status_text.text("Finalizing results...")
                progress_bar.progress(100)
                st.success("Analysis Complete!")
                st.divider()

                # Display the final verdict
                st.header("Final Assessment Result")
                
                risk_level = final_assessment['risk_level']
                if risk_level == "High":
                    st.error(f"**Risk Level: {risk_level}**")
                elif risk_level == "Medium":
                    st.warning(f"**Risk Level: {risk_level}**")
                else:
                    st.success(f"**Risk Level: {risk_level}**")

                st.metric(label="**Risk Score (out of 100)**", value=final_assessment['risk_score'])
                
                # Display detailed results in tabs
                tab1, tab2, tab3 = st.tabs(["💡 Reasoning", "📋 Compliance Report", "📊 Raw Data"])

                with tab1:
                    st.subheader("Factors Influencing Risk Score:")
                    for reason in final_assessment['reasoning']:
                        st.markdown(f"- {reason}")
                
                with tab2:
                    st.subheader("Compliance Checklist:")
                    for issue in final_assessment['compliance_report']:
                        st.markdown(f"- {issue}")

                with tab3:
                    st.subheader("Extracted Document Keywords")
                    st.json({"keywords": doc_analysis['risk_keywords'], "entities": doc_analysis['entities']})
                    st.subheader("Detected Image Tags")
                    st.json(image_analysis)

        except Exception as e:
            st.error(f"An error occurred during analysis: {str(e)}")
            st.info("Please ensure the uploaded files are valid and try again.")