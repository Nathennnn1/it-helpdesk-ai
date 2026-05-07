'''
person = {

   "name" : "Nathen",
   "age" : 28,
   "job" : "Helpdesk",
   "city" : "New Taipei City"

}


print(person["name"])
print(person["age"])
print(person["job"])


person["skill"] = "Python"
person["job"] = "AI Engineer"
del person["city"]

print(person)

for key, value in person.items():
    print(f"{key}:{value}")

'''

person1 = {

"name" : "Nathen",
"Age" : 28,
"skills" : ["Python","Helpdesk","Claude AI"],
"Interesting" :["Music","GYM","Nine ball"],
"Work":"Already locking for job",
"city":["Taipei","Taoyuan","New Taipei"]

}

for key,value in person1.items():
    print(f"{key}:{value}")
    
