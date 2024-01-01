from enum import Enum
from typing import List

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg
from models.base import BaseModel
from sqlalchemy import Column, Date, ForeignKey, Identity, Integer, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing_extensions import override


# These are example methodologies derived from:
# https://openstax.org/books/introduction-sociology-3e/pages/2-2-research-methods
class MethodologyType(Enum):
    SURVEY = 1
    FIELD_RESEARCH = 2
    PARTICIPANT_OBSERVATION = 3
    ETHNOGRAPHY = 4
    EXPERIMENT = 5
    SECONDARY_DATA_ANALYSIS = 6
    CASE_STUDY = 7


class PopulationType(Enum):
    POPULATION_1 = 1
    POPULATION_2 = 2
    POPULATION_3 = 3


class ResearchType(Enum):
    APPLIED_RESEARCH = 1
    EVALUATIVE_RESEARCH = 2
    PROGRAM_SUPPORT = 3


class ResearchProjectCANs(BaseModel):
    __tablename__ = "research_project_cans"

    research_project_id: Mapped[int] = mapped_column(
        ForeignKey("research_project.id"), primary_key=True
    )
    can_id: Mapped[int] = mapped_column(ForeignKey("can.id"), primary_key=True)

    @BaseModel.display_name.getter
    def display_name(self):
        return f"research_project_id={self.research_project_id};can_id={self.can_id}"


class ResearchProjectTeamLeaders(BaseModel):
    __tablename__ = "research_project_team_leaders"

    research_project_id: Mapped[int] = mapped_column(
        ForeignKey("research_project.id"), primary_key=True
    )
    team_lead_id: Mapped[int] = mapped_column(ForeignKey("user.id"), primary_key=True)

    @BaseModel.display_name.getter
    def display_name(self):
        return f"research_project_id={self.research_project_id};team_lead_id={self.team_lead_id}"


class ResearchProject(BaseModel):
    __tablename__ = "research_project"
    id = Column(Integer, Identity(), primary_key=True)
    title = Column(String, nullable=False)
    short_title = Column(String)
    description = Column(Text)
    url = Column(String)
    origination_date = Column(Date)
    methodologies = Column(
        pg.ARRAY(sa.Enum(MethodologyType)), server_default="{}", default=[]
    )
    populations = Column(
        pg.ARRAY(sa.Enum(PopulationType)), server_default="{}", default=[]
    )
    agreements = relationship("Agreement", back_populates="research_project")
    team_leaders = relationship(
        "User",
        back_populates="research_projects",
        secondary="research_project_team_leaders",
        primaryjoin="ResearchProject.id == ResearchProjectTeamLeaders.research_project_id",
        secondaryjoin="User.id == ResearchProjectTeamLeaders.team_lead_id",
    )

    cans: Mapped[List["CAN"]] = relationship(
        "CAN", secondary="research_project_cans", back_populates="research_projects"
    )

    @BaseModel.display_name.getter
    def display_name(self):
        return self.title
