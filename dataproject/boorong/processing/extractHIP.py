
hipfilename="hipnumbers.txt"

numberslist=[]

# Open the file in read mode
with open(hipfilename, 'r') as file:
    # Read each line in the file
    for line in file:
        # Print each line
        for item in line.strip().split(" "):
            if len(item) > 3:
                if item not in numberslist:
                    numberslist.append(item)

print(numberslist)


outfilename="distincthipnumers.txt"
with open(outfilename, 'w') as file:
    for number in numberslist:
        string = f"HIP{number}\n"
        print(string)
        file.write(string)



