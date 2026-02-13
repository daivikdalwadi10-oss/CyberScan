from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas
from app.database import get_db

router = APIRouter(prefix="/risk", tags=["Risk"])

@router.post("/", response_model=schemas.RiskScoreOut)
def create_risk_score(score: schemas.RiskScoreCreate, db: Session = Depends(get_db)):
    db_score = models.RiskScore(**score.dict())
    db.add(db_score)
    db.commit()
    db.refresh(db_score)
    return db_score

@router.get("/", response_model=List[schemas.RiskScoreOut])
def list_risk_scores(db: Session = Depends(get_db)):
    return db.query(models.RiskScore).order_by(models.RiskScore.created_at.desc()).all()

@router.get("/latest", response_model=schemas.RiskScoreOut)
def get_latest_risk_score(db: Session = Depends(get_db)):
    score = db.query(models.RiskScore).order_by(models.RiskScore.created_at.desc()).first()
    if not score:
        raise HTTPException(status_code=404, detail="No risk score found")
    return score
