import pdfplumber
import spacy
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Singleton for caching spaCy model
class SpacyModel:
    _instance = None
    _nlp = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SpacyModel, cls).__new__(cls)
            try:
                cls._nlp = spacy.load("en_core_web_sm")
            except Exception as e:
                raise RuntimeError(f"Failed to load spaCy model: {str(e)}")
        return cls._instance

    @property
    def nlp(self):
        return self._nlp

def extract_text_from_pdf(pdf_file):
    """
    Extracts all text from an uploaded PDF file.

    Args:
        pdf_file: Streamlit uploaded file object (PDF).

    Returns:
        str: Extracted text.

    Raises:
        RuntimeError: If PDF cannot be opened or text extraction fails.
    """
    try:
        text = ""
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        if not text.strip():
            raise ValueError("No text could be extracted from the PDF.")
        return text
    except Exception as e:
        raise RuntimeError(f"Failed to process PDF: {str(e)}")

def analyze_document_text(text):
    """
    Analyzes extracted text by splitting it into intelligent chunks and processing with spaCy.

    Args:
        text (str): Extracted text from the PDF.

    Returns:
        dict: Analysis results with entities and risk keywords.

    Raises:
        ValueError: If text is empty or invalid.
    """
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Input text must be a non-empty string.")

    # Use LangChain's RecursiveCharacterTextSplitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    text_chunks = text_splitter.split_text(text)

    # Initialize variables to hold combined results
    all_entities = {"locations": [], "dates": []}
    all_risk_keywords = []
    nlp = SpacyModel().nlp

    # Process the document chunk by chunk
    for chunk in text_chunks:
        try:
            doc = nlp(chunk)
            
            # Extract Named Entities from the chunk
            for ent in doc.ents:
                if ent.label_ == "GPE" or ent.label_ == "LOC":
                    all_entities["locations"].append(ent.text)
                elif ent.label_ == "DATE":
                    all_entities["dates"].append(ent.text)

            # Find risk-related keywords in the chunk
            keywords_in_chunk = re.findall(r'\b(damage|leak|crack|mold|fire|hazard|asbestos)\b', chunk, re.IGNORECASE)
            all_risk_keywords.extend(keywords_in_chunk)
        except Exception as e:
            raise RuntimeError(f"Failed to process text chunk: {str(e)}")

    # Combine and deduplicate results
    analysis_result = {
        "entities": {
            "locations": list(set(all_entities["locations"])),
            "dates": list(set(all_entities["dates"]))
        },
        "risk_keywords": list(set(all_risk_keywords))
    }
    
    return analysis_result