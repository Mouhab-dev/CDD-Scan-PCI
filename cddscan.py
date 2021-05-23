import csv,re

with open('test.csv','r') as f:
    reader=csv.reader(f, delimiter=',')
    for index,row in enumerate(reader):
        #print(row,index)
        row_string = ",".join(row)
        if index == 0: 
            first_row = row
            #print(first_row)
        # print(row_string)
        x = re.findall(r"4[0-9]{12}(?:[0-9]{3})?",row_string)
        ccn_indecies = [index for index,item in enumerate(row) if item in x]
        # print(ccn_indecies)
        field_names = []
        for i in ccn_indecies:
            field_names.append(first_row[i])
        
        if len(x) != 0 : print(x,"at Field Names:",field_names)
