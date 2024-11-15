import requests

# Replace with your actual access token
access_token = 'YOUR_ACCESS_TOKEN'

# Get the list of activities
activities_url = 'https://www.strava.com/api/v3/athlete/activities'
headers = {'Authorization': f'Bearer {access_token}'}
response = requests.get(activities_url, headers=headers)

# Print response to debug
print(response.text)