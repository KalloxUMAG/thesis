from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.schema import ForeignKey
from sqlalchemy.orm import relationship
from scripts.db_conn.database import Base
from datetime import datetime

# Tablas independientes


class Aa_interaction(Base):
    __tablename__ = "aa_interaction"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    score = Column(Float)
    type = Column(String)

    database_id = Column(Integer, ForeignKey("database.id", ondelete="SET NULL"))

    antibodies = relationship(
        "Antibody",
        secondary="antibody_has_aa_interaction",
        back_populates="aa_interactions",
    )

    def __str__(self):
        return self.id


class Antibody(Base):
    __tablename__ = "antibody"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    pdb = Column(String)

    antibody_chains = relationship("Antibody_chain", backref="antibody")
    antigens = relationship(
        "Antigen", secondary="interaction", back_populates="antibodies"
    )
    databases = relationship(
        "Database", secondary="antibody_has_database", back_populates="antibodies"
    )
    aa_interactions = relationship(
        "Aa_interaction",
        secondary="antibody_has_aa_interaction",
        back_populates="antibodies",
    )

    def __str__(self):
        return self.name


class Antigen(Base):
    __tablename__ = "antigen"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    sequence = Column(String)
    length = Column(Integer)
    ss3 = Column(String)
    ss8 = Column(String)
    diso = Column(String)
    acc = Column(String)
    tm2 = Column(String)
    tm8 = Column(String)
    pdb = Column(String)

    antibodies = relationship(
        "Antibody", secondary="interaction", back_populates="antigens"
    )
    databases = relationship(
        "Database", secondary="antigen_has_database", back_populates="antigens"
    )
    epitopes = relationship(
        "Epitope", secondary="antigen_has_epitope", back_populates="antigens"
    )
    gene_ontologys = relationship(
        "Gene_ontology", secondary="antigen_has_go", back_populates="antigens"
    )
    pfams = relationship(
        "Pfam", secondary="antigen_has_pfam", back_populates="antigens"
    )

    def __str__(self):
        return self.name


class Chain_type(Base):
    __tablename__ = "chain_type"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    antibody_chains = relationship("Antibody_chain", backref="chain_type")

    def __str__(self):
        return self.name


class Database(Base):
    __tablename__ = "database"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    antibodies = relationship(
        "Antibody", secondary="antibody_has_database", back_populates="databases"
    )
    antigens = relationship(
        "Antigen", secondary="antigen_has_database", back_populates="databases"
    )
    epitopes = relationship(
        "Epitope", secondary="epitope_has_database", back_populates="databases"
    )

    interaction = relationship("Interaction", backref="database")
    aa_interaction = relationship("Aa_interaction", backref="database")

    def __str__(self):
        return self.name


class Epitope_type(Base):
    __tablename__ = "epitope_type"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    epitopes = relationship("Epitope", backref="epitope_type")

    def __str__(self):
        return self.name


class Gene_ontology(Base):
    __tablename__ = "gene_ontology"

    id = Column(Integer, primary_key=True, autoincrement=True)
    accession = Column(String)
    term = Column(String)
    type = Column(String)

    antigens = relationship(
        "Antigen", secondary="antigen_has_go", back_populates="gene_ontologys"
    )

    def __str__(self):
        return self.id


class Pfam(Base):
    __tablename__ = "pfam"

    id = Column(Integer, primary_key=True, autoincrement=True)
    accession = Column(String)
    term_class = Column(String)

    antigens = relationship(
        "Antigen", secondary="antigen_has_pfam", back_populates="pfams"
    )

    def __str__(self):
        return self.id


class Vdj(Base):
    __tablename__ = "vdj"

    id = Column(Integer, primary_key=True, autoincrement=True)
    v = Column(String)
    d = Column(String)
    j = Column(String)

    antibody_chains = relationship("Antibody_chain", backref="vdj")

    def __str__(self):
        return self.v


# Tablas dependientes


class Antibody_chain(Base):
    __tablename__ = "antibody_chain"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    sequence = Column(String)
    length = Column(Integer)
    ss3 = Column(String)
    ss8 = Column(String)

    antibody_id = Column(Integer, ForeignKey("antibody.id", ondelete="SET NULL"))
    chain_type_id = Column(Integer, ForeignKey("chain_type.id", ondelete="SET NULL"))
    vdj_id = Column(Integer, ForeignKey("vdj.id", ondelete="SET NULL"))

    def __str__(self):
        return self.name


class Epitope(Base):
    __tablename__ = "epitope"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    sequence = Column(String)

    epitope_type_id = Column(
        Integer, ForeignKey("epitope_type.id", ondelete="SET NULL")
    )
    databases = relationship(
        "Database", secondary="epitope_has_database", back_populates="epitopes"
    )
    antigens = relationship(
        "Antigen", secondary="antigen_has_epitope", back_populates="epitopes"
    )

    def __str__(self):
        return self.name


# Relaciones (M -> N)


class Antibody_has_database(Base):
    __tablename__ = "antibody_has_database"

    antibody_id = Column(Integer, ForeignKey("antibody.id"), primary_key=True)
    database_id = Column(Integer, ForeignKey("database.id"), primary_key=True)
    accession = Column(String, default=datetime.now(), onupdate=datetime.now)


class Antibody_has_aa_interaction(Base):
    __tablename__ = "antibody_has_aa_interaction"

    antibody_id = Column(Integer, ForeignKey("antibody.id"), primary_key=True)
    aa_interaction_id = Column(
        Integer, ForeignKey("aa_interaction.id"), primary_key=True
    )


class Antigen_has_database(Base):
    __tablename__ = "antigen_has_database"

    antigen_id = Column(Integer, ForeignKey("antigen.id"), primary_key=True)
    database_id = Column(Integer, ForeignKey("database.id"), primary_key=True)
    accession = Column(String, default=datetime.now(), onupdate=datetime.now)


class Antigen_has_epitope(Base):
    __tablename__ = "antigen_has_epitope"

    antigen_id = Column(Integer, ForeignKey("antigen.id"), primary_key=True)
    epitope_id = Column(Integer, ForeignKey("epitope.id"), primary_key=True)


class Antigen_has_go(Base):
    __tablename__ = "antigen_has_go"

    antigen_id = Column(Integer, ForeignKey("antigen.id"), primary_key=True)
    go_id = Column(Integer, ForeignKey("gene_ontology.id"), primary_key=True)
    probability = Column(Integer)


class Antigen_has_pfam(Base):
    __tablename__ = "antigen_has_pfam"

    antigen_id = Column(Integer, ForeignKey("antigen.id"), primary_key=True)
    pfam_id = Column(Integer, ForeignKey("pfam.id"), primary_key=True)
    e_value = Column(Integer)


class Epitope_has_database(Base):
    __tablename__ = "epitope_has_database"

    epitope_id = Column(Integer, ForeignKey("epitope.id"), primary_key=True)
    database_id = Column(Integer, ForeignKey("database.id"), primary_key=True)
    accession = Column(String, default=datetime.now(), onupdate=datetime.now)


class Interaction(Base):
    __tablename__ = "interaction"

    antibody_id = Column(Integer, ForeignKey("antibody.id"), primary_key=True)
    antigen_id = Column(Integer, ForeignKey("antigen.id"), primary_key=True)
    score = Column(Float)
    database_id = Column(Integer, ForeignKey("database.id", ondelete="SET NULL"))
