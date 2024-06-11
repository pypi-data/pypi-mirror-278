import requests

def get_api_url(query, page, per_page):
    """
    Generate the Pexels API URL for the given query and pagination settings.
    """
    return f'https://www.pexels.com/en-us/api/v3/search/photos?page={page}&per_page={per_page}&query={query}&orientation=all&size=all&color=all&sort=popular&seo_tags=true'

def fetch_images(query, num_images):
    """
    Fetch images from Pexels API based on the query and number of images.
    """
    headers = {
        'sec-ch-ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        'content-type': 'application/json',
        'x-client-type': 'react',
        'sec-ch-ua-platform': '"Windows"',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': f'https://www.pexels.com/search/{query}/',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'en-US,en;q=0.9',
        'authorization': '',
        'secret-key': 'H2jk9uKnhRmL6WPwh89zBezWvr',
    }

    try:
        # Initialize the API
        url = get_api_url(query, 1, num_images)
        
        # Send GET requests to the API with valid headers
        response = requests.get(url, headers=headers)
        print(f"Fetching {query} images") # Interactivity 
        response.raise_for_status()
        
        # Parse JSON response
        data = response.json()
        print(f"Fetch Successful ✅") # Interactivity
             
        # Extract the image URLS and total count 
        img_urls = [img['attributes']['image']['large'] for img in data['data']]
        total_count = data['pagination']['total_results']
        
        return {
            'img_urls': img_urls,
            'total_count': total_count
        }
        
    except Exception as e:
        print(f"Error: {e}")
        raise
