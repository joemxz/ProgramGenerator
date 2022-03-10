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
        
book = openpyxl.load_workbook('PHX185-IO-List Rev 2.5.xlsm', data_only=True)

hoja = book.active

# rango = hoja['A6' : 'AH1957']
rango = hoja['A86' : 'AI1957']

lista_Tags = []
CoutFoundXIC = 0
CoutFoundXIO = 0
RestoDec = 0
Res2toDec = 0

# print(celdas)
InptStDet = 'I'
OutptStDet = 'O'
TagIOType = 0

for fila in rango:
    tag = [celda.value for celda in fila]
    lista_Tags.append(tag)
    
for tag in lista_Tags:
        if tag[31] != None and tag[31] != "NA" and tag[32] != None:
            temptagRs = str(tag[34])
            FindInptRs = temptagRs.find(InptStDet)
            FindOptRs = temptagRs.find(OutptStDet)
            if (FindInptRs >= 0):
                TagIOType = 1
                #print("The original string : " + temptagRs)
                
                #  temp = re.findall(r'\d+', temptagRs)
                #  res = list(map(int, temp))
                #  RestoDec = OctalToDecimal(res[1])
                
                #  #print("The numbers list is : " + str(res))
                
                #  FindXIO = (f'XIO(I[{res[0]}].{res[1]})')
                #  FindXIC = (f'XIC(I[{res[0]}].{res[1]})')
                FindXIO = (f'XIO({temptagRs})')
                FindXIC = (f'XIC({temptagRs})')
                
                
                #print(FindXIO)
                #print(FindXIC)
                #resBool=(res[0]*16) + (res[1])
                #  nums = [int(s) for s in temptagRs.split() if s.isdigit()]
                # print (nums)
                XIOReplace = (f'XIO({tag[31]}.{tag[33]})')
                XICReplace = (f'XIC({tag[31]}.{tag[33]})')
            else:
                TagIOType = 4
            # print(f'El tag AOI {tag[31]} es un {tag[32]} y es revisado {tag[33]}')
            
            if (TagIOType == 1) or (TagIOType == 2):
                reading_file = open("_2_MCP_Program.L5X", "r")
                new_file_content = ""
                for line in reading_file:
                    stripped_line = line.strip()
                    
                    FindTextXIO = stripped_line.find(FindXIO)
                    
                    if FindTextXIO>=0:
                        CoutFoundXIO = CoutFoundXIO + 1
                
                    
                    new_line1 = stripped_line.replace(FindXIO,XIOReplace)
                    stripped_line1 = new_line1.strip()
                    FindTextXIC = stripped_line1.find(FindXIC)
                    
                    if FindTextXIC>=0:
                        CoutFoundXIC = CoutFoundXIC + 1
                        
                    
                    new_line = new_line1.replace(FindXIC, XICReplace)
                        
                    # print (new_line)
                    new_file_content += new_line +"\n"
                reading_file.close()

                writing_file = open("_2_MCP_Program.L5X", "w")
                writing_file.write(new_file_content)
                writing_file.close()


# for fila in celdas:
#         print([celda.value for celda in fila])
