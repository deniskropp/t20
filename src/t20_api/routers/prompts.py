from typing import List, Optional, Literal
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from t20_api.database import get_db
from t20_api import models

router = APIRouter(prefix="/prompts", tags=["prompts"])

@router.post("/", response_model=models.PromptResponse, status_code=status.HTTP_201_CREATED)
async def create_prompt(prompt: models.PromptCreate, db: AsyncSession = Depends(get_db)):
    # TAS 9: Type validation is handled by Pydantic, but we can enforce it here too just in case
    if prompt.type not in ["system", "session", "team", "task"]:
        raise HTTPException(status_code=400, detail="Invalid prompt type")
    
    db_prompt = models.Prompt(**prompt.model_dump())
    db.add(db_prompt)
    await db.commit()
    await db.refresh(db_prompt)
    return db_prompt

@router.get("/", response_model=List[models.PromptResponse])
async def list_prompts(
    type: Optional[Literal["system", "session", "team", "task"]] = None,
    limit: int = 100,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    query = select(models.Prompt)
    if type:
        query = query.where(models.Prompt.type == type)
    query = query.offset(offset).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

@router.get("/{prompt_id}", response_model=models.PromptResponse)
async def get_prompt(prompt_id: int, db: AsyncSession = Depends(get_db)):
    query = select(models.Prompt).where(models.Prompt.id == prompt_id)
    result = await db.execute(query)
    prompt = result.scalar_one_or_none()
    if not prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    return prompt

@router.put("/{prompt_id}", response_model=models.PromptResponse)
async def update_prompt(prompt_id: int, prompt_update: models.PromptUpdate, db: AsyncSession = Depends(get_db)):
    query = select(models.Prompt).where(models.Prompt.id == prompt_id)
    result = await db.execute(query)
    db_prompt = result.scalar_one_or_none()
    if not db_prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    update_data = prompt_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_prompt, key, value)
    
    await db.commit()
    await db.refresh(db_prompt)
    return db_prompt

@router.delete("/{prompt_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_prompt(prompt_id: int, db: AsyncSession = Depends(get_db)):
    query = select(models.Prompt).where(models.Prompt.id == prompt_id)
    result = await db.execute(query)
    db_prompt = result.scalar_one_or_none()
    if not db_prompt:
        raise HTTPException(status_code=404, detail="Prompt not found")
    
    await db.delete(db_prompt)
    await db.commit()
