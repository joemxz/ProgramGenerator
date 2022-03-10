from tkinter.tix import ExFileSelectBox
import openpyxl
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
        
book = openpyxl.load_workbook('PHX185-IO-List Rev 5.1.xlsm', data_only=True)

hoja = book.active

rango = hoja['A6' : 'AM1957']
#rango = hoja['A6' : 'AM11']

lista_Tags = []
CoutFoundXIC = 0
CoutFoundTagF = 0
RestoDec = 0
Res2toDec = 0

TagIOType = 0

for fila in rango:
    tag = [celda.value for celda in fila]
    lista_Tags.append(tag)
    
for tag in lista_Tags:
        print (tag[0])
        if tag[31] != None and tag[31] != "NA" and tag[32] != None and tag[23] != None:
            temptagRs = str(tag[23])

            FindTagF = (f'{temptagRs}')
            TagFReplace = (f'{tag[31]}.Val')
            
            reading_file = open("USCNEL001_Rev5_1_E.L5X", "r")
            new_file_content = ""
            for line in reading_file:
                # stripped_line = line.strip()
                
                if line.find(FindTagF) >= 0:
                    CoutFoundTagF = CoutFoundTagF + 1
                    hoja[F'AL{6+int(tag[0])}']= "Encontrado"
                new_line = line.replace(FindTagF, TagFReplace)
                new_file_content += new_line 
            new_file_content += "\n"
            reading_file.close()

            writing_file = open("USCNEL001_Rev5_1_E.L5X", "w")
            writing_file.write(new_file_content)
            writing_file.close()
     
book.save('prueba.xlsx')