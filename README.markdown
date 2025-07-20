# AI Property Risk Assessor

A Streamlit-based web application that leverages AI to assess property risks by analyzing uploaded appraisal documents (PDF) and property images. The app extracts text from PDFs, identifies risk-related keywords and entities, detects objects in images using YOLOv8, and evaluates risks based on a rule-based scoring system defined in a configurable JSON file.

## Features
- **Document Analysis**: Extracts text from PDF files and identifies risk-related keywords (e.g., "fire", "leak") and entities (locations, dates) using spaCy and LangChain.
- **Image Analysis**: Detects objects in images using a cached YOLOv8 model, flagging potential risks (e.g., fire hazards, moisture sources) defined in `config.json`.
- **Risk Assessment**: Combines document and image analysis to compute a risk score and classify risk levels (Low, Medium, High).
- **Compliance Check**: Flags compliance issues based on configurable rules in `config.json` (e.g., asbestos or fire hazard mentions).
- **Interactive UI**: Built with Streamlit, featuring a progress bar, detailed status messages, and tabs for reasoning, compliance, and raw data.
- **Robustness**: Includes error handling, file size validation (10MB for PDFs, 5MB per image, max 5 images), and model caching for performance.
- **Modularity**: Risk objects and compliance rules are defined in `config.json` for easy customization.

## Prerequisites
- Python 3.8+
- Streamlit
- pdfplumber
- spaCy
- ultralytics (YOLOv8)
- PIL (Pillow)
- langchain
- numpy
- A pre-trained YOLOv8 model (`yolov8n.pt` recommended for lightweight performance)

## Installation
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ai-property-risk-assessor
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Download the spaCy model:
   ```bash
   python -m spacy download en_core_web_sm
   ```
5. Download a pre-trained YOLOv8 model (e.g., `yolov8n.pt`) and place it in the project directory.
6. Ensure `config.json` is present in the project root with the appropriate risk objects and compliance rules.

## Usage
1. Run the Streamlit app:
   ```bash
   streamlit run streamlit_app.py
   ```
2. Open your browser and navigate to `http://localhost:8501`.
3. Upload a property appraisal PDF (max 10MB) and up to 5 images (PNG, JPG, JPEG; max 5MB each).
4. Click the "Assess Property Risk" button to view the analysis results, including:
   - Risk score and level (Low, Medium, High)
   - Reasoning behind the score
   - Compliance report
   - Raw extracted data (keywords, entities, and image tags)
5. Use the `samples/` directory for example PDF and image files to test the app.

## Project Structure
- `streamlit_app.py`: Main application with Streamlit UI, file upload handling, and analysis orchestration.
- `document_processor.py`: Handles PDF text extraction and analysis using spaCy and LangChain, with model caching.
- `image_analyzer.py`: Performs object detection on images using a cached YOLOv8 model.
- `risk_engine.py`: Evaluates risks based on document and image analysis, using rules from `config.json`.
- `config.json`: Configuration file for risk objects and compliance checks.
- `requirements.txt`: Lists all Python dependencies.
- `samples/`: Directory for sample PDF and image files (e.g., `property.jpg`).

## Example
1. Upload a PDF appraisal document mentioning terms like "leak" or "asbestos".
2. Upload images of the property (e.g., showing a potted plant near electronics).
3. The app will analyze the inputs and provide a risk score, such as "Medium" with a score of 65, along with reasoning like "Detected potential risk objects in images: potted plant" and compliance issues like "Presence of asbestos is a major compliance red flag."

## Configuration
Modify `config.json` to customize:
- `potential_risk_objects`: List of objects considered risky (e.g., "fire hydrant", "potted plant").
- `compliance_checklist`: Dictionary of keywords and associated compliance issues (e.g., "asbestos_mentioned": "Presence of asbestos is a major compliance red flag.").

## Limitations
- The risk scoring system is rule-based and may require customization for specific use cases via `config.json`.
- Image analysis relies on YOLOv8's pre-trained model, which may not detect all property-specific risks.
- Large files may slow down processing; file size limits are enforced to mitigate this.
- No support for malicious file scanning; additional security measures may be needed for production.

## Future Improvements
- Add unit tests using `pytest` for each module.
- Implement a custom-trained YOLO model for property-specific object detection.
- Add support for advanced NLP models for deeper document analysis.
- Enhance security with malicious file scanning.
- Include a configuration UI in Streamlit for modifying `config.json` without editing the file.

## License
This project is licensed under the MIT License.