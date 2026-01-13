"""Pydantic models for nmrxiv API responses."""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class NmrXivBase(BaseModel):
    """Base model with flexible parsing."""

    model_config = ConfigDict(extra="ignore")


class Project(NmrXivBase):
    """Project model from nmrxiv API."""

    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    identifier: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Study(NmrXivBase):
    """Study model from nmrxiv API."""

    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    sample_info: Optional[str] = None
    project_id: Optional[int] = None
    identifier: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Dataset(NmrXivBase):
    """Dataset model from nmrxiv API."""

    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    type: Optional[str] = None
    format: Optional[str] = None
    study_id: Optional[int] = None
    identifier: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ListResponse(NmrXivBase):
    """Generic list response wrapper."""

    items: list[Any]
    count: int
    type: str
