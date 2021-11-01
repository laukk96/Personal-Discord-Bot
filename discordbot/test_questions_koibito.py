mstr = 'Visit Character \nVisitor · <@476844367613526036> \nCharacter · **Megumin** (`h333gv`) \nAffection Rating · **118.03**/200 (**Enamored**) \nAffection Points · **183** \nEnergy · ■■■■□\n \n *“Which supernatural beings do you think are most likely to exist?”*\n\n1️⃣ Mermaids\n2️⃣ Unicorns\n3️⃣ Vampires\n4️⃣ Angels'
footerText = 'Choose the response most likely to impress Megumin'

# embed['title']
# Visit Character


# embed['description']

# Visitor · <@476844367613526036>
# Character · **Megumin** (`h333gv`)
# Affection Rating · **118.03**/200 (**Enamored**)
# Affection Points · **183**
# Energy · ■■■■□
# 
# *“Which supernatural beings do you think are most likely to exist?”*
# 
# 1️⃣ Mermaids
# 2️⃣ Unicorns
# 3️⃣ Vampires
# 4️⃣ Angels


# embed['footer']['text']
# Choose the response most likely to impress Megumin


char = None
question = None
answers = []


temp = mstr[mstr.find("Energy"):len(mstr)]
print(temp.find('*“'), temp.find('”*'))
question = temp[ temp.find('*“') + len('*“'):temp.find('”*') ]

print("question: " + question)

temp = mstr[mstr.find("”*") + len('”*'):len(mstr)]

print(temp)

answers = temp.split("\n")

print(answers)

while "" in answers:
    answers.remove("")
        

print("\nNEW")
print(answers)


td = {
    'footer': "",
    'title': 'pen',
    'description': 'trying to code'
    }

print(td['footer'] != None)