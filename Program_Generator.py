import openpyxl
book = openpyxl.load_workbook('PHX185-IO-List Rev 2.5.xlsm', data_only=True)
hoja = book.active
# rango = hoja['A6' : 'AH1957']
rango = hoja['A6' : 'AL1957']
lista_Tags = []
rowtg=""

for fila in rango:
    tag = [celda.value for celda in fila]
    lista_Tags.append(tag)
    
# DEFINICION DE CONSTANTES EN EL PROGRAMA
list_tgNA = []
row1=[]
program_filecontent = []
list_progs = []
progcant = 0


CLX_Init_Count=0
ProgTagType = ["P_Motor","P_DIn"]

#TAGS VARIABLES

Newtagtype = "P_Motor"

#PMotor Variables Requeridas por cada nueva estrategia de control.
NwPmotor_tag = "MOTOR01"
NwPmotor_Inptg = "Pmotor_Dir_aux"
NwPmotor_Outptg = "Pmotor_Dir_aux1"

#PDIN Variables Requeridas por cada nueva estrategia de control.
NwPDIn_tag = "bc3101_MS"
NwPDIn_Inptg = "bd3101_MS"

#VSD Variables Requeridas por cada nueva estrategia de control.
NwPvsd_tag = "_VSD01_M01"
NwPvsd_Inptg = "_vsd1_AUX"
NwPvsd_Outptg = "_vsd101_Coil"
NwPvsd_OutSpeedtg = "Outspeed_ref"
NwPvsd_OutRuntg = "Vsd_OutRun"

#PAIn Variables Requeridas por cada nueva estrategia de control.
NwPAIn_tag = "LT01"
NwPAIn_Inptg = "LT01_INPRAW"

#4DSD Variables Requeridas por cada nueva estrategia de control.
NwPd4sd_tag = "_4DSDTEST_M01"
NwPd4sd_Inptg = "_4DSDtst_AUX"
NwPd4sd_Inpt1g = "Inp_d4sd"
NwPd4sd_Outptg = "_4DSDtst_Coil"
NwPd4sd_Out1ptg = "_4DSDtst_Coil"
#Aout Variables Requeridas por cada nueva estrategia de control.
NwAOut_tag = "PAoutTEST"
NwAOut_Outptg = "paout_cv"

#DOut Variables Requeridas por cada nueva estrategia de control.
NwDOut_tag = "PDoutTEST1"
NwDOut_Outptg = "pdout_coil"

#DOut Variables Requeridas por cada nueva estrategia de control.
NwValvso_tag = "PValveTEST1"
NwValvso_Outptg = "pvalve_coil"

# DEFINICION DE FUNCION PARA Tags

def NewProg_Tag(fname, NwTag, FindTg, NwDesc):
    FcRead_file = open(f'{fname}',"r")
    FcNewFile_content=""
    for Fcline in FcRead_file:
    # stripped_line = line.strip()
        if Fcline.find('TagDescript') >= 0:
            FcNew_line = Fcline.replace('TagDescript', NwDesc)
        else:
            FcNew_line = Fcline.replace(FindTg, NwTag)
        FcNewFile_content += FcNew_line
    FcNewFile_content += "\n"
    FcRead_file.close()
    return FcNewFile_content


CLX_Init_file = open("Init.L5X", encoding='utf-8')
New_file_content = ""
for line in CLX_Init_file:
    if CLX_Init_Count == 0:
        newline = line.strip()
        New_file_content += newline + "\n"
    else:          
        New_file_content += line
    CLX_Init_Count += 1
New_file_content += "\n"
CLX_Init_file.close()


list_tagsAOI1 =[]
row4 = []


