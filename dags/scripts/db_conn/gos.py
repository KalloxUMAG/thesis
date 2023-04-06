from scripts.db_conn.models import Antigen, Antigen_has_go, Gene_ontology
from scripts.db_conn.antigens import get_antigen_id

def get_go_id(go, db):
    accession = go['accession']
    term = go['term']
    type = go['type']

    data = db.query(Gene_ontology.id).filter(Gene_ontology.accession == accession).filter(Gene_ontology.term == term).filter(
        Gene_ontology.type == type).first()

    if data == None:
        return -1
    return data[0]

def antigen_has_go_exist(antigen_id, go_id, db):
    data = db.query(Antigen_has_go.antigen_id).filter(Antigen_has_go.antigen_id == antigen_id).filter(
        Antigen_has_go.go_id == go_id).first()
    if data == None:
        return False
    return True

def create_antigen_has_go_relation(go, db):
    antigen_id = get_antigen_id(go['antigen'])
    go_id = get_go_id(go)
    if antigen_has_go_exist(antigen_id, go_id):
        return
    new_antigen_has_go = Antigen_has_go(antigen_id = antigen_id, go_id = go_id, probability = go['probability'])
    db.add(new_antigen_has_go)
    db.commit()

def create_go(go, db):
    go_exists = get_go_id(go)
    if go_exists != -1:
        new_gene_ontology = Gene_ontology(accession = go['accession'], term = go['term'], type = go['type'])
        db.add(new_gene_ontology)
        db.commit()

    create_antigen_has_go_relation(go, db)
    