from typing import List

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@app.get("/genes/{gene_name}", response_model=schemas.Gene, tags=["genes"])
def read_gene(gene_name: str, db: Session = Depends(get_db)):
    return crud.get_gene_by_name(db, gene_name)


@app.get("/genes/search/{regex}", response_model=List[schemas.Gene], tags=["genes"])
def read_gene(regex: str, db: Session = Depends(get_db)):
    return crud.get_gene_by_regex(db, regex)

@app.get("/genesets/limit={limit}&offset={offset}", response_model=List[schemas.Geneset], tags=["genesets"])
def read_all_genesets(limit: int, offset: int, db: Session = Depends(get_db)):
    genesets = crud.get_genesets(db, offset, limit)
    return genesets

@app.get("/genesets/search/{pattern}", response_model=List[schemas.Geneset], tags=["genesets"])
def read_match_genesets(pattern: str, db: Session = Depends(get_db)):
    genesets = crud.get_geneset_by_title(db, pattern)
    return genesets


@app.get("/genesets/{geneset_id}", response_model=schemas.Geneset, tags=["genesets"])
def read_geneset(geneset_id: int, db: Session = Depends(get_db)):
    return crud.get_geneset(db, geneset_id)


@app.put("/genesets/{geneset_id}", response_model=schemas.Geneset, tags=["genesets"])
def update_genesets(geneset_id: int, geneset: schemas.GenesetCreate, db: Session = Depends(get_db)):
    return crud.update_geneset(db, geneset_id, geneset.title, geneset.genes)


@app.post("/genesets", tags=["genesets"])
def create_geneset(geneset: schemas.GenesetCreate, db: Session = Depends(get_db)):
    print(geneset)
    db_geneset = crud.create_geneset_with_genes(db, geneset)
    return db_geneset.id