for tag in lista_Tags:
    checktg1 = 0
    if tag[31] != None and tag[31] != "NA" and tag[32] != None:
        temptagAOI1name = tag[31].strip()
        for rw in list_tagsAOI1:
            if temptagAOI1name == rw[0]:
                checktg1 = 1
                            # if rw[1] == "P_Motor" and rw[2] == "Sts_Running":
                            #     NwPmotor_Inptg = tag[10]
                break
            else:
                checktg1 = 0
        if checktg1 == 0:    
            tagAOI1name = tag[31].strip()
            row4= [f'{tag[31]}', f'{tag[32]}', f'{tag[33]}']
            list_tagsAOI1.append(row4)
            if tag[32].strip() == "P_AIn":
                        # NUEVO TAG AIN
                New_file_content += NewProg_Tag("D_TagPAIn.L5X",tagAOI1name,"XT101",tag[13])
            elif tag[32].strip() == "P_DIn":
                        # NUEVO TAG PDIn
                New_file_content += NewProg_Tag("B_Tag_PDIn.L5X",tagAOI1name,"LS100",tag[13])
            elif tag[32].strip() == "P_Motor":
                        # NUEVO TAG PMotor
                New_file_content += NewProg_Tag("A_Tag_PMotor.L5X",tagAOI1name,"MT100",tag[13])
            elif tag[32].strip() == "P_VSD":
                    # NUEVO TAG PVSD
                New_file_content += NewProg_Tag("C_TagPVSD.L5X",tagAOI1name,"MT300",tag[13])
            elif tag[32].strip() == "P_D4SD":
                            # NUEVO TAG D4SD
                New_file_content += NewProg_Tag("E_TagP4DSD.L5X",tagAOI1name,"D4SD100",tag[13])
            elif tag[32].strip() == "P_AOut":
                New_file_content += NewProg_Tag("F_Tag_PAOut.L5X",tagAOI1name,"XC100",tag[13])
            elif tag[32].strip() == "P_Dout":
                New_file_content += NewProg_Tag("G_Tag_PDOut.L5X",tagAOI1name,"XY100",tag[13])
            elif tag[32].strip() == "P_ValveSO":
                New_file_content += NewProg_Tag("H_Tag_PValveSO.L5X",tagAOI1name,"XV100",tag[13])
            elif tag[32].strip() == "NA":
                row1=[f'{tag[31]}', f'{tag[32]}',f'{tag[33]}']
                list_tgNA.append(row1)

# New_file_content += "\n"
New_file_content += "</Tags>\n"

############## INICIA LA SECCION DE PROGRAMA #######################
New_file_content += "<Programs>\n"


for tag in lista_Tags:
    check_prog=0
    if tag[35] != None:
        progtemp = tag[35].strip()
        for tgprog in list_progs:
            if progtemp == tgprog[1]:
                check_prog=1
                break
            else:
                check_prog=0
        if check_prog != 1:        
            prog_actual = progtemp
            progcant+=1
            row2=[f'{progcant}',f'{prog_actual}', f'{tag[36]}']
            list_progs.append(row2)
            
