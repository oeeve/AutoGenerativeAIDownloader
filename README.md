
## AutoGenerativeAIDownloader
Proof of Concept - Part of UC2ST210 ST2 Team 13 Group Project: The Role of Artificial Intelligence in the Development of Digital Forensics Training Images.

This script will:
1. Reads prompt-strings from the 'Prompt' column header in main.csv, then generates the respective images using OpenAI's DALLE2 API.
2. Downloads the newly generated images to the 'generated_images' folder.
3. Writes the path and filename to the corresponding column 'GeneratedImages' in main.csv.

 
Remember to add a valid API key. Guid for setting an environment variable [here](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety)

### Script Overview
```mermaid
%%{init: {'theme': 'neutral'}}%%
sequenceDiagram
    participant Script as Python Script <br> image_downloader.py
    participant CSV as CSV File <br> main.csv
    participant ImgGen as Image Generator  <br> generate_and_save_image()
    participant FS as File System
    participant API as OpenAI API
    Participant CDN as OpenAI CDN

    
    Script->>CSV: Reads "main.csv"
    loop For each prompt in CSV
        Script->>ImgGen: Runs the Generate & Save image function
        ImgGen->>API: Requests image to be created from prompt
        API-->>ImgGen: Response with image URL
        ImgGen->>CDN: Requests image data
        CDN-->>ImgGen: Image data
        ImgGen->>FS: Writes image data to /image_folder/image_nn.png
        FS-->>ImgGen: Success message
        ImgGen-->>Script: Return image file name and file path
    end
    Script->>CSV: Writes updates to "main.csv"
```
*Sequence diagram detailing the interactions between the scripts image-generator function, local files, and OpenAI.*

### Demo: Image Generator Script
![PoC](AutoGenerativeAI.gif)

### Demo: AI Corpora Generator
[![CorporaGenAI · AI Corpora Generator](readme/vid.png)](https://vimeo.com/oeeve/corporagen-uc2st210-team13?share=copy)

