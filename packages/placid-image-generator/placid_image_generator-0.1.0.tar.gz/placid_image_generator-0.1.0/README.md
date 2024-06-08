# Placid Image Generator

A simple Python package to generate images using the Placid API.

## Installation

```bash
pip install .
```

## Usage
```
from placid_image_generator.generator import PlacidImageGenerator

api_key = "your_api_key"
template_uuid = "your_template_uuid"
img_url = "your_image_url"
headline_text = "your_headline_text"
filename = "your_output_filename"

generator = PlacidImageGenerator(api_key, template_uuid)
image_url = generator.generate_image(img_url, headline_text, filename)
print("Generated Image URL:", image_url)

```