list_tagsAOI =[]
row3 = []
for prog in list_progs:
    Jsr_prog_content=[]
    Jsr_routine_content = []
    jrs_routine_count=0
    tag_prog_content=""
    routines_content=""
    prognum = int(prog[0])
    
    New_file_content+= f'<Program Name="{prog[1]}" TestEdits="false" MainRoutineName="Main_Routine" Disabled="false" UseAsFolder="false">\n'
    New_file_content += '<Tags>\n'
    
    for tag in lista_Tags:
        checktg = 0
        if tag[31] != None and tag[31] !="NA" and  tag[35] != None:
            if tag[35].find(prog[1])>=0:
                tagstatus = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                temptagAOIname = tag[31].strip()
                for rw in list_tagsAOI:
                    if temptagAOIname == rw[0]:
                        checktg = 1
                        # if rw[1] == "P_Motor" and rw[2] == "Sts_Running":
                        #     NwPmotor_Inptg = tag[10]
                        break
                    else:
                        checktg = 0
                if checktg == 0:    
                    tagAOIname = temptagAOIname
                    row3= [f'{tag[31]}', f'{tag[32]}', f'{tag[33]}']
                    list_tagsAOI.append(row3)
                if checktg == 0:              
                    if tag[32].strip() == "P_Motor":
                        tag_prog_content += NewProg_Tag("A_TagProgram_PMotor.L5X",tagAOIname,"MT100",tagAOIname)
                    elif tag[32].strip() == "P_DIn":
                        tag_prog_content += NewProg_Tag("B_TagProgram_PDIn.L5X",tagAOIname,"LS100",tagAOIname)
                    elif tag[32].strip() == "P_VSD":
                        tag_prog_content += NewProg_Tag("C_TagProgram_PVSD.L5X",tagAOIname,"MT300",tagAOIname)
                    elif tag[32].strip() == "P_AIn":
                        tag_prog_content += NewProg_Tag("D_TagProgram_PAIn.L5X",tagAOIname,"XT101",tagAOIname)
                    elif tag[32].strip() == "P_D4SD":
                        tag_prog_content += NewProg_Tag("E_TagProgram_P4DSD.L5X",tagAOIname,"D4SD100",tagAOIname)
                    elif tag[32].strip() == "P_AOut":
                        tag_prog_content += NewProg_Tag("F_TagProgram_PAOut.L5X",tagAOIname,"XC100",tagAOIname)
                    elif tag[32].strip() == "P_Dout":
                        tag_prog_content += NewProg_Tag("G_TagProgram_PDOut.L5X",tagAOIname,"XY100",tagAOIname)
                    elif tag[32].strip() == "P_ValveSO":
                        tag_prog_content += NewProg_Tag("H_TagProgram_PValveSO.L5X",tagAOIname,"XV100",tagAOIname)
                    
                    
                    tagAOI = tag[31].strip()
                    AOItypetag = tag[32].strip()
                    #PMOTOR Rutina para estrategia de control
                    if AOItypetag == "P_Motor":
                        
                        for rowtg in lista_Tags:
                            if tagAOI == rowtg[31] and "Sts_Running" == rowtg[33]:
                                NwPmotor_Inptg = rowtg[34]
                                tagstatus[1] = 1
                                hoja[F'AM{6+int(rowtg[0])}']= "Programado"
                                
                            elif tagAOI == rowtg[31] and "PCmd_Start" == rowtg[33]:
                                NwPmotor_Outptg = rowtg[34]
                                tagstatus[2] = 2   
                                hoja[F'AM{6+int(rowtg[0])}']= "Programado"
                            elif tagAOI == rowtg[31] and "Sts_Ext" == rowtg[33]:
                                NwPmotor_InpExt = rowtg[34]
                                tagstatus[15] = 15   
                                hoja[F'AM{6+int(rowtg[0])}']= "Programado"
                            elif tagAOI == rowtg[31] and "Sts_Jogging" == rowtg[33]:
                                NwPmotor_InpJog = rowtg[34]
                                tagstatus[16] = 16   
                                hoja[F'AM{6+int(rowtg[0])}']= "Programado"
                            
                        CLX_Routine_PmotorFile = open("A_Routine_PMotor.L5X", "r")
                        for line in CLX_Routine_PmotorFile:
                            stripped_line_RoutnMotor = line.strip()
                            if stripped_line_RoutnMotor.find('Operand="MT100_Inp_RunFdbk"') >= 0 and tagstatus[1] == 1:
                                New_line_RoutnMotor = stripped_line_RoutnMotor.replace("MT100_Inp_RunFdbk", NwPmotor_Inptg)
                            elif stripped_line_RoutnMotor.find('Operand="MT100_Out_Run"') >= 0 and tagstatus[2] == 2:
                                New_line_RoutnMotor = stripped_line_RoutnMotor.replace("MT100_Out_Run", NwPmotor_Outptg)
                            elif stripped_line_RoutnMotor.find('Operand="MT100_Inp_XCmdAcq"') >= 0 and tagstatus[15] == 15:
                                New_line_RoutnMotor = stripped_line_RoutnMotor.replace("MT100_Inp_XCmdAcq", NwPmotor_InpExt)
                            elif stripped_line_RoutnMotor.find('Operand="MT100_Inp_XCmdJog"') >= 0 and tagstatus[16] == 16:
                                New_line_RoutnMotor = stripped_line_RoutnMotor.replace("MT100_Inp_XCmdJog", NwPmotor_InpJog)    
                            else:
                                New_line_RoutnMotor = stripped_line_RoutnMotor.replace("MT100", tagAOIname)
                            routines_content += New_line_RoutnMotor +"\n"
                        CLX_Routine_PmotorFile.close()
                        
                    elif tag[32].strip() == "P_DIn":
                        for rowtg in lista_Tags:
                            if tagAOI == rowtg[31] and "Sts_PV" == rowtg[33]:
                                NwPDIn_Inptg = rowtg[34]
                                tagstatus[3] = 3         
                                hoja[F'AM{6+int(rowtg[0])}']= "Programado"                       
                        #PDIN Estrategia de control
                        Routine_PDInFile = open("B_Routine_PDIn.L5X", "r")
                        for line in Routine_PDInFile:
                            stripped_line_RoutnDIn = line.strip()
                            if stripped_line_RoutnDIn.find('Operand="LS100_Inp_PV"') >= 0 and tagstatus[3] == 3:
                                New_line_RoutnDIn = stripped_line_RoutnDIn.replace("LS100_Inp_PV", NwPDIn_Inptg)
                            else:
                                New_line_RoutnDIn = stripped_line_RoutnDIn.replace("LS100", tagAOIname)
                            routines_content += New_line_RoutnDIn +"\n"
                        Routine_PDInFile.close()
                    
                    elif tag[32].strip() == "P_VSD":
                        #PVSD ESTRATEGIA DE CONTROL
                        for rowtg in lista_Tags:
                            if tagAOI == rowtg[31] and "Out_SpeedRef" == rowtg[33]:
                                NwPvsd_OutSpeedtg = rowtg[34]
                                tagstatus[4] = 4
                                hoja[F'AM{6+int(rowtg[0])}']= "Programado"
                            elif tagAOI == rowtg[31] and "Sts_RunningFwd" == rowtg[33]:
                                NwPvsd_Inptg = rowtg[34]
                                tagstatus[5] = 5
                                hoja[F'AM{6+int(rowtg[0])}']= "Programado"
                            elif tagAOI == rowtg[31] and "PCmd_StartFwd" == rowtg[33]:
                                NwPvsd_OutRuntg = rowtg[34]
                                tagstatus[6] = 6
                                hoja[F'AM{6+int(rowtg[0])}']= "Programado"
                            elif tagAOI == rowtg[31] and "Sts_DriveFault" == rowtg[33]:
                                NwPvsd_InpDrFault = rowtg[34]
                                tagstatus[17] = 17
                                hoja[F'AM{6+int(rowtg[0])}']= "Programado"
                            elif tagAOI == rowtg[31] and "Sts_AtSpeed" == rowtg[33]:
                                NwPvsd_InpAtSpeed = rowtg[34]
                                tagstatus[18] = 18
                                hoja[F'AM{6+int(rowtg[0])}']= "Programado"
                            elif tagAOI == rowtg[31] and "Out_ClearFault" == rowtg[33]:
                                NwPvsd_InpReset = rowtg[34]
                                tagstatus[19] = 19
                                hoja[F'AM{6+int(rowtg[0])}']= "Programado"
                            elif tagAOI == rowtg[31] and "Inp_SpeedFdbk" == rowtg[33]:
                                NwPvsd_InpSpFdbk = rowtg[34]
                                tagstatus[20] = 20
                                hoja[F'AM{6+int(rowtg[0])}']= "Programado"
                
                        Routine_PVSDFile = open("C_Routine_PVSD.L5X", "r")
                        for line in Routine_PVSDFile:
                            stripped_line_RoutnVSD = line.strip()
                            if stripped_line_RoutnVSD.find('Operand="MT300_Inp_Running"') >= 0 and tagstatus[5] == 5:
                                New_line_RoutnVSD = stripped_line_RoutnVSD.replace("MT300_Inp_Running", NwPvsd_Inptg)
                            elif stripped_line_RoutnVSD.find('Operand="MT300_Out_SpeedRef"') >= 0 and tagstatus[4] == 4:
                                New_line_RoutnVSD = stripped_line_RoutnVSD.replace("MT300_Out_SpeedRef", NwPvsd_OutSpeedtg)
                            elif stripped_line_RoutnVSD.find('Operand="MT300_Out_Run"') >= 0 and tagstatus[6] == 6:
                                New_line_RoutnVSD = stripped_line_RoutnVSD.replace("MT300_Out_Run", NwPvsd_OutRuntg)
                            elif stripped_line_RoutnVSD.find('Operand="MT300_Inp_Faulted"') >= 0 and tagstatus[17] == 17:
                                New_line_RoutnVSD = stripped_line_RoutnVSD.replace("MT300_Inp_Faulted", NwPvsd_InpDrFault)
                            elif stripped_line_RoutnVSD.find('Operand="MT300_Inp_AtSpeed"') >= 0 and tagstatus[18] == 18:
                                New_line_RoutnVSD = stripped_line_RoutnVSD.replace("MT300_Inp_AtSpeed", NwPvsd_InpAtSpeed)
                            elif stripped_line_RoutnVSD.find('Operand="MT300_Inp_Reset"') >= 0 and tagstatus[19] == 19:
                                New_line_RoutnVSD = stripped_line_RoutnVSD.replace("MT300_Inp_Reset", NwPvsd_InpReset)
                            elif stripped_line_RoutnVSD.find('Operand="MT300_Inp_SpeedFdbk"') >= 0 and tagstatus[20] == 20:
                                New_line_RoutnVSD = stripped_line_RoutnVSD.replace("MT300_Inp_SpeedFdbk", NwPvsd_InpSpFdbk)
                            else:
                                New_line_RoutnVSD = stripped_line_RoutnVSD.replace("MT300", tagAOIname)
                            routines_content += New_line_RoutnVSD +"\n"
                        Routine_PVSDFile.close()

                    elif tag[32].strip() == "P_AIn":
                        #PAIN RUTINA ESTRATEGIA DE CONTROL
                        for rowtg in lista_Tags:
                            if tagAOI == rowtg[31] and "Val" == rowtg[33]:
                                NwPAIn_Inptg = rowtg[34]
                                tagstatus[7] = 7
                                hoja[F'AM{6+int(rowtg[0])}']= "Programado"
                                
                        Routine_AInDFile = open("D_Routine_PAIn.L5X", "r")
                        for line in Routine_AInDFile:
                            stripped_line_RoutnAIN = line.strip()
                            if stripped_line_RoutnAIN.find('Operand="XT101_Inp_Raw"') >= 0  and tagstatus[7] == 7:
                                New_line_RoutnAIn = stripped_line_RoutnAIN.replace("XT101_Inp_Raw", NwPAIn_Inptg)
                            else:
                                New_line_RoutnAIn = stripped_line_RoutnAIN.replace("XT101", tagAOIname)
                            routines_content += New_line_RoutnAIn +"\n"
                        Routine_AInDFile.close()
                        
                    elif tag[32].strip() == "P_D4SD":
                        
                        for rowtg in lista_Tags:
                            if tagAOI == "_DG8330": 
                                chk=1
                            if tagAOI == rowtg[31] and "PCmd_St0" == rowtg[33]:
                                NwPd4sd_Outptg = rowtg[34]
                                tagstatus[8] = 8
                                hoja[F'AM{6+int(rowtg[0])}']= "Programado"
                            elif tagAOI == rowtg[31] and "PCmd_St1" == rowtg[33]:
                                NwPd4sd_Out1ptg = rowtg[34]    
                                tagstatus[9] = 9
                                hoja[F'AM{6+int(rowtg[0])}']= "Programado"
                            elif tagAOI == rowtg[31] and "Sts_St0" == rowtg[33]:
                                NwPd4sd_Inptg = rowtg[34]
                                tagstatus[10] = 10
                                hoja[F'AM{6+int(rowtg[0])}']= "Programado"
                            elif tagAOI == rowtg[31] and "Sts_St1" == rowtg[33]:
                                NwPd4sd_Inpt1g = rowtg[34]
                                tagstatus[11] = 11
                                hoja[F'AM{6+int(rowtg[0])}']= "Programado"
                        #D4DSD RUTINA ESTRATEGIA DE CONTROL
                        Routine_D4sdDFile = open("E_Routine_PD4SD.L5X", "r")
                        for line in Routine_D4sdDFile:
                            stripped_line_RoutnD4sd = line.strip()
                            if stripped_line_RoutnD4sd.find('Operand="D4SD100_Inp_FdbkA"') >= 0 and tagstatus[10] == 10:
                                New_line_RoutnD4sd = stripped_line_RoutnD4sd.replace("D4SD100_Inp_FdbkA", NwPd4sd_Inptg)
                            elif stripped_line_RoutnD4sd.find('Operand="D4SD100_Inp_FdbkB"') >= 0 and tagstatus[11] == 11:
                                New_line_RoutnD4sd = stripped_line_RoutnD4sd.replace("D4SD100_Inp_FdbkB", NwPd4sd_Inpt1g)
                            elif stripped_line_RoutnD4sd.find('Operand="D4SD100_Out_A"') >= 0 and tagstatus[8] == 8:
                                New_line_RoutnD4sd = stripped_line_RoutnD4sd.replace("D4SD100_Out_A", NwPd4sd_Outptg)
                            elif stripped_line_RoutnD4sd.find('Operand="D4SD100_Out_B"') >= 0 and tagstatus[9] == 9:
                                New_line_RoutnD4sd = stripped_line_RoutnD4sd.replace("D4SD100_Out_B", NwPd4sd_Out1ptg)
                            else:
                                New_line_RoutnD4sd = stripped_line_RoutnD4sd.replace("D4SD100", tagAOIname)
                            routines_content += New_line_RoutnD4sd +"\n"
                        Routine_D4sdDFile.close()
                        
                    elif tag[32].strip() == "P_AOut":
                        for rowtg in lista_Tags:
                            if tagAOI == rowtg[31] and "Out_CV" == rowtg[33]:
                                NwAOut_Outptg = rowtg[34]
                                tagstatus[12] = 12
                                hoja[F'AM{6+int(rowtg[0])}']= "Programado"
                        #PAOUT RUTINA ESTRATEGIA DE CONTROL
                        Routine_AOUTFile = open("F_Routine_PAOut.L5X", "r")
                        for line in Routine_AOUTFile:
                            stripped_line_RoutnAout = line.strip()
                            if stripped_line_RoutnAout.find('Operand="XC100_Out_CV"') >= 0 and tagstatus[12] == 12:
                                New_line_RoutnAout = stripped_line_RoutnAout.replace("XC100_Out_CV", NwAOut_Outptg)
                            else:
                                New_line_RoutnAout = stripped_line_RoutnAout.replace("XC100", tagAOIname)
                            routines_content += New_line_RoutnAout +"\n"
                        Routine_AOUTFile.close()
                    
                    elif tag[32].strip() == "P_Dout":
                        for rowtg in lista_Tags:
                            if tagAOI == rowtg[31] and "PCmd_On" == rowtg[33]:
                                NwDOut_Outptg = rowtg[34]
                                tagstatus[13] = 13
                                hoja[F'AM{6+int(rowtg[0])}']= "Programado"
                        #PDOUT RUTINA ESTRATEGIA DE CONTROL
                        Routine_DOUTFile = open("G_Routine_PDOut.L5X", "r")
                        for line in Routine_DOUTFile:
                            stripped_line_RoutnDout = line.strip()
                            if stripped_line_RoutnDout.find('Operand="XY100_Out"') >= 0 and tagstatus[13] == 13:
                                New_line_RoutnDout = stripped_line_RoutnDout.replace("XY100_Out", NwDOut_Outptg)
                            else:
                                New_line_RoutnDout = stripped_line_RoutnDout.replace("XY100", tagAOIname)
                            routines_content += New_line_RoutnDout +"\n"
                        Routine_DOUTFile.close()
                        
                    elif tag[32].strip() == "P_ValveSO":
                        for rowtg in lista_Tags:
                            if tagAOI == rowtg[31] and "Out" == rowtg[33]:
                                NwValvso_Outptg = rowtg[34]
                                tagstatus[14] = 14
                                hoja[F'AM{6+int(rowtg[0])}']= "Programado"
                        #PDOUT RUTINA ESTRATEGIA DE CONTROL
                        Routine_ValvesoFile = open("H_Routine_PValveSO.L5X", "r")
                        for line in Routine_ValvesoFile:
                            stripped_line_RoutnValvso = line.strip()
                            if stripped_line_RoutnValvso.find('Operand="XV100_Out"') >= 0 and tagstatus[14] == 14:
                                New_line_RoutnValvso = stripped_line_RoutnValvso.replace("XV100_Out", NwValvso_Outptg)
                            else:
                                New_line_RoutnValvso = stripped_line_RoutnValvso.replace("XV100", tagAOIname)
                            routines_content += New_line_RoutnValvso +"\n"
                        Routine_ValvesoFile.close()
                    rowroutines = [f'{jrs_routine_count}',f'<![CDATA[JSR({tagAOIname},0);]]>\n']
                    Jsr_routine_content.append(rowroutines)
                    jrs_routine_count+=1
                    hoja[F'AL{6+int(tag[0])}']= tagAOIname
                # hoja[F'AM{6+int(tag[0])}']= tagAOIname
    
    New_file_content += tag_prog_content
    # New_file_content += "\n"
    New_file_content += '</Tags>\n'
    #INICIA SECCION DE NUEVAS RUTINAS

    New_file_content += '<Routines>\n'
     #Rutina Principal de Programa
    New_file_content += routines_content
    New_file_content += '<Routine Name="Main_Routine" Type="RLL">\n'
    New_file_content += '<RLLContent>\n'
    for jsr in Jsr_routine_content:
        New_file_content += f'<Rung Number="{int(jsr[0])}" Type="N">\n'
        New_file_content += '<Text>\n'
        New_file_content += f'{jsr[1]}'
        New_file_content += '</Text>\n'
        New_file_content += '</Rung>\n'
    New_file_content += '</RLLContent>\n'
    New_file_content += '</Routine>\n'
    
    New_file_content += '</Routines>\n'
    New_file_content += '</Program>\n'

