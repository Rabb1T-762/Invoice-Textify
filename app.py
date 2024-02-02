from imghdr import what
import sys
import re
import cv2
import pytesseract
import pandas as pd
from pathlib import Path

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

IMAGE_AREAS_WITH_DATA = {'invoice_number': invoice_number_area,
                         'totals': totals_area,
                         **line_item_areas}


def image_to_data(image, areas):
    # Dictionary to store the extracted text for each area
    extracted_data = {}

    # Load the image
    image_file = cv2.imread(image)

    # Iterate over each area
    for area_name, area_coords in areas.items():
        # Perform OCR on the cropped region
        text = extract_text_from_area(image_file, area_coords)

        # correct the extracted text
        corrected_data = text_to_data(text, area_name)

        extracted_data[area_name] = corrected_data
    return extracted_data


def extract_text_from_area(image, area):
    # Perform OCR on a given area
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


def format_data_output(text):
    pass


def text_to_data(text, area_name):
    # remove new line characters and change values to correct types
    # doing conversions in place and not creating a new variable
    if area_name == 'totals':
        text = split_totals(text)
        text = clean_sentence_array(text)
        # change totals to integers
        text = string_array_to_int(text)
    elif area_name.startswith('line_item'):
        text = clean_sentence(text)
    elif area_name == 'invoice_number':
        text = clean_sentence(text)
    return text


def string_array_to_int(array):
    return [int(string) for string in array]


def data_to_file(data):
    return data


def create_line_items(data, cost_array_key, line_item_key):
    # Mutate data for export
    # Add cost to each line item
    for i, total in enumerate(data[cost_array_key]):
        # create line_item for each item in cost array
        key = f"{line_item_key}_{i + 1}"
        data[key] = {"item": data[key], "cost": total}

    return data


def create_spreadsheet_dataframe(data):
    # Create a DataFrame from the extracted text
    df = pd.DataFrame.from_dict(data, orient='index')

    # Transpose the DataFrame to have the correct orientation
    new_df = pd.DataFrame(columns=['Invoice Number', 'Total'])
    for key, value in data.items():
        if key.startswith('line_item'):
            index = int(key.split('_')[-1])
            new_df[f'Line_Item_{index}'] = [value['item']]
            new_df[f'Cost_{index}'] = [value['cost']]

    # Assign the invoice number and total to the new DataFrame
    new_df['Invoice Number'] = data['invoice_number']
    new_df['Total'] = data['total']
    return new_df


def process_image(image_path):
    print(f"Processing image: {image_path}")

    extracted_text = image_to_data(image_path, IMAGE_AREAS_WITH_DATA)

    # Create line items with name and cost
    extracted_text = create_line_items(extracted_text, "totals", "line_item")

    # Calculate invoice total
    extracted_text["total"] = sum(extracted_text["totals"])

    # Remove the 'totals' key from the extracted text
    extracted_text.pop("totals")

    # Create excel dataframe
    return create_spreadsheet_dataframe(extracted_text)


def main(input_files, output_file):
    # Dataframe list
    df_list = []
    for input_file in input_files:
        if Path(input_file).is_dir():
            # Filter only image files in the directory
            image_files = [file for file in Path(
                input_file).glob('*') if what(file) is not None]
            for file in image_files:
                df = process_image(str(file))
                df_list.append(df)
        elif what(input_file) is not None:  # Check if input file is an image
            df = process_image(input_file)
            df_list.append(df)

    combined_df = pd.concat(df_list, ignore_index=True)
    combined_df.to_excel(f"{output_file}.xlsx", index=False)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python script.py <input_image1> <input_image2> ... "
              "<output_excel_file_name>\n"
              "or\n"
              "python script.py <input_directory> <output_excel_file_name>")
        sys.exit(1)

    input_files = sys.argv[1:-1]
    output_file = sys.argv[-1]

    main(input_files, output_file)
