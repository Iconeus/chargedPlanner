import requests

# API Base URL
BASE_URL = "https://iconeus.ilucca.net/api/v3"

# API Key or Access Token
HEADERS = {
    "Authorization": "Bearer YOUR_ACCESS_TOKEN",
    "Accept": "application/json"
}

# Function to get collaborator absences
def get_collaborator_holidays(collaborator_id):
    url = f"{BASE_URL}/collaborators/{collaborator_id}/absences"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()  # Returns the absences as JSON
    else:
        print(f"Failed to fetch holidays: {response.status_code}")
        print(response.text)
        return None

# Example Usage
collaborator_id = "12345"  # Replace with the actual collaborator ID
holidays = get_collaborator_holidays(collaborator_id)
if holidays:
    print("Holidays:", holidays)