New_file_content += "</Programs>\n"

############## INICIA LA SECCION DE TASK #######################
New_file_content += '<Tasks>\n'

New_file_content += f'<Task Name="Task_B" Type="PERIODIC" Rate="50" Priority="10" Watchdog="500" DisableUpdateOutputs="false" InhibitTask="false">\n'
New_file_content += '<ScheduledPrograms>\n'
for rw in list_progs:
    if rw[2] == "Task_B":
        New_file_content += f'<ScheduledProgram Name="{rw[1]}"/>\n'
New_file_content += '</ScheduledPrograms>\n'
New_file_content += '</Task>\n'
New_file_content += '<Task Name="Task_C" Type="PERIODIC" Rate="100" Priority="10" Watchdog="500" DisableUpdateOutputs="false" InhibitTask="false">\n'
New_file_content += '<ScheduledPrograms>\n'
for rw in list_progs:
    if rw[2] == "Task_C":
        New_file_content += f'<ScheduledProgram Name="{rw[1]}"/>\n'
New_file_content += '</ScheduledPrograms>\n'
New_file_content += '</Task>\n'
New_file_content += '<Task Name="Task_D" Type="PERIODIC" Rate="100" Priority="10" Watchdog="500" DisableUpdateOutputs="false" InhibitTask="false">\n'
New_file_content += '<ScheduledPrograms>\n'
for rw in list_progs:
    if rw[2] == "Task_D":
        New_file_content += f'<ScheduledProgram Name="{rw[1]}"/>\n'
New_file_content += '</ScheduledPrograms>\n'
New_file_content += '</Task>\n'


New_file_content += '</Tasks>'
############## CIERRE DE PROGRAMA #######################
CLX_Cierre_file = open("Close.L5X", "r")
New_file_content += "\n"
for line in CLX_Cierre_file:
    New_file_content += line
CLX_Cierre_file.close()


CLXprogFile = open("Program1.L5X","w", encoding="utf-8") 
CLXprogFile.write(New_file_content)
CLXprogFile.close()
book.save('prueba.xlsx')


