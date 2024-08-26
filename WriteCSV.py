import csv

# Sample table data (list of lists)
table_data = [
    ['Name', 'Age', 'City'],
    ['Alice', '25', 'New York'],
    ['Bob', '30', 'San Francisco'],
    ['Charlie', '35', 'London']
]

# Specify the output file name
output_file = 'output.csv'

# Write the data to the CSV file
with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(table_data)

print(f"CSV file '{output_file}' has been created successfully.")