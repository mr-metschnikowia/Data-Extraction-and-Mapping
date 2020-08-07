import os
print(os.getcwd())

# Provides working directory.

import xlrd

def find_column():
    loc = (input(r'Please enter file path of .xlsx file containing locus tag/gene id data:'))
    wb = xlrd.open_workbook(loc)
    global sheet
    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0,0)
    for i in range(sheet.ncols):
        cell = sheet.cell_value(0, i)
        cell = "".join([i for i in cell if i.isalnum()])
        cell = cell.upper()
        if cell == 'GENEID':
            global column
            column = i
        elif cell == 'LOCUSTAG':
            column = i
        else:
            continue

def read_column():
    global id_tag_list
    id_tag_list = []
    for i in range(sheet.nrows):
        cell = sheet.cell_value(i,column)
        cell = "".join([i for i in cell if i.isalnum()])
        id_tag_list.append(cell)
    id_tag_list = id_tag_list[1:len(id_tag_list)]

# find_column function uses xldr module to iterate through columns and find one containing gene ids/locus tags.
# read_column function iterates through rows of column found by find_column, storing value of each cell in id_tag_list list.

reference = input('Name of File containing reference sequence (DNA/Protein) in FASTA format:')

with open(reference, 'r') as f:
    file_data = f.read()

file_data = "".join([i for i in file_data if i.isalpha()])

file_data = file_data.upper()

# Reads fasta file containing reference sequence and converts it into a continuous sting with no special characters, all upper case.

if file_data.find('SEQUENCE') >= 0:
    bearing_4 = file_data.find('SEQUENCE') + len('SEQUENCE')
    file_data = file_data[bearing_4: len(file_data)]

# Cuts first line off of .fasta reference sequence (containing strain info etc).

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

# File containing protein/DNA sequence(s) of gene(s) of interest is read and converted into continuous string with all special characters and numbers removed.

if file_type == 'ta':
    bearing_5 = target.find('sequence') + len('sequence')
    target = target[bearing_5: len(target)]

# If file extension is .fasta, first line is cut off.

if switch == 1:
    find_column()
    read_column()
    prot_seqs = []
    for i in range(len(id_tag_list)):
        locus_tag = id_tag_list[i]
        bearing_1 = target.find(locus_tag)
        chunk = target[bearing_1:len(target)]
        bearing_2 = chunk.find('translation') + len('translation')
        chunk = chunk[bearing_2:len(chunk)]
        bearing_3 = chunk.find('gene')
        chunk = chunk[0:bearing_3]
        prot_seqs.append(chunk)
        switch = 0
elif switch == 2:
    find_column()
    read_column()
    prot_seqs = []
    DNA_seqs = []
    desired_info = input('Would you like to extract DNA or PROTEIN data?:')
    for i in range(len(id_tag_list)):
        gene_id = id_tag_list[i]
        bearing_1 = target.find(gene_id)
        chunk = target[bearing_1:len(target)]
        if desired_info == 'DNA':
            bearing_2 = chunk.find('codingsequence') + len('codingsequence')
            chunk = chunk[bearing_2:len(chunk)]
            bearing_3 = chunk.find('proteinsequence')
            chunk = chunk[0:bearing_3]
            chunk = chunk.upper()
            DNA_seqs.append(chunk)
            switch = 0
        else:
            bearing_2 = chunk.find('proteinsequence') + len('proteinsequence')
            chunk = chunk[bearing_2:len(chunk)]
            bearing_3 = chunk.find('endgene')
            chunk = chunk[0:bearing_3]
            prot_seqs.append(chunk)
            switch = 0

# Operations for data extraction from .gb and .gff files, respectively. Locus tags/gene ids are pulled from .xlsx file using find + read_column functions.
# Locus tags/gene ids are used to navigate to relevant section of .gb/.gff file.
# Protein/DNA sequence data is extracted (specified by user) for each tag/id and is stored in prot_seqs/DNA_seqs list.

o = 0

if switch == 0:
    if file_type == 'gb' or file_type == 'ff' and desired_info == 'PROTEIN':
        prot_seq_match = []
        matched_ids_tags = []
        key_list = []
        for i in range(len(prot_seqs)):
            p = prot_seqs[i]
            p = p.upper()
            for i in range(len(file_data)-(len(p) - 1)):
                x = file_data[i]
                if file_data[i:i + len(p)] == p:
                    if i >= 499:
                        h = 500
                    else:
                        h = i
                    match = file_data[i - h:i + len(p) + 500]
                    prot_seq_match.append(match)
                    matched_ids_tags.append(id_tag_list[o])
            o += 1
        result = dict(zip(matched_ids_tags, prot_seq_match))
        print('Done')
        for key in result:
            key_list.append(key)
        print(key_list)
    elif file_type == 'ff' and desired_info == 'DNA':
        matched_ids_tags = []
        DNA_seq_match = []
        key_list = []
        for i in range(len(DNA_seqs)):
            d = DNA_seqs[i]
            d = d.upper()
            for i in range(len(file_data) - (len(d) - 1)):
                x = file_data[i]
                if file_data[i:i + len(d)] == d:
                    if i >= 499:
                        h = 500
                    else:
                        h = i
                    match = file_data[i - h:i + len(d) + 500]
                    DNA_seq_match.append(match)
                    matched_ids_tags.append(id_tag_list[o])
            o += 1
        result = dict(zip(matched_ids_tags, DNA_seq_match))
        print('Done')
        for key in result:
            key_list.append(key)
        print(key_list)
    else:
        target = "".join([i for i in target if i.isalpha()])
        target = target.upper()
        for i in range(len(file_data) - (len(target) - 1)):
            x = file_data[i]
            if file_data[i:i + len(target)] == target:
                match = file_data[i - 500:i + len(target) + 500]
                if i >= 499:
                    h = 500
                else:
                    h = i
                match = file_data[i - h:i + len(target) + 500]
                print('Done')
                print(match)

# Mapping: For .gb and .gff files, a loop is used to iterate through list storing extracted DNA/protein sequence data.
# Each item in the list is mapped onto the .fasta reference sequence.
# Any matches are returned with + 500 characters either side and are stored in the prot_seq_match/DNA_seq_match list.
# Variable o is used to keep track of id/tag currently being mapped. Successfully mapped tags/ids are appended to matched_ids_tags list.
# Matched_ids_tags and prot_seq_match/DNA_seq_match lists are zipped together to form a dictionary reflecting successfully mapped tags/ids.
# Keys are appended to a list, which is printed.
# For .fasta files, the sequence is simply mapped onto the reference and a match is returned with + 500 characters either side.
