import os

print(os.getcwd())

# Provides working directory.

reference = input('Name of File containing reference sequence (DNA/Protein) in FASTA format:')

with open(reference, 'r') as f:
    file_data = f.read()

file_data = "".join([i for i in file_data if i.isalpha()])

file_data = file_data.upper()

# Reads fasta file containing reference sequence and converts it into a continuous sting with no special characters, all upper case.

bearing_4 = file_data.find('SEQUENCE') + len('SEQUENCE')
file_data = file_data[bearing_4: len(file_data)]

# Cuts first line off (containing strain info etc).

SOI = input('Name of file containing sequence of gene of interest include file extension (.gff/.gb/.fasta):')
start = len(SOI) - 2
end = len(SOI)
file_type = SOI[start:end]
switch = 0
if file_type == 'gb':
    switch = 1
if file_type == 'ff':
    switch = 2

# Takes name of file containing protein/DNA sequence of gene (.fasta/.gb/.gff).
# Determines file extension based on last two characters of file name. Value of switch is changed accordingly to allow for relevant extraction operation.

with open(SOI,'r') as z:
    target = z.read()

target = "".join([i for i in target if i.isalnum()])

# File containing protein/DNA sequence of gene is read and converted into continuous string with all special characters and numbers removed.

if file_type == 'ta':
    bearing_5 = target.find('sequence') + len('sequence')
    target = target[bearing_5: len(target)]
    print(target[0:1000])

# If file extension is .fasta, first line is cut off.

if switch == 1:
    locus_tag = input('Please paste locus tag here:')
    locus_tag = "".join([i for i in locus_tag if i.isalnum()])
    bearing_1 = target.find(locus_tag)
    target = target[bearing_1:len(target)]
    bearing_2 = target.find('translation') + len('translation')
    target = target[bearing_2:len(target)]
    bearing_3 = target.find('gene')
    target = target[0:bearing_3]
    print(target)
    switch = 0
elif switch == 2:
    gene_id = input('Please paste gene id here:')
    bearing_1 = target.find(gene_id)
    target = target[bearing_1:len(target)]
    desired_info = input('Would you like to extract DNA or PROTEIN data?:')
    if desired_info == 'DNA':
        bearing_2 = target.find('codingsequence') + len('codingsequence')
        target = target[bearing_2:len(target)]
        bearing_3 = target.find('proteinsequence')
        target = target[0:bearing_3]
        target = target.upper()
        print(target)
        switch = 0
    else:
        bearing_2 = target.find('proteinsequence') + len('proteinsequence')
        target = target[bearing_2:len(target)]
        bearing_3 = target.find('endgene')
        target = target[0:bearing_3]
        print(target)
        switch = 0

# Operations for data extraction from .gb and .gff files, respectively. Locus tag/ gene id is used to navigate to relevant region.
# All of the string prior to that is essentially chopped off. Relevant code word e.g. 'proteinsequence' is then used to navigate to
# relevant region. Everything after that code word until a second code word e.g. 'end gene' is extracted. 

if switch == 0:
    target = target.upper()
    for i in range(len(file_data)-(len(target) - 1)):
        x = file_data[i]
        if file_data[i:i + len(target)] == target:
            if i >= 499:
                h = 500
            else:
                h = i
            match = file_data[i - h:i + len(target) + 500]
            print(i)
            print(len(match))
            print(match)
            print(len(match) - len(target))
            print('Done')

# Mapping: A for loop iterates over the reference sequence using a window of equal length to the gene sequence.
# Any matches are returned. 
