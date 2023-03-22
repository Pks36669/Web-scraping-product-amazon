import requests
from bs4 import BeautifulSoup
import csv

# Set the base URL and headers
base_url = "https://www.amazon.in"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Set the search query and number of pages to scrape
search_query = "bags"
num_pages = 20

# Create an empty list to store the data
data = []

# Loop through the pages and scrape the data
for page in range(1, num_pages+1):
    # Construct the URL for the current page
    url = f"{base_url}/s?k={search_query}&page={page}"

    # Send a GET request to the page URL with headers
    response = requests.get(url, headers=headers)

    # Create a BeautifulSoup object from the response content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the product listings on the page
    listings = soup.find_all('div', {'data-component-type': 's-search-result'})

    # Loop through each listing and extract the data
    for listing in listings:
        # Extract the product URL
        product_url_elem = listing.find('a', {'class': 'a-link-normal s-no-outline'})
        product_url = f"{base_url}{product_url_elem['href']}" if product_url_elem else None

        # Extract the product name
        product_name_elem = listing.find('h2', {'class': 'a-size-mini a-spacing-none a-color-base s-line-clamp-2'})
        product_name = product_name_elem.text.strip() if product_name_elem else None

        # Extract the product price
        product_price_elem = listing.find('span', {'class': 'a-price-whole'})
        product_price = product_price_elem.text.strip() if product_price_elem else None

        # Extract the product rating
        rating_elem = listing.find('span', {'class': 'a-icon-alt'})
        rating = float(rating_elem.text.split()[0]) if rating_elem else None

        # Extract the number of reviews
        num_reviews_elem = listing.find('span', {'class': 'a-size-base', 'dir': 'auto'})
        num_reviews = int(num_reviews_elem.text.replace(',', '')) if num_reviews_elem else None
        
        # Send a GET request to the product URL to extract additional information
        product_response = requests.get(product_url, headers=headers)
        product_soup = BeautifulSoup(product_response.content, 'html.parser')
        
        # Extract the ASIN
        
        asin_elem = product_soup.find('th', string='ASIN')
        asin = asin_elem.find_next_sibling('td').text.strip() if asin_elem else None
        
        # Extract the product description
        description_elem = product_soup.find('div', {'id': 'productDescription'})
        description = description_elem.text.strip() if description_elem else None
        
       # Extract the manufacturer
        manufacturer_elem = product_soup.find('th', string='Manufacturer')
        manufacturer = manufacturer_elem.find_next_sibling('td').text.strip() if manufacturer_elem else None

        # Add the data to the list
        data.append({
            'product_url': product_url,
            'product_name': product_name,
            'product_price': product_price,
            'rating': rating,
            'num_reviews': num_reviews,
            'asin': asin,
            'description': description,
            'manufacturer': manufacturer
        })

# Write the data to a CSV file
with open('amazon_bags_data.csv', 'w', newline='') as csvfile:
    fieldnames = ['product_url', 'product_name', 'product_price', 'rating', 'num_reviews', 'asin', 'description', 'manufacturer']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for d in data:
        writer.writerow(d)

print(f"Scraped data for {len(data)} products and saved to 'amazon_bags_data.csv' file.")