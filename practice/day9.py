import requests

API_Key = "AIzaSyBYCufpNBks8vV-gFmVGxUpqiJVRXMhF4A"
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_Key}"

data={
     
     "contents":[{
         "parts":[{"text":"你好，請用繁體中文介紹一下你自己"}]

     }]
}


reponse = requests.post(url, json=data)
result = reponse.json()
print(result)

'''
["candidates"][0]["content"]["parts"][0]["text"]
'''

