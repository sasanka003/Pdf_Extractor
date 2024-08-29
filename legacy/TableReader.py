import camelot
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
pdf_file = os.path.join(current_dir, "pdfs", "64.pdf")
output_csv = os.path.join(current_dir, "output", "output.xlsx")

# Read the PDF file
tables = camelot.read_pdf(pdf_file, pages='all', flavor='stream')

# Print the number of tables extracted
print(f"Total tables extracted: {len(tables)}")

# Iterate through all tables
for i, table in enumerate(tables):
    print(f"\nTable {i+1}:")
    
    # Print the table as a pandas DataFrame
    print(table.df)
    
    # Optionally, save the table to a CSV file
    table.to_csv(f'table_{i+1}.csv')


