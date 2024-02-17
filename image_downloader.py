# ST2 - G13. Part of PoC for "The Role of Artificial Intelligence in the development of Digital Forensics Training Images"
# This script:
# 1. Reads prompt-strings from the 'Prompt' column header in main.csv, then generates the respective images using DALLE2 API.
# 2. Downloads the newly generated images to the 'generated_images' folder.
# 3. Writes the path and filename to the corresponding column 'GeneratedImages' in main.csv.
    
import pandas as pd
import os   
import requests
import openai

# Load API key. (Add your OpenAI API key direclty, as a file path or as an environment variable).
OPENAI_API_KEY = openai.api_key_path = 'ADD_KEY_HERE'
BASE_URL = 'https://api.openai.com/v1/images/generations'  # Note, there is a newer endpoint, but this is the one I got working now.

# Reads the CSV and loads it into a DataFrame. (Edit the filepaht as needed).
df = pd.read_csv('main.csv')

# Checks for and creates a folder for the generated images. (Specify folder path as needed).
image_folder = 'generated_images'
os.makedirs(image_folder, exist_ok=True)

# Authenticates the API key.
headers = {
    'Authorization': f'Bearer {OPENAI_API_KEY}',
    'Content-Type': 'application/json',
}

# Generates the image using DALLE2 API, checks response and tries to download it. (Note: edit n for the numbers of files generated, and size for the aspect ratio).
def generate_and_save_image(prompt, index):
    response = openai.Image.create(
        model="dall-e-2",
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    if 'data' in response and len(response['data']) > 0:
        image_url = response['data'][0]['url']
        try:
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                generated_image_filename = f"image_{index}.png" # Note: Edit this to chagne file name.
                with open(os.path.join(image_folder, generated_image_filename), 'wb') as image_file:
                    image_file.write(image_response.content)
                print(f"Image successfully saved to {os.path.join(image_folder, generated_image_filename)}")
                return generated_image_filename
            else:
                print(f"Failed to download image from {image_url}")
        except Exception as download_error:
            print(f"An error occurred while downloading the image: {download_error}")
    else:
        print("Failed to generate image due to unexpected API response format.")

# Check for and crate the 'GeneratedImages' column in CSV if missing.
if 'GeneratedImages' not in df.columns:
    df['GeneratedImages'] = None

# Checks each line in 'GeneratedImages' and if empty, runs the image geneation function (generate_and_save_image) with the corresponding prompt.
for index, row in df.iterrows():
    if pd.isna(row['GeneratedImages']):
        prompt = row['Prompt']
        generated_image_filename = generate_and_save_image(prompt, index)
        df.at[index, 'GeneratedImages'] = os.path.join(image_folder, generated_image_filename)

# Writes the updated DataFrame to the CSV. 
df.to_csv('main.csv', index=False, columns=['Prompt','GeneratedImages'])

print("All done. CSV file has been updated with image paths.")