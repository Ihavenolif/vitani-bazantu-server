with open("generate_query.txt") as query_file:
    QUERY = query_file.read()

LINES = QUERY.splitlines()

#Iterating through lines of the file
for task in LINES:
    LINES_TO_PRINT = task.split(";")[0]

    #Iterating through each line
    for lines in range(0,int(LINES_TO_PRINT)):



        for task_to_print in range(1, len(task.split(";"))):
            print(task_to_print)
            exit()
            #letter_count = int(task[task_to_print].split(":")[0])
            #letter = task[task_to_print].split(":")[1]
        
            for i in range(0, letter_count):
                print(letter + ";")

        

    