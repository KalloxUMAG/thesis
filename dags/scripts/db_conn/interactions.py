from scripts.db_conn.models import Interaction, Aa_interaction, Antibody_has_aa_interaction
from scripts.db_conn.load_databases import get_database_id
from sqlalchemy import or_

def interaction_exist(antibody_id, antigen_id, db):
    data = (
        db.query(Interaction.antigen_id, Interaction.antibody_id)
        .filter(
            Interaction.antibody_id == antibody_id, Interaction.antigen_id == antigen_id
        )
        .first()
    )
    if data == None:
        return -1
    return data[0]

def ab_interaction_exist(antibody1_id, antibody2_id, db):
    if antibody1_id < antibody2_id:
        name = f"{antibody1_id}-{antibody2_id}"
    else:
        name = f"{antibody2_id}-{antibody1_id}"
    data = db.query(Aa_interaction.id).filter(Aa_interaction.name == name).first()
    if data == None:
        return -1
    return data[0]

