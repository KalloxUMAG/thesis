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