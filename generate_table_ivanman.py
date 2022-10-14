with open("generate_query.txt") as query_file:
    QUERY = query_file.read()

LINES = QUERY.splitlines()

result_file = open("result_file.txt", "a")

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
                result_file.write(letter + ";")
                #print(letter + ";")
        
        #print("\n")
        result_file.write("\n")
    
result_file.close()