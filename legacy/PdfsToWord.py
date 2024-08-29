from spire.pdf.common import *
from spire.pdf import *


current_dir = os.path.dirname(os.path.abspath(__file__))
pdf_file = os.path.join(current_dir, "pdfs","64.pdf")
output_file = os.path.join(current_dir, "output", "output.doc",)

# Create a PdfDocument object
pdf = PdfDocument()
# Load a PDF file from the specified path
pdf.LoadFromFile(pdf_file)
# Save the PDF in DOC format
pdf.SaveToFile(output_file, FileFormat.DOC)
# Close the PdfDocument object
pdf.Close()