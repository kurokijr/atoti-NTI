from __future__ import annotations

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class UeUnit(Base):
    __tablename__ = "ue_unit"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(str(50))

    def __repr__(self) -> str:
        return f"UeUnit(id={self.id!r}, name={self.name!r})"

class ProjectProjectUE(Base):
    _tablename__ = "project_project_ue"
    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("ProjectProject.id"))
    unit_id: Mapped[int] = mapped_column(ForeignKey("UeUnit.id"))

    def __repr__(self) -> str:
        return f"ProjectProjectUE(id={self.id!r}), project_id={self.project_id!r}, unit_id={self.unit_id!r}"

class ProjectProject(Base):
    __tablename__ = "project_project"
    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(str(15))
    project_type: Mapped[str] = mapped_column(str(200))
    final_maturity_level: Mapped[str] = mapped_column(str(200))
    status: Mapped[str] = mapped_column(str(200))
    def __repr__(self) -> str:
        return f"ProjectProject(id={self.id!r}), code={self.code!r}, project_type={self.project_type!r}, final_maturity_level={self.final_maturity_level!r}, status={self.status!r}"

class ProjectFinancingModality(Base):
    __tablename__ = "project_financingmodality"
    id: Mapped[int] = mapped_column(primary_key=True)
