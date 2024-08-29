import os
import json
import PyPDF2

def pdfs_to_json(directory, output_file):
    """Converts PDFs in a directory to a single JSON file.

    Args:
        directory: The path to the directory containing PDFs.
        output_file: The path to the output JSON file.
    """

    data = []
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(directory, filename)
            with open(pdf_path, 'rb') as pdf_file:
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                pdf_text = ""
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    pdf_text += page.extract_text()
                data.append({"filename": filename, "text": pdf_text})

    # Create the output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Example usage
current_dir = os.path.dirname(os.path.abspath(__file__))
pdf_directory = os.path.join(current_dir, "pdfs")
output_file = os.path.join(current_dir, "output", "combined.json")
pdfs_to_json(pdf_directory, output_file)
