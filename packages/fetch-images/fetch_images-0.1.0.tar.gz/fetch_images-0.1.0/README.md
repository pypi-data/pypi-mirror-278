# Fetch Images
A simple Python package to fetch images from Pexels API based on a search query.

## Installation
You can install `fetch_images` via pip:
```sh
pip install fetch_images
```

### For Jupyter Notebooks
If you're using Jupyter notebooks, you can install `fetch_images` using the following command in a notebook cell:
```python
!pip install fetch_images
```

## Usage
```python
from fetch_images.fetch_images import fetch_images

# Specify the search query and the number of images to fetch
query = "cat"
num_images = 10

# Fetch images from Pexels API
result = fetch_images(query, num_images)

# Retrieve image URLs and total count
img_urls = result['img_urls']
total_count = result['total_count']

# Print the fetched image URLs and total count
print('Image URLs:', img_urls)
print('Total image count:', total_count)
```

## Contributing
Contributions are welcome! Please feel free to open an issue or submit a pull request for any improvements or additional features.
