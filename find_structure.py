import openpyxl
book = openpyxl.load_workbook('PHX185-IO-List Rev 2.5.xlsm', data_only=True)
hoja = book.active
# rango = hoja['A6' : 'AH1957']
rango = hoja['A6' : 'AK1957']
lista_Tags = []
rowtg=""
for fila in rango:
    tag = [celda.value for celda in fila]
    lista_Tags.append(tag)
  

List_progroutine = []
prog=[]
rout=[]
prog_string=""
rout_string=""
tsk_str=""
prg_str=""
rout_str=""
x=0
y=0
tagtemp=[]

progfound=0
cont_rout=0
general_prog = open("USCNEL001_NELLIMEProg.L5X", "r")
for line in general_prog:
    stripped_line = line.strip()
      
    if stripped_line.find('Program Name=') >= 0:
            prog = line.split('"')[1::2]
            if len(prog) > 0:
                prog_temp =prog[0]
                if prog_temp != prog_string:
                    prog_string = prog_temp
            progfound = 1
    elif stripped_line.find('<Routine Name=') >= 0 and progfound == 1:
            rout = line.split('"')[1::2]
            if len(rout) > 0:
                rout_string=rout[0]
                row1=[f'{prog_string}',f'{rout_string}']
                List_progroutine.append(row1)
general_prog.close()

List_taskprogroutine = []
taskprou = ["","",""]
task=[]
prog2 =[]
task_string=""
general2_prog = open("USCNEL001_NELLIMEProg.L5X", "r")
for line in general2_prog:
    stripped_line = line.strip()
    if stripped_line.find('Task Name=') >= 0:
            task = line.split('"')[1::2]
            if len(task) > 0:
                task_temp =task[0]
                if task_temp != task_string:
                    task_string = task_temp
    elif stripped_line.find('<ScheduledProgram Name=') >= 0 and progfound == 1:
            prog2 = line.split('"')[1::2]
            if len(prog2) > 0:
                for row in List_progroutine:
                    if row[0] == prog2[0]:
                        tsk_str = task_string
                        prg_str = row[0]
                        rout_str = row[1]
                        row2=[f'{tsk_str}', f'{prg_str}',f'{rout_str}']
                        List_taskprogroutine.append(row2) 
                        cont_rout+=1
                        if cont_rout>=298:
                            check=1          
general2_prog.close()


#TAG[36] Task
#Tag[35] Area2
#Tag[31] TagAOI
for tag in lista_Tags:
    if tag[31] != None:
        striped_cell = tag[31].strip()
        for row in List_taskprogroutine:
            if striped_cell.find(row[2])>=0:
                hoja[F'AR{6+tag[0]}']= row[1]
                hoja[F'AS{6+tag[0]}']= row[0]
                hoja[F'AT{6+tag[0]}']= row[2]
                
for rw in List_taskprogroutine:
    for tg1 in lista_Tags:
        if tg1[31] != None:
            if rw[2].find(tg1[31])>=0:
                x=1
                break
            else:
                x=0
    if x!=1:
        hoja[F'AO{6+y}']= rw[2]
        hoja[F'AP{6+y}']= rw[1]
        hoja[F'AQ{6+y}']= rw[0]
        y+=1
        
book.save('prueba.xlsx')
