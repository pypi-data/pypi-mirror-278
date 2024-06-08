# models/target.py
from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, Boolean, Enum, DateTime, func, BigInteger
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.schema import MetaData
from sqlalchemy.ext.declarative import declarative_base

from carbon_registry_indexer.models.enums import CorrespondingAdjustmentDeclaration, CorrespondingAdjustmentStatus, Countries, CoveredByNDC, LabelType, Methodology, ProjectSector, ProjectStatusValues, ProjectType, Registries, SustainableDevelopmentGoals, UnitMetric, UnitStatus

# Define your schema name here

Base = declarative_base()

# Project Location
class ProjectLocation(Base):
    __tablename__ = 'project_location'
    created_ts = Column(DateTime, nullable=False, server_default=func.now())
    updated_ts = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    cmhq_project_id = Column(String, ForeignKey('projects.cmhq_project_id'))
    country = Column(Enum(Countries))
    state = Column(String)
    project_location_id = Column(String, primary_key=True)
    in_country_region = Column(String)
    geographic_identifier = Column(String)

# Project Rating
class ProjectRating(Base):
    __tablename__ = 'project_rating'
    created_ts = Column(DateTime, nullable=False, server_default=func.now())
    updated_ts = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    cmhq_project_id = Column(String, ForeignKey('projects.cmhq_project_id'), primary_key=True)
    rating_type = Column(String)
    rating_range_lowest = Column(Integer)
    rating_range_highest = Column(Integer)
    rating = Column(Integer)
    rating_link = Column(String)

# Co-Benefits
class CoBenefit(Base):
    __tablename__ = 'co_benefits'
    created_ts = Column(DateTime, nullable=False, server_default=func.now())
    updated_ts = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    cmhq_project_id = Column(String, ForeignKey('projects.cmhq_project_id'))
    co_benefit_id = Column(String, primary_key=True)
    co_benefit = Column(Enum(SustainableDevelopmentGoals))

# Projects
class Project(Base):
    __tablename__ = 'projects'
    created_ts = Column(DateTime, nullable=False, server_default=func.now())
    updated_ts = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    cmhq_project_id = Column(String, primary_key=True)
    cadt_project_id = Column(String)
    project_id = Column(String)
    current_registry = Column(Enum(Registries))
    registry_of_origin = Column(Enum(Registries))
    program = Column(String)
    project_name = Column(String)
    project_description = Column(String)
    project_link = Column(String)
    project_developer = Column(String)
    sector = Column(Enum(ProjectSector))
    project_type = Column(Enum(ProjectType))
    project_tags = Column(JSONB)
    covered_by_ndc = Column(Enum(CoveredByNDC))
    ndc_information = Column(String)
    project_status = Column(Enum(ProjectStatusValues))
    project_status_date = Column(Date)
    unit_metric = Column(Enum(UnitMetric))
    methodology = Column(Enum(Methodology))
    validation_body = Column(String)
    validation_date = Column(Date)
    compliance_program_status = Column(String)
    compliance_program_id = Column(String)

    related_projects = relationship("RelatedProject", backref="project")
    issuances = relationship("Issuance", backref="project")
    labels = relationship("Label", backref="project")
    co_benefits = relationship("CoBenefit", backref="project")
    project_location = relationship("ProjectLocation", backref="project")
    project_rating = relationship("ProjectRating", backref="project")
    estimations = relationship("Estimation", backref="project") 
    
# Related Projects
class RelatedProject(Base):
    __tablename__ = 'related_projects'
    created_ts = Column(DateTime, nullable=False, server_default=func.now())
    updated_ts = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    cmhq_project_id = Column(String, ForeignKey('projects.cmhq_project_id'), primary_key=True)
    related_project_id = Column(Integer)
    relationship_type = Column(String)
    registry = Column(String)

# Issuances
class Issuance(Base):
    __tablename__ = 'issuances'
    created_ts = Column(DateTime, nullable=False, server_default=func.now())
    updated_ts = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    cmhq_project_id = Column(String, ForeignKey('projects.cmhq_project_id'))
    issuance_id = Column(String, primary_key=True)
    issuance_start_date = Column(Date)
    issuance_end_date = Column(Date)
    vintage_year = Column(Integer)
    verification_approach = Column(String)
    verification_report_date = Column(Date)
    verification_body = Column(String)
    units = relationship("Unit", backref="issuance")

# Labels
class Label(Base):
    __tablename__ = 'labels'
    created_ts = Column(DateTime, nullable=False, server_default=func.now())
    updated_ts = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    cmhq_project_id = Column(String, ForeignKey('projects.cmhq_project_id'))
    label_id = Column(String, primary_key=True)
    label_type = Column(Enum(LabelType))
    label = Column(String)
    crediting_period_start_date = Column(Date)
    crediting_period_end_date = Column(Date)
    validity_start_date = Column(Date)

# Units
class Unit(Base):
    __tablename__ = 'units'
    created_ts = Column(DateTime, nullable=False, server_default=func.now())
    updated_ts = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    issuance_id = Column(String, ForeignKey('issuances.issuance_id'))
    unit_name = Column(String)
    cmhq_unit_id = Column(String, primary_key=True)
    cadt_unit_id = Column(String)
    unit_issuance_location = Column(String)
    label_id = Column(String, ForeignKey('labels.label_id'))
    unit_owner = Column(String)
    country_jurisdiction_of_owner = Column(String)
    in_country_jurisdiction_of_owner = Column(String)
    unit_block_start = Column(String)
    unit_block_end = Column(String)
    unit_count = Column(BigInteger)
    vintage_year = Column(Integer)
    unit_type = Column(String)
    marketplace = Column(String)
    marketplace_link = Column(String)
    marketplace_identifier = Column(String)
    unit_tags = Column(JSONB)
    unit_status = Column(Enum(UnitStatus))
    unit_status_reason = Column(String)
    unit_registry_link = Column(String)
    corresponding_adjustment_declaration = Column(Enum(CorrespondingAdjustmentDeclaration))
    corresponding_adjustment_status = Column(Enum(CorrespondingAdjustmentStatus))
    issuance_date = Column(Date)
    last_status_update = Column(Date)
    unit_status_time = Column(Date)
    buffer_count = Column(Integer)

# Governance
class Governance(Base):
    __tablename__ = 'governance'
    created_ts = Column(DateTime, nullable=False, server_default=func.now())
    updated_ts = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    # Define columns for governance picklist values
    governance_id = Column(String, primary_key=True)
    value = Column(String)

# Estimations
class Estimation(Base):
    __tablename__ = 'estimations'
    created_ts = Column(DateTime, nullable=False, server_default=func.now())
    updated_ts = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
    cmhq_project_id = Column(String, ForeignKey('projects.cmhq_project_id'))
    estimation_id = Column(String, primary_key=True)
    crediting_period_start = Column(Date)
    crediting_period_end = Column(Date)
    unit_count = Column(BigInteger)
    validity_end_date = Column(Date)
    unit_quantity = Column(Integer)
    label_link = Column(String)

