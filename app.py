import re
import cv2
import pytesseract
import pandas as pd

# Load the image
image_file = cv2.imread("images/1.png")

# Define the areas of interest and their coordinates
invoice_number_area = (996, 576, 192, 57)
totals_area = (1002, 1068, 324, 396)
line_item_areas = {
    'line_item_1': (135, 1060, 594, 75),
    'line_item_2': (135, 1124, 594, 75),
    'line_item_3': (135, 1188, 594, 75),
    'line_item_4': (135, 1251, 594, 75),
    'line_item_5': (135, 1315, 594, 75),
    'line_item_6': (135, 1378, 594, 75)}

areas = {'invoice_number': invoice_number_area,
         'totals': totals_area}

areas.update(line_item_areas)


# Perform OCR on a given area
def extract_text_from_area(image, area):
    x, y, w, h = area
    cropped_image = image[y:y+h, x:x+w]
    text = pytesseract.image_to_string(cropped_image)
    return text


def split_totals(text):
    # Split text by new line
    lines = re.split('\n(?=[0-9])', text)
    return lines


def clean_sentence_array(lines):
    # Remove newline characters while preserving spaces between words
    cleaned_lines = []
    for sentence in lines:
        cleaned_lines.append(clean_sentence(sentence))
    return cleaned_lines


def clean_sentence(line):
    # Remove all new line characters
    return line.replace('\n', ' ').strip()


def format_text_output(text):
    pass


def clean_extracted_text(text):
    if text.area_name == 'totals':
        text = split_totals(text)
        text = clean_sentence_array(text)
    if text.area_name.startswith('line_item'):
        text = clean_sentence(text)
    if area_name == 'invoice_number':
        text = clean_sentence(text)


def string_array_to_int(array):
    return [int(string) for string in array]


# Dictionary to store the extracted text for each area
extracted_text = {}

# Iterate over each area
for area_name, area_coords in areas.items():
    # Perform OCR on the cropped region
    text = extract_text_from_area(image_file, area_coords)

    # Clean the extracted text
    if area_name == 'totals':
        text = split_totals(text)
        text = clean_sentence_array(text)
        text = string_array_to_int(text)
    if area_name.startswith('line_item'):
        text = clean_sentence(text)
    if area_name == 'invoice_number':
        text = clean_sentence(text)

    extracted_text[area_name] = text

# Mutate data for export
# Add cost to each line item
for i, total in enumerate(extracted_text["totals"]):
    key = f"line_item_{i + 1}"
    extracted_text[key] = {"item": extracted_text[key], "cost": total}


# Calculate invoice total
extracted_text["total"] = sum(extracted_text["totals"])


# export as excel sheet
# Remove the 'totals' key from the extracted text
extracted_text.pop("totals")

# Create a DataFrame from the extracted text
df = pd.DataFrame.from_dict(extracted_text, orient='index')

# Transpose the DataFrame to have the correct orientation
new_df = pd.DataFrame(columns=['Invoice Number', 'Total'])
for key, value in extracted_text.items():
    if key.startswith('line_item'):
        index = int(key.split('_')[-1])
        new_df[f'Line_Item_{index}'] = [value['item']]
        new_df[f'Cost_{index}'] = [value['cost']]

# Assign the invoice number and total to the new DataFrame
new_df['Invoice Number'] = extracted_text['invoice_number']
new_df['Total'] = extracted_text['total']

# Save the DataFrame to an Excel file
new_df.to_excel("invoice_data.xlsx", index=False)
