from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.modules.categories import repository
from app.modules.categories.schemas import (
    CategoryCreate,
    CategoryOut,
    CategoryUpdate,
)

router = APIRouter(prefix="/categories", tags=["categories"])

DBSession = Annotated[AsyncSession, Depends(get_db)]


@router.get("/", response_model=list[CategoryOut])
async def list_categories(db: DBSession):
    categories = await repository.get_categories(db)
    return categories


@router.post("/", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
async def create_category_endpoint(data: CategoryCreate, db: DBSession):
    existing = await repository.get_category_by_slug(db, data.slug)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Slug already exists",
        )
    category = await repository.create_category(db, data)
    return category


@router.get("/{category_id}", response_model=CategoryOut)
async def get_category(category_id: int, db: DBSession):
    category = await repository.get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Category not found")
    return category


@router.patch("/{category_id}", response_model=CategoryOut)
async def update_category_endpoint(
    category_id: int,
    data: CategoryUpdate,
    db: DBSession,
):
    category = await repository.get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Category not found")
    category = await repository.update_category(db, category, data)
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category_endpoint(category_id: int, db: DBSession):
    category = await repository.get_category_by_id(db, category_id)
    if not category:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Category not found")
    await repository.delete_category(db, category)