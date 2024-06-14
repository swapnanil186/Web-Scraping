import requests
from bs4 import BeautifulSoup
import csv
import re

# List of event URLs
event_urls = [
    'https://www.salesforce.com/dreamforce/',
    'https://www.saastrannual.com/',
    'https://websummit.com/',
    'https://www.b2bmarketingexpo.co.uk/',
    'https://www.ces.tech/'
]

# Function to scrape event data with improved error handling
def scrape_event_data(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')

    # Initialize variables with default values
    event_name = 'N/A'
    event_date = 'N/A'
    location = 'N/A'
    description = 'N/A'
    key_speakers = []
    agenda = []
    registration_details = 'N/A'
    pricing = 'N/A'
    categories = []
    audience_type = 'N/A'

    # Extract data with improved error handling
    try:
        title_tag = soup.find('title')
        if title_tag:
            event_name = title_tag.text.strip()
    except AttributeError as e:
        print(f"Error extracting event name: {e}")

    try:
        date_meta = soup.find('meta', {'name': 'date'})
        if date_meta:
            event_date = date_meta['content'].strip()
    except (AttributeError, KeyError) as e:
        print(f"Error extracting event date: {e}")

    try:
        location_meta = soup.find('meta', {'name': 'location'})
        if location_meta:
            location = location_meta['content'].strip()
    except (AttributeError, KeyError) as e:
        print(f"Error extracting location: {e}")

    try:
        description_meta = soup.find('meta', {'name': 'description'})
        if description_meta:
            description = description_meta['content'].strip()
    except (AttributeError, KeyError) as e:
        print(f"Error extracting description: {e}")

    try:
        key_speakers = [speaker.get_text(strip=True) for speaker in soup.select('.speaker-name')]
    except Exception as e:
        print(f"Error extracting key speakers: {e}")

    try:
        agenda = [item.get_text(strip=True) for item in soup.select('.agenda-item')]
    except Exception as e:
        print(f"Error extracting agenda: {e}")

    try:
        registration_link = soup.find('a', class_='registration-link')
        if registration_link:
            registration_details = registration_link['href'].strip()
    except (AttributeError, KeyError) as e:
        print(f"Error extracting registration details: {e}")

    try:
        pricing_div = soup.find('div', class_='pricing')
        if pricing_div:
            pricing = pricing_div.get_text(strip=True)
    except AttributeError as e:
        print(f"Error extracting pricing: {e}")

    try:
        categories = [category.get_text(strip=True) for category in soup.select('.category')]
    except Exception as e:
        print(f"Error extracting categories: {e}")

    try:
        audience_meta = soup.find('meta', {'name': 'audience'})
        if audience_meta:
            audience_type = audience_meta['content'].strip()
    except (AttributeError, KeyError) as e:
        print(f"Error extracting audience type: {e}")

    # Returning the data as a dictionary
    return {
        'Event Name': event_name,
        'Event Date(s)': event_date,
        'Location': location,
        'Website URL': url,
        'Description': description,
        'Key Speakers': ', '.join(key_speakers),
        'Agenda/Schedule': ', '.join(agenda),
        'Registration Details': registration_details,
        'Pricing': pricing,
        'Categories': ', '.join(categories),
        'Audience Type': audience_type
    }

# Scrape data for all events
events_data = []
for url in event_urls:
    event_data = scrape_event_data(url)
    if event_data:
        events_data.append(event_data)
    else:
        print(f"Skipping event due to missing data: {url}")

# Write data to CSV
csv_file = 'b2b_events.csv'
try:
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Event Name', 'Event Date(s)', 'Location', 'Website URL', 'Description', 'Key Speakers', 'Agenda/Schedule', 'Registration Details', 'Pricing', 'Categories', 'Audience Type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for event in events_data:
            writer.writerow(event)
    print(f"Data scraped and saved to {csv_file}")
except IOError:
    print(f"Error writing to {csv_file}")
