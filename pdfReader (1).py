import fitz
import csv
import re

#page 2472 - 4120
doc = fitz.open("FullCEHReport2.pdf")

data = {'Location':[],
        'Perpetrator':[],
        'Type of Action':[],
        'Year':[],
        'Certainty':[],
        'Case Number':[],
        'Description of the event':[],
        'Names of victims':[],
        'Number of victims without identification':[]
        }

left_rect = fitz.Rect(40,30,173,700)
right_rect = fitz.Rect(178, 30, 612, 700)
left = ""
right = ""
for page in doc:
   # if (page.number >= 2471 and page.number < 2851) or (page.number >= 2865 and page.number < 3242) or (page.number >= 3251 and page.number < 3689) or (page.number >= 3705 and page.number <= 4120):
    left += (page.get_textbox(left_rect))
    left += "\n"
    right += (page.get_textbox(right_rect))
    right += "\n"

#left = re.sub("\wnewpage\w", "test", left)
left = re.sub("\n+", "\n", left)
left = left.split("\n")


right = right.replace("\n", "")
right = right.replace("Víctimas sin identificar:", "\nVíctimas sin identificar:")
right = right.replace("Víctimas identificadas:", "\n")
matches = re.finditer("Víctimas sin identificar: \d+", right)

old = right
for match in matches:
    s = match.span()
    right = old[:s[1]-2]+"\n"+old[s[1]:]

right = re.sub("Víctimas sin identificar: \d", "Víctimas sin identificar: \n", right)
right = right.split("\n")
for x in range(len(right)):
    #print(right[x]+"\n------------")
    #if "Víctimas sin identificar:" in right[x]:
        #right[x] = right[x].replace("Víctimas sin identificar: ", "")
        #m = re.match("^\d", right[x]).group()
        #right[x] = right[x][int(m)]
        #data['Number of victims without identification'].append(m)
    #else:
    data['Number of victims without identification'].append("")
    data['Description of the event'].append("")
    data['Names of victims'].append("")
    

#print(right)

count = len(left)
next = 0
for x in range(count):
    if x == next and x+6 <= count:
        data['Location'].append(left[0+x])
        data['Perpetrator'].append(left[1+x])
        data['Type of Action'].append(left[2+x])
        if left[4+x] == "Año:":
            x = x+1
        elif "Certeza:" in left[4+x]:
            certainty = left[4+x][left[4+x].index("Certeza:"):]
            year = left[4+x][:left[4+x].index("Certeza:")]
           # print(certainty)
            left.insert(5+x, certainty)
        data['Year'].append(left[4+x])
        if len(left[5+x].split()) == 2:
            data['Certainty'].append(left[5+x].split()[1])
        else:
            data['Certainty'].append("")
        if len(left[6+x].split()) == 2:
            data['Case Number'].append(left[6+x].split()[1])
        else:
            data['Case Number'].append("")
        next = x+7
#print(right)
#print(left)
#print(data)

fieldnames = data.keys()
with open('output2.csv', 'w', newline='') as output:
    writer = csv.writer(output)
    writer.writerow(fieldnames)
    results = zip(data['Location'], data['Perpetrator'], data['Type of Action'], data['Year'], data['Certainty'], data['Case Number'], data['Description of the event'], data['Names of victims'], data['Number of victims without identification'])
    for result in results:
        writer.writerow(result)

#print(text)
