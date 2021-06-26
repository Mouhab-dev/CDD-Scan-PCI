#!/usr/bin/python3

##################################################################

# This script was developed by Mouhab El-Banna
# Its currently under continous improvements
# version 2.0
# Supports Luhn Validation Check
# Regex Link for online testing: https://regex101.com/r/Qc4HdB/1

##################################################################

print ("\nWelcome to FILTER CDD SCAN RESULTS Script! Ver: 2.0")

import re, csv, os, glob

# Change dir to the cdd scan results
os.chdir("your csv files path")

# Print num of csv files found in the directory
print ("\nNumber of csv files found: ",len(list(glob.glob("*.csv"))))
print ("--------------------------------------------------------\n")

for file in glob.glob("*.csv"): # test should be * after debugging

    with open(file, 'r') as csv_file: # Open the csv file
        # Read lines
        csv_reader = csv.reader(csv_file, delimiter=',')
        row_number = 0
        ccn_found = False
        f_name_printed = False
        for index,row in enumerate(csv_reader):
            if index == 0: 
                first_row = row
            row_string = " ".join(row)
            row_number += 1
            if row_string != None :
                #print (row_string)

                # findall: returns a list and keep searching the whole row even if a match were found.
		            # search:  returns a single value and breaks out after the first match is found.

                #ccn = re.search(r"(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}", row_string) # Regex for mastercard
                #ccn = re.findall(r"\b\d{13,16}\b", row_string) # Regex format for any sequence of digits with length {13-16}
                
                                   # Matching condition VISA   |  	                       # Matching condition Master Card            	            | # American Express
                ccn = re.findall(r"\b(?:4[0-9]{12}(?:[0-9]{3})?|(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}|3[47][0-9]{13})\b", row_string) # VISA | Mastercard | American Express
                ccn_indecies = [index for index,item in enumerate(row) if item in ccn]
                field_names=[]
                for i in ccn_indecies:
                    field_names.append(first_row[i])
                #print (ccn)
                if len(ccn) != 0:
                    ccn_found = True
                    # Luhn Algorithm check
                    for credit_card_num in ccn:
                        total_sum = 0 # declare a variable called sum to store the sum in it
                        digit = 0 # declare a variable called digit to split a number if it consists of two digits
                        f_2digits = 0 # declare a variable to get the first two values of the credit-card number
                        credit_card_num = credit_card_num.strip(" ") # remove whitespaces
                        length = len(credit_card_num) # this block of code calculates length of credit-card number
                        number = int(credit_card_num) # Convert CC Number to int to perform calculations on it

                        # this block of code represents luhn's algorithm
                        for i in range(length):
                            # take sum of the numbers outside luhn's algorithm
                            if (i % 2 == 0):
                                total_sum += number % 10
                                number = int(number / 10)
                            # take sum of the numbers envolved in luhn's algorithm
                            if (i % 2 != 0):
                                digit = (number % 10) * 2
                                # divide two-digit number into two separate numbers
                                while (digit > 0):
                                    total_sum += digit % 10
                                    digit = int(digit / 10)
                                number = int(number / 10)
                            # grab the first two values from the left of the credit-card number
                            if (i == length - 3):
                                f_2digits = number

                        if (total_sum % 10 == 0): # If we entered this condition then luhn check is valid

                            if ccn_found == True and f_name_printed == False :
                                print ("File Name:", file)
                                f_name_printed = True
                            print ("********")
                            print ("[*] Credit card was found:", ccn," at Field Names:",field_names)
                            os.system ("mkdir -p filter_cdd_scan_results_test")
                            os.system ("cp " + file + " filter_cdd_scan_results")

                            # determine the type of the credit-card
                            if (length == 15 and (f_2digits == 34 or f_2digits == 37)):
                                print("Luhn Check: PASS    CC_Type: AMEX")
                            elif (length == 16 and (f_2digits >= 51 and f_2digits <= 55)):
                                print("Luhn Check: PASS    CC_Type: MASTERCARD")
                            elif ((length == 13 or length == 16) and (int(f_2digits / 10) == 4)):
                                print("Luhn Check: PASS    CC_Type: VISA")
                            else:
                                print("Luhn Check: PASS    CC_Type: N/A")

                            print ("[*] Row Number:", row_number)
                        else:
                            if ccn_found == True and f_name_printed == False :
                                print ("File Name:", file)
                                f_name_printed = True
                            print ("********")
                            print ("[*] Credit card was found:", ccn)
                            print ("[!] Luhn Check: FAILED        INVALID CC")
                            print ("[*] Row Number:", row_number)
                            os.system ("mkdir -p filter_cdd_scan_results")
                            os.system ("cp "+ file + " filter_cdd_scan_results")


        if ccn_found == True :
            print ("----------------------------------------")

        #if ccn_found == False:
            #print ("[!] No Credit Card Number were found!")


