# Automatic Generation of pptx from names
This repo contains a simple script to scrape images from google images using selenium and also tries to get a short description from the website links associated with the name.

## Requirements
- python
- Chrome
To get all the depencies run,
```bash 
pip install -r requirements.txt
```
## How to use
Modify the file called `names.txt` with the names you want to scrape.
Each name should appear on a seperate line. The name is essentially the query to google images. It can also have addition context like who the person is.
You also need to set your gemini api key in the `generate_pptx.py` file.

Then run the script,
```bash
python main.py
```
This would fetch the results in a folder called `selenium_search_results`.

Each folder in `selenium_search_results` will have a slide in the presentation.

The presentation (in ".pptx" format) would be saved as `output_presentation.pptx`.

Example Slide  
![Example](example.png)
## How it works 
`main.py` fetches the first 3 images from google images and saves them in a subfolder named after the query. Further, the data from the website is saved in a file called `data_{int}.html`
`generate_pptx.py` generates the presentation from the images in the `selenium_search_results` folder, and a short description is generated from the `data_{int}.html` using the `summarize_text` function, which in turn uses Gemini API. If insufficient information is available to generate a short description, then the text `<FILL-UP>` is returned.  

