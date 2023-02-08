def extract_fasta(protein):
    protein = protein.content.decode("utf-8")
    protein_lines = protein.split("\n")
    if len(protein.lines) < 2:
        return {}

    name = protein_lines[0][1:].split(" | ")[0]
    name = name.split(" ", 1)
    name = " || ".join(name)
    sequence = "".join(protein_lines[1:])

    return {
        "name": name,
        "sequence": sequence,
    }

def extract_fasta_file(fasta_file, dataframe, separator, split_position):
    # Read in FASTA
    cols = dataframe.columns
    file = open(fasta_file, 'r')
    lines = file.readlines()
    i = 1
    id = ''
    sequence = ''
    for line in lines:
        if line[0] == '>':
            if i > 1:
                dataframe = dataframe.append({
                    cols[0] : id,
                    cols[1] : sequence
                }, ignore_index = True)
            id = ''
            sequence = ''
            linecontent = line[1:]
            linecontent = linecontent.split(separator)
            id = linecontent[split_position]
            i = i + 1
        elif len(line) > 0:
            linecontent = line[:-1]
            sequence = sequence + linecontent
            i = i + 1
    dataframe = dataframe.append({
                    cols[0] : id,
                    cols[1] : sequence
                }, ignore_index = True)
    file.close()
    return dataframe