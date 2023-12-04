import pandas as pd
import requests

def get_block_address(latitude, longitude):
    #https://geocode.maps.co/reverse?lat=40.7558017&lon=-73.9787414
    api_url = f'https://geocode.maps.co/reverse?lat={latitude}&lon={longitude}'
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        display_name = data.get('display_name', 'N/A')
        print(display_name)
        return display_name
    else:
        return 'N/A'

df=pd.read_csv('C:/Users/srava/OneDrive/Desktop/531_Project/Processed/SemiProcessed/NY.csv')


# Apply the function to create the 'BlockAddress' column
df['BlockAddress'] = df.apply(lambda row: get_block_address(row['Latitude'], row['Longitude']), axis=1)

df.to_csv("NYwithBlockAddress.csv",index=True)