import requests
from bs4 import BeautifulSoup
import random

def fetch_vehicle_models(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the table containing the vehicle models
        table = soup.find('div', {'class': 'docContent'}).find('table')
        
        if not table:
            print("Table not found on the page.")
            return []

        # Extract vehicle model names from the table
        vehicle_models = []
        for row in table.find_all('tr')[1:]:  # Skip the header row
            cells = row.find_all('td')
            if len(cells) > 0:
                model_name = cells[0].get_text(strip=True).lower()
                vehicle_models.append(model_name)
        
        return vehicle_models
    except requests.RequestException as e:
        print(f"Error fetching vehicle models: {e}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def generate_display_name(model_name):
    # Create a display name by capitalizing each word and replacing underscores with spaces
    words = model_name.replace('_', ' ').title()
    return words

def generate_price(model_name):
    # Generate a random price within a specified range
    min_price = 20000  # Minimum price
    max_price = 1000000  # Maximum price
    return random.randint(min_price, max_price)

def format_vehicle_models(vehicle_models):
    formatted_models = []
    for model in vehicle_models:
        display_name = generate_display_name(model)
        price = generate_price(model)
        formatted_models.append(f'["{model}"] = {{"{display_name}", {price}, ""}},')
    return formatted_models

def main():
    url = 'https://docs.fivem.net/docs/game-references/vehicle-models/'
    
    vehicle_models = fetch_vehicle_models(url)
    
    if vehicle_models:
        formatted_models = format_vehicle_models(vehicle_models)
        print("Formatted Vehicle Models:")
        for model in formatted_models:
            print(model)
    else:
        print("No vehicle models found or error fetching the list.")

if __name__ == "__main__":
    main()
