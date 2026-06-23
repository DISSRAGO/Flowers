from __future__ import annotations

from pydantic import BaseModel


class CategoryBase(BaseModel):
    slug: str
    name: str
    description: str | None = None
    is_active: bool = True
    sort_order: int = 0


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None
    sort_order: int | None = None


class CategoryOut(CategoryBase):
    id: int

    class Config:
        from_attributes = True