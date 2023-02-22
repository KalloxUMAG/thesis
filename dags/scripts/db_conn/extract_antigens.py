def extract_json_uniprot(protein):
    uniProtkbId = ""
    primaryAccession = ""
    proteinName = ""
    sequence = ""
    pdb = []

    if protein["entryType"] == "Inactive":
        return {}
    if (
        "proteinDescription" in protein
        and "recommendedName" in protein["proteinDescription"]
    ):
        if "fullName" in protein["proteinDescription"]["recommendedName"]:
            proteinName = protein["proteinDescription"]["recommendedName"]["fullName"][
                "value"
            ]

    uniProtkbId = protein["uniProtkbId"]
    primaryAccession = protein["primaryAccession"]

    if "sequence" in protein:
        sequence = protein["sequence"]["value"]

    if "uniProtKBCrossReferences" in protein:
        for database in protein["uniProtKBCrossReferences"]:
            if database["database"] == "PDB":
                pdb.append(database["id"])

    name = proteinName + "||" + uniProtkbId + " || " + primaryAccession

    return {
        "name": name,
        "sequence": sequence,
    }


# Pensado para KEGG
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
