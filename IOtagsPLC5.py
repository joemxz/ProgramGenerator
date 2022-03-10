import openpyxl


# getting numbers from string 
# using re.findall()
import re
  
def OctalToDecimal(num): 
      
    decimal_value = 0 
    base = 1
  
    while (num): 
        last_digit = num % 10
        num = int(num / 10)
        decimal_value += last_digit * base
        base = base * 8  
    return decimal_value

book = openpyxl.load_workbook('PHX185-IO-List Rev 2.5.xlsm', data_only=True)

hoja = book.active

rango = hoja['A6' : 'AL1957']

lista_Tags = []
CoutFoundXIC = 0
CoutFoundXIO = 0
RestoDec = 0
Res2toDec = 0
y=0

# print(celdas)
InptStDet = 'I:'
OutptStDet = 'O:'
Ndet = 'N'
TagIOType = 0

for fila in rango:
    tag = [celda.value for celda in fila]
    lista_Tags.append(tag)
    
for tag in lista_Tags:
    if tag[11] != None:
        temptagRs = str(tag[11])
        FindInptRs = temptagRs.find(InptStDet)
        FindOptRs = temptagRs.find(OutptStDet)
        FindN = temptagRs.find(Ndet)
        if (FindInptRs >= 0):
                TagIOType = 1
                temp = re.findall(r'\d+', temptagRs)
                res = list(map(int, temp))
                RestoDec = OctalToDecimal(res[1])
                FindXIO = (f'I[{res[0]}].{RestoDec}')
                            
        elif (FindOptRs >= 0):
                TagIOType = 2
                temp2 = re.findall(r'\d+', temptagRs)
                res2 = list(map(int, temp2))
                Res2toDec = OctalToDecimal(res2[1])
                FindXIO = (f'O[{res2[0]}].{Res2toDec}')
        elif (FindN >= 0):
                TagIOType = 3
                temp3 = re.findall(r'\d+', temptagRs)
                res3 = list(map(int, temp3))
                FindXIO = (f'N{res3[0]}[{res3[1]}]')
        else:
                TagIOType = 4
                FindXIO=""
    else:
        FindXIO=""
    hoja[F'AI{6+y}']= FindXIO
    y+=1
book.save('prueba.xlsx')
    
    