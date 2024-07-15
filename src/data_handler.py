import pandas as pd
import PyPDF2

def load_population_data(filepath):
    """Load population data from a CSV file."""
    return pd.read_csv(filepath)

def extract_text_from_pdf(filepath):
    """Extract text from a PDF file."""
    text = ''
    with open(filepath, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            text += page.extract_text() if page.extract_text() else ''
    return text
