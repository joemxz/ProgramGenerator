# Program_Close_txt = ['</Routines>\n','</Program>\n']

# CLX_Init_file = open("datos.txt", "r")
# New_file_content = ""
# for line in CLX_Init_file:
#     New_file_content += line
# print(New_file_content)

# for strline in Program_Close_txt:
#     New_file_content += strline
# print(New_file_content)
# CLX_Init_file.close()


list01 = []


def actual_tpr(actual_task, actual_program, actual_routine):
    row1 = [f'{actual_task}',f'{actual_program}',f'{actual_routine}']
    return row1
    

s = '<Routine Name="_BC4401BIN_ALM" Type="FBD">'
l = s.split('"')[1::2]  # the [1::2] is a slicing which extracts odd values
print(l)

for i in range(0,3):
     list01.append(actual_tpr(f'task {i}',f'progr {i}',f'{l[0]}+{i}'))
print (list01)

for row in list01:
    print(row)
    for i in range(len(row)):
        print(row[i])
        
print(list01[0][2])

userInputtedText = '<Routine Name="Main_Routine" Type="RLL">'
import re
quoted = re.compile('"[^"]*"')

for value in quoted.findall(userInputtedText):
    print (value)




     
 



# transposed = []
# matrix = [["task1", "task2", "task3"], ["program1", "program2", "program3"], ["routine1", "routine2", "routine3"]]

# for i in range(len(matrix[0])):
#     transposed_row = []

#     for row in matrix:
#         transposed_row.append(row[i])
#     transposed.append(transposed_row)

# print(transposed)


# # Python program to merge two 3D list into one
# # importing pretty printed
# import pprint
  
# def ThreeD(a, b, c):
#     lst1 = [[ ['1' for col in range(a)] for col in range(b)] for row in range(c)]
#     lst2= [[ ['2' for col in range(a)] for col in range(b)] for row in range(c)]
#     # Merging using "+" operator
#     lst = lst1+lst2
#     return lst
      
# # Driver Code
# col1 = 1
# col2 = 1
# row = 1
  
# # used the pretty printed function
# pprint.pprint(ThreeD(col1, col2, row))

