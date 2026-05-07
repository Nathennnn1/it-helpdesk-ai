import requests

ur1 = "https://wttr.in/Taipei?format=j1"
reponse = requests.get(ur1)
data = reponse.json()

temp = data["current_condition"][0]["temp_C"]
weather = data["current_condition"][0]["weatherDesc"][0]["value"]

print(f"臺北現在天氣:{weather}")
print(f"目前氣溫{temp}°C")

