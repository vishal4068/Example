import fitz  # PyMuPDF
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
import re

# Open the PDF file
pdf_file = "sample.pdf"
doc = fitz.open(pdf_file)

# Function to extract text from a page
def extract_text(page):
    text = page.get_text()
    return text.strip()

# Function to extract hyperlink text associated with a given URL
def extract_hyperlink_text(page_text, hyperlink_url):
    pattern = r'<a[^>]*href=[\'\"]' + re.escape(hyperlink_url) + r'[\'\"][^>]*>(.*?)</a>'
    match = re.search(pattern, page_text)

    if match:
        hyperlink_text = match.group(1)
        return hyperlink_text.strip()
    else:
        return ""

# Create a new Excel workbook
workbook = Workbook()
worksheet = workbook.active

# Add headers
worksheet.append(['Hyperlink Text', 'Hyperlink URL', 'Page Number'])

# Set header row formatting
for cell in worksheet[1]:
    cell.font = Font(bold=True)
    cell.alignment = Alignment(horizontal='center')

# Iterate through each page of the PDF
for page_number in range(len(doc)):
    page = doc.load_page(page_number)
    
    # Extract text from the page
    page_text = extract_text(page)
    
    # Extract hyperlinks from the page
    hyperlinks = page.get_links()
    
    # Iterate through hyperlinks on the page
    for hyperlink in hyperlinks:
        hyperlink_url = hyperlink["uri"]  # Extract hyperlink URL
        
        # Extract hyperlink text based on URL
        hyperlink_text = extract_hyperlink_text(page_text, hyperlink_url)
        
        # Append hyperlink with page number to worksheet
        worksheet.append([hyperlink_text, hyperlink_url, page_number + 1])  # Adding 1 to start page numbering from 1

# Save the Excel file
workbook.save('hyperlinks_with_page_numbers.xlsx')

# Close the PDF document
doc.close()
