import json

credentials = {}
credentials['CONSUMER_KEY'] = 'VCHdsFfrBC3T3y6wJ5irBCMhm'
credentials['CONSUMER_SECRET'] = 'nJamhCdpYNloua6OtBdQZD9TKJUBBz26Usc6c2pGQt77w8rUoo'
credentials['ACCESS_TOKEN'] = '41560471-Pg4bPfed0YktXJ1rffjMaTwWyb4sIWzGJ3LjkJHBh'
credentials['ACCESS_SECRET'] = '19Hj0wwgAUBQdV5K4Zk6490YU8Cq2ZL0QlA7jwMXavIo6'

# Save the credentials object to file
with open("twitter_credentials.json", "w") as file:
    json.dump(credentials, file)

