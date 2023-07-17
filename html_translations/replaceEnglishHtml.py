import os
import glob
import pandas as pd
from bs4 import BeautifulSoup
import sys
from tqdm import tqdm

sys.path.append('..')
from pyFuncs import browseForFile, browseForDir

def translate_html_from_excel(excel_path, html_dir, output_path):
    # Reading the excel file using pandas
    workbook = pd.ExcelFile(excel_path)

    # Create a dictionary to hold unused translations
    unused_translations = {}

    # Loop through each sheet in the workbook
    for sheet in workbook.sheet_names:
        # Read the data in the sheet into a pandas DataFrame
        # Specify header=None since the excel file does not have headers
        df = pd.read_excel(excel_path, sheet_name=sheet, header=None)

        # Only keep the first two columns (assumed to be English and Spanish)
        df = df.iloc[:, :2]

        # Rename the columns so that we can reference them later
        df.columns = ['English', 'Spanish']

        # Set the unused translations for this sheet to all the translations initially
        unused_translations[sheet] = set(df['English'].values)

        # Construct the corresponding html file name
        html_file_path = os.path.join(html_dir, sheet + '.html')

        # If this HTML file exists
        if os.path.exists(html_file_path):
            # Parse the HTML file with BeautifulSoup
            with open(html_file_path, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file.read(), "html.parser")

            # Loop through each English-Spanish pair in the DataFrame
            for index, row in df.iterrows():
                english = row['English']
                spanish = row['Spanish']

                # Find all instances of the English phrase in the HTML
                body = soup.find(text=lambda text: text and english in text)
                if body:
                    # If found, replace with the Spanish phrase
                    body.replace_with(body.replace(english, spanish))
                    # Remove the translation from unused translations
                    unused_translations[sheet].remove(english)

            # Construct the translated html file name
            translated_html_file_path = os.path.join(html_dir, 'spanish_' + sheet + '.html')

            # Write the modified HTML back to the file
            with open(translated_html_file_path, 'w', encoding='utf-8') as file:
                file.write(str(soup))

    # Write the unused translations to the output file
    with open(output_path, 'w', encoding='utf-8') as file:
        for sheet, translations in unused_translations.items():
            for translation in translations:
                file.write(f'{sheet}: {translation}\n')

# Call the function
translate_html_from_excel(browseForFile(), browseForDir(), 'unused_translations.txt')
