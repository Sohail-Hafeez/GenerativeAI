import requests

API_KEY = "AIzaSyCeZu24qMrH7VwVkj3aHmiioGRwO4cgAHw"
url = f"https://maps.googleapis.com/maps/api/staticmap?center=33.6429,72.9925&zoom=17&size=600x400&key={API_KEY}"

response = requests.get(url)
if response.status_code == 200:
    print("✅ API Key is working!")
else:
    print("❌ API Key error:", response.text)
