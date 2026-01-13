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


class Molecule(NmrXivBase):
    """Molecule model from nmrxiv search API."""

    id: int
    molecular_formula: Optional[str] = None
    molecular_weight: Optional[float] = None
    canonical_smiles: Optional[str] = None
    inchi: Optional[str] = None
    standard_inchi: Optional[str] = None
    inchi_key: Optional[str] = None
    standard_inchi_key: Optional[str] = None
    iupac_name: Optional[str] = None
    synonyms: Optional[str] = None
    cas: Optional[str] = None
    identifier: Optional[int] = None


class ListResponse(NmrXivBase):
    """Generic list response wrapper."""

    items: list[Any]
    count: int
    type: str


class PaginatedResponse(NmrXivBase):
    """Paginated response with metadata."""

    items: list[Any]
    total: int
    page: int
    per_page: int
    last_page: int
