import re

input_string = "The important text is between <start> and <end> tags."

# Search for the text between '<start>' and '<end>'
match = re.search(r'<start>(.*?)<end>', input_string)

if match:
    extracted_text = match.group(1)
    print("Extracted text:", extracted_text)
else:
    print("No match found.")
