import os

print(os.getcwd())

reference = input('Name of File containing reference sequence (DNA/Protein) in FASTA format:')

with open(reference, 'r') as f:
    file_data = f.read()

file_data = "".join([i for i in file_data if i.isalpha()])

file_data = file_data.upper()

SOI = input('Name of file containing sequence of gene of interest include file extension (.gff/.gb/.fasta):')
start = len(SOI) - 2
end = len(SOI)
file_type = SOI[start:end]
switch = 0
if file_type == 'gb':
    switch = 1
if file_type == 'ff':
    switch = 2

with open(SOI,'r') as z:
    target = z.read()

target = "".join([i for i in target if i.isalnum()])

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

if switch == 0:
    for i in range(len(file_data)-(len(target) - 1)):
        x = file_data[i]
        if file_data[i:i + len(target)] == target:
            match = file_data[i - 500:i + len(target) + 500]
            print(match)
            print(len(match) - len(target))
            print('Done')
