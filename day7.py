def greet(name):
    message = f"hello,I'm {name}"
    return message

result = greet("Nathen")
print(result)


def introduce(name,job,city):
    return f"我叫{name}，職業是{job}，住在{city}"

print(introduce("Nathen","Helpdesk","Taipei"))



def greet_user(name,language ="中文"):
    if language == "中文":
        return f"你好，{name}!"
    else:
        return f"hello,{name}!"
    
print(greet_user("Nathen"))
print(greet_user("Nathen","英文"))


def show_skills(person):
    print(f"姓名{person['name']}")
    for skill in person["skills"]:
        print(f" - {skill}")


my_profile={

     "name" : "Nathen",
     "skills" : ["Python","Helpdesk","Claude AI"]


}
       

show_skills(my_profile)


def calc_age(birth_year):
    current_year = 2026
    age = current_year - birth_year
    retire_year = 65 - age
    return f"你今年{age}歲，距離退休還有{retire_year}年!"

print(calc_age(1998))