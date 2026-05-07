skills =["Python","Excel","Helpdesk"]
'''
print(skills[0])
print(skills[1])
print(skills[-1])
print(len(skills))
'''
skills.append("Claude AI")
skills.append("Communicate with User")
skills.append("Fixxed PC/NB")
skills.append("Create SOP text")
skills.append("Use USB/Type-C")
skills.remove("Use USB/Type-C")
skills.remove("Excel")
'''
for skill in skills:
    print(f"我會的技能:{skills}")
'''
for skill in skills:
    if skills[0]:
        continue
    if skills[5]:
        break
print(f"我會的技能有:{skills}")

for skill in skills:          
     print(f"我會的技能：{skill}")


print("我會的技能有:"+",".join(skills))

result = ""
i = 0

while i < len(skills):
    if i == len(skills)-1:
        result += skills[i]
    else:
        result += skills[i]+","
        i += 1
print(f"我會的技能有:{result}")

