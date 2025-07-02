import os
from PIL import Image

# Make sure folder exists
os.makedirs('static/test_images', exist_ok=True)

# Create white dummy image
img = Image.new('RGB', (100, 100), color='white')
img.save('static/test_images/clean_sample.jpeg')

print("✅ Dummy test image created at: static/test_images/clean_sample.jpeg")

