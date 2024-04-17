import requests
from bs4 import BeautifulSoup
import json

# URL of the page you want to scrape
url = 'https://yousee.dk/hjaelp/butik'

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find all div elements with class "MuiBox-root" and append them to a list
    div_elements = soup.find_all('div', class_='MuiBox-root css-j7qwjs')
    # Extract text or other attributes from the div elements if needed
    div_texts = [div.get_text() for div in div_elements]
    # Print the text content of the div elements
    for text in div_texts:
        print(text)
else:
    print('Failed to fetch the page:', response.status_code)

# Fetch the webpage content
response = requests.get(url)

# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Find all <a> tags with class 'MuiTypography-root' and 'MuiLink-root'
links = soup.find_all('a', class_="MuiTypography-root MuiTypography-inherit MuiLink-root MuiLink-underlineAlways css-1c0gb7g")

# Extract the href attribute from each <a> tag and append to a list
link_list = [link.get('href') for link in links]

# Initialize an empty list to store results
results = []

# Loop over each URL
for url_suffix in link_list:
    # Construct the full URL
    url = f'https://yousee.dk/hjaelp/{url_suffix}'
    # Fetch the webpage content
    response = requests.get(url)
    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')
    # Initialize variables to store the extracted data
    opening_hours = []
    store_info = {}

    # Find the div with class 'MuiBox-root css-h5fkc8' for opening hours
    main_div_opening_hours = soup.find('div', class_="MuiBox-root css-h5fkc8")

    # Extract opening hours
    for span in main_div_opening_hours.find_all('span'):
        # Check if the span contains date information
        if '/' in span.get_text():
            day_date = span.get_text().strip().split()
            day = day_date[0]
            date = day_date[1]
            opening_time = span.find_next('span').get_text().strip()
            opening_hours.append({
                "Dag": day,
                "Dato": date,
                "Tidspunkt": opening_time
            })

    # Find the div with class 'MuiBox-root css-1v9q1ma' for store information
    main_div_store_info = soup.find('div', class_="MuiBox-root css-1v9q1ma")

    # Extract store information
    address_element = main_div_store_info.find('p', itemprop='streetAddress')
    if address_element:
        store_info["Adresse"] = address_element.get_text().strip()
    else:
        store_info["Adresse"] = ""

    for p in main_div_store_info.find_all('p'):
        text = p.get_text().strip()
        # Extract zip code
        if p.find('span', itemprop='postalCode'):
            store_info["Postnummer"] = p.find('span', itemprop='postalCode').get_text().strip()
        # Extract phone number
        elif "Tlf:" in text:
            store_info["Telefon"] = text.split("Tlf:")[1].strip()
        # Extract email
        elif "@" in text:
            store_info["Email"] = text

    # Extract city
    city_element = main_div_store_info.find('span', itemprop='addressLocality')
    if city_element:
        city = city_element.get_text().strip()
    else:
        city = ""

    # Combine the extracted data
    result = {
        city: {
            "Åbningstider": opening_hours,
            "Butiks_Information": store_info
        }
    }

    # Append result to the results list
    results.append(result)

# Convert the data to JSON format
results_json = json.dumps(results, ensure_ascii=False)


json_array = json.loads(results_json)


# Generate output in a text file
with open('opening_hours.ctxt', 'w', encoding='utf-8') as file:
    # Iterate over the JSON array
    file.write("##\n\n")
    for index, element in enumerate(json_array):
        file.write(f"## ")  # Write element number
        file.write(json.dumps(element, indent=4, ensure_ascii=False))  # Write JSON element
        file.write("\n\n")  # Add newline between elements
