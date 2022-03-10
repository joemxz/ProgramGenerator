# TagType = ["P_Motor","P_DIn"]
# Newtagtype = "P_Motor"
# con=0
# for tag in TagType:
#     con+=1
#     print(tag)
# if TagType[0] == Newtagtype:
#     print("Holla Mundo")
# else:
#     print ("nel no es igual compa")
    
# import openpyxl
# book = openpyxl.load_workbook('PHX185-IO-List Rev 2.0.xlsm', data_only=True)
# hoja = book.active
# # rango = hoja['A6' : 'AH1957']
# rango = hoja['A6' : 'AK1957']
# lista_Tags = []

# hoja['A1'] = "Hola Mundo Excel"

# book.save('prueba.xlsx')

# from difflib import SequenceMatcher

# def similar (a,b):
#     return SequenceMatcher(None, a, b).ratio()

# print (similar("_69_BC_8303A", "_BC8302_M01"))

# PROGRAMA PARA ORGANIZAR LAS RUTINAS.

progfndtemp = 0
routfndtemp =0 
Pifindinit = 0
Pifindclose = 0
routinesfound = 0
programscontent = []
routcontent = []
proginit = open("Simulation_Base.L5X", "r")
PinitNewFile_content = ""
PcloseNewFile_content = ""
progrmnew_content = ""
routnew_content = ""
new_file_content =""

for line in proginit:
    
    if Pifindinit == 0:
        PinitNewFile_content += line
    if line.find('<Programs>') >= 0:
            Pifindinit = 1
    if Pifindinit == 1 and line.find('<Program ') >= 0:
        progfndtemp = 1
    if progfndtemp == 1:
        progrmnew_content += line
        if line.find('<Routines>') >= 0:
                routinesfound = 1
                progfndtemp = 0
                programscontent.append(progrmnew_content)
                progrmnew_content = ""

    if routinesfound == 1 and line.find('<Routine ') >= 0:
        routfndtemp = 1
    if routfndtemp == 1:
        routnew_content += line
        if line.find('</Routine>') >= 0:
                routinesfound = 0
                routfndtemp = 0
                routcontent.append(routnew_content)
                routnew_content = ""
    
    if line.find('<Tasks>') >= 0:
        Pifindclose = 1
    if Pifindclose == 1:
        PcloseNewFile_content += line

proginit.close()

new_file_content += PinitNewFile_content
for prgcont  in programscontent:
    new_file_content += prgcont
new_file_content += PcloseNewFile_content


writing_file = open("PruebaCambioRutina.L5X", "w")
writing_file.write(new_file_content)
writing_file.close()