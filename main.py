
import pandas as pd
from transformers import pipeline
from src.data_handler import load_population_data, extract_text_from_pdf

def retrieve_information(query, data):
    """
    Retrieve information about a country from the dataframe.
    Returns a formatted string of relevant country data.
    """
    # Filter data for the requested country, case-insensitively.
    relevant_info = data[data['Country'].str.contains(query, case=False, na=False)]
    if not relevant_info.empty:
        # Assuming the first match is the most relevant one.
        info = relevant_info.iloc[0]
        details = (f"Country: {info['Country']}, Population 2023: {info['Population2023']}, "
                   f"Yearly Change: {info['YearlyChange']}, Net Change: {info['NetChange']}, "
                   f"Density (P/Km²): {info['Density(P/Km²)']}, "
                   f"Land Area (Km²): {info['Land Area(Km²)']}, Migrants (net): {info['Migrants(net)']}, "
                   f"Fertility Rate: {info['Fert.Rate']}, Median Age: {info['MedianAge']}, "
                   f"Urban Pop %: {info['UrbanPop%']}, World Share: {info['WorldShare']}")
        return details
    return "No detailed data available."

def generate_response(context):
    """
    Generate a response using the GPT-2 model with given context.
    """
    generator = pipeline('text-generation', model='gpt2')
    response = generator(context, max_length=100, truncation=True)
    return response[0]['generated_text']

def main():
    # Load data
    population_data = load_population_data('data/population.csv')

    # User query
    query = input("Please enter your query (e.g., a country name): ")

    # Retrieval step
    retrieved_context = retrieve_information(query, population_data)

    # Generate response using the retrieved context
    response = generate_response(retrieved_context)
    print("AI Response:", response)

if __name__ == "__main__":
    main()
from transformers import pipeline

def generate_response(prompt):
    generator = pipeline('text-generation', model='gpt2')
    response = generator(prompt, max_length=100, num_return_sequences=1)
    return response[0]['generated_text']
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