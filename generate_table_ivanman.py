import json

with open("generate_query.txt") as query_file:
    QUERY = query_file.read()

LINES = QUERY.splitlines()

result_file = open("result_file.txt", "a")
result_json = open("result_json.json", "a")

result_string = ""

#Iterating through lines of the file
for task in LINES:
    LINES_TO_PRINT = task.split(";")[0]

    #Iterating through each line
    for lines in range(0,int(LINES_TO_PRINT)):

        for task_to_print in range(1, int(len(task.split(";")))):

            #print(task.split(";")[task_to_print])
            
            letter_count = int(task.split(";")[task_to_print].split(":")[0])
            letter = task.split(";")[task_to_print].split(":")[1]
        
            for i in range(0, letter_count):
                result_string += letter + ";"
                result_file.write(letter + ";")
                #print(letter + ";")
        
        #print("\n")
        result_string += "\n"
        result_file.write("\n")
    

result_file.close()

result_list = []

for x in result_string.splitlines():
    temp_list = []
    for y in x.split(";"):
        if y == "": continue
        temp_list.append(y)
    
    result_list.append(temp_list)

print(json.dumps(result_list))   
result_json.write(json.dumps(result_list))