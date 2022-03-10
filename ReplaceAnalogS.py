from tkinter.tix import ExFileSelectBox
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

def FindDataType(Texto):
    Datatype = ""
    if (Texto == "1756-IA16") or (Texto == "1756-OA16") or (Texto == "1756-IB16") or (Texto == "1756-OA16I"):
            Datatype = "BOOL"
    elif Texto == "1756-IF16":
            Datatype = "INT"
    elif (Texto == "1756-IRT8I") or (Texto == "1756-OF8I"):
            Datatype = "REAL"
    else:
            Datatype = "Error"
    return Datatype

book = openpyxl.load_workbook('PHX185-IO-List Rev 2.5.xlsm', data_only=True)

hoja = book.active

# rango = hoja['A6' : 'AH1957']
rango = hoja['A6' : 'AI1957']

orefID = []
lista_Tags = []
CoutFoundXIC = 0
CoutFoundXIO = 0
RestoDec = 0
Res2toDec = 0

# print(celdas)
InptStDet = 'N'
OutptStDet = 'O'
TagIOType = 0
CoutFoundN = 0
for fila in rango:
    tag = [celda.value for celda in fila]
    lista_Tags.append(tag)
    

FindNsignal = 'Operand="N'
reading_file = open("USCNEL001.L5X", "r")
new_file_content = ""
for line in reading_file:
    
    stripped_line = line.strip()
    FindTextN = stripped_line.find(FindNsignal)
    if FindTextN>=0:
        CoutFoundN = CoutFoundN + 1
        orefID = line.split('"')[1::2]
        TagIOType = 0
        for tag in lista_Tags:
            if tag[31] != None and tag[32] != 'NA':
                temptagRs = str(tag[34])
                hoja[F'AQ{6+int(tag[0])}']= tag[34]
                if (temptagRs.find(orefID[3]) >= 0):
                    TagIOType = 1
                    FindXIO = (f'Operand="{temptagRs}"')
                    XIOReplace = (f'Operand="{tag[27]}"')
                    hoja[F'AR{6+int(tag[0])}']= "Revisado"
        if TagIOType==1:
            new_line = stripped_line.replace(FindXIO,XIOReplace)
        else:
            new_line = stripped_line
    else:new_line = line
    new_file_content += new_line +"\n"
reading_file.close()

writing_file = open("USCNEL001_N.L5X", "w")
writing_file.write(new_file_content)
writing_file.close()
book.save('prueba.xlsx')


# for fila in celdas:
#         print([celda.value for celda in fila])
