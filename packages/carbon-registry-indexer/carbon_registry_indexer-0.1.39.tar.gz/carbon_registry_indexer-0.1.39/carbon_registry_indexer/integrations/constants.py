from carbon_registry_indexer.models import enums

CADT_FILE_NAME = "/cadt.xlsx"
GS_FILE_NAME = "/gs.xlsx"

PROJECTS_STORAGE_FILE_NAME = "projects"
ISSUANCES_STORAGE_FILE_NAME = "issuances"
PROJECT_LOCATIONS_STORAGE_FILE_NAME = "project_location"
ESTIMATIONS_STORAGE_FILE_NAME = "estimations"
CO_BENEFITS_STORAGE_FILE_NAME = "co_benefits"
LABELS_STORAGE_FILE_NAME = "labels"
UNITS_STORAGE_FILE_NAME = "units"
GOVERNANCE_STORAGE_FILE_NAME = "governance"
PROJECT_RATING_STORAGE_FILE_NAME = "project_rating"
RELATED_PROJECTS_STORAGE_FILE_NAME = "related_projects"

PROJECTS_SCHEMA_NAME = "Project"
ISSUANCES_SCHEMA_NAME = "Issuance"
PROJECT_LOCATIONS_SCHEMA_NAME = "ProjectLocation"
ESTIMATIONS_SCHEMA_NAME = "Estimation"
CO_BENEFITS_SCHEMA_NAME = "CoBenefit"
LABELS_SCHEMA_NAME = "Label"
UNITS_SCHEMA_NAME = "Unit"
GOVERNANCE_SCHEMA_NAME = "Governance"
PROJECT_RATING_SCHEMA_NAME = "ProjectRating"
RELATED_PROJECTS_SCHEMA_NAME = "RelatedProject"

JSON_FILES = [
    "/units_1.json",
    "/units_2.json",
    "/units_3.json",
    "/units_4.json",
    "/units_5.json",
    "/units_6.json",
]

GS_SHEET_NAMES = [
    "projects",
    "credits",
    "retirements",
]

sheets_to_tables = {
    "projects": "projects",
    "projectLocations": "project_location",
    "issuances": "issuances",
    "estimations": "estimations",
    "coBenefits": "co_benefits",
    "labels": "labels",
    "units": "units",
}

puro_projects_cols = {
    "Name": "project_name",
    "ID Number": "project_id",
    "Country": "country",
    "Method": "methodology",
}

puro_units_cols = {
    "Project name": "project_name",
    "ï»¿date": "last_status_update",
    "date": "last_status_update",
    "numberOfCredits": "unit_count",
    "Credit Type": "unit_type",
    "Beneficiary": "unit_owner",
    "Retirement purpose": "unit_status_reason",
    "Project country": "country_jurisdiction_of_owner",
}

puro_sheet_to_cols = {
    "/puro_projects.csv": puro_projects_cols,
    "/puro_retirements.csv": puro_units_cols,
}

art_projects_cols = {
    "Program ID" : "project_id",
    "Sovereign Program Developer": "project_developer",
    "Program Name": "project_name",
    "Verification Body": "validation_body",
    "Crediting Program and Standard": "methodology",
    "Program Type": "project_type",
    "Status": "project_status",
    "Program  Country": "country",
    "Program Jurisdiction(s)" : "in_country_region",
    "Program Website": "project_link",
}

art_project_tags_cols = {
    "Program Notes" : "project_tags",
}

art_units_issued_cols = {
    "Date Approved": "issuance_start_date",
    "Program ID" : "project_id",
    "Sovereign Program Developer": "unit_owner",
    "Vintage": "vintage_year",
    "Total Emission Reductions/Removals": "unit_count",
    "Credits Deposited in Buffer": "buffer_count",
}

art_unit_tags_cols = {
    "Eligible for CORSIA 2021-2023 Compliance Period (Pilot Phase)": "unit_tags",
    "Eligible for CORSIA 2024-2026 Compliance Period (First Phase)": "unit_tags",
    "CCP Approved": "unit_tags",
    "Standard Version": "unit_tags",
    "Account Holder": "unit_owner",
    "Retirement Reason Details": "unit_tags",
    "Date Approved": "unit_tags",
}

art_units_retired_cols = {
    "Program ID" : "project_id",
    "Vintage" : "vintage_year",
    "Quantity of Credits": "unit_count",
    "Status Effective" : "unit_status_time",
    "Retirement Reason": "unit_status_reason",
    "Cancellation Reason": "unit_status_reason",
}

art_sheet_to_cols = {
    "/art_projects.csv": art_projects_cols,
    "/art_credits_issued.csv": art_units_issued_cols,
    "/art_credits_retired.csv": art_units_retired_cols,
    "/art_credits_cancelled.csv": art_units_issued_cols,
}

acr_projects_cols = {
    "Project ID" : "project_id",
    "Project Name" : "project_name",
    "Project Developer" : "project_developer",
    "Current VVB": "validation_body",
    "Project Type" : "project_type",
    "Voluntary Status" : "project_status",
    "Project Site Country": "country",
    "Project Site Location": "in_country_region",
    "Project Site State": "state",
    "Project Status Date": "project_status_date",
    "Project Methodology/Protocol": "methodology",
    "Project Website": "project_link",
    "Compliance Program ID (ARB or Ecology)": "compliance_program_id",
    "Compliance Program Status (ARB or Ecology)" : "compliance_program_status",
}

acr_project_tags_cols = {
    'ACR Project Validation' : 'project_tags',
}


acr_units_issued_cols = {
    "Project ID" : "project_id",
    "Project Owner": "unit_owner",
    "Project Site Location": "unit_issuance_location",
    "Project Site Country": "country_jurisdiction_of_owner",
    "Vintage": "vintage_year",
    "Credits Issued to Project": "unit_count",
    "Credits Transferred to Buffer Pool" : "buffer_count",
    "Credits Issued to Buffer Pool" : "buffer_count",
    "Project VVB" : "verification_body",
    "Date Issued" : "unit_status_time",
    "Verified Removal": "unit_type",
    "Vintage Assignment Period Start Date" : "issuance_start_date",
    "Vintage Assignment Period End Date": "issuance_end_date",
}

acr_units_retired_cols = {
    "Project ID" : "project_id",    
    "Vintage": "vintage_year",
    "Account Holder": "unit_owner",
    "Project Site Location": "unit_issuance_location",
    "Project Site Country": "country_jurisdiction_of_owner",
    "Retirement Reason": "unit_status_reason",
    "Quantity of Credits": "unit_count",
    "Retirement Reason Details": "unit_tags",
    "Status Effective" : "unit_status_time",
    "Cancellation Type": "unit_status_reason",
    "Cancellation Details": "unit_tags",
}

acr_unit_tags_cols = {
    "Offset Credit Serial Numbers" : "unit_tags",
    "Credit Serial Numbers": "unit_tags",
    "Project Type": "unit_tags",
    "CORSIA Eligible": "unit_tags",
    "ARB Eligible": "unit_tags",
    "Ecology Eligible": "unit_tags",
    "Status": "unit_status",
} 

acr_sheet_to_cols = {
    "/acr_projects.csv": acr_projects_cols,
    "/acr_credits_issued.csv": acr_units_issued_cols,
    "/acr_credits_retired.csv": acr_units_retired_cols,
    "/acr_credits_cancelled.csv": acr_units_issued_cols,
}

car_projects_cols = {
    "Project ID" : "project_id",
    "Project Name" : "project_name",
    "Project Developer" : "project_developer",
    "Verification Body": "validation_body",
    "Project Type" : "project_type",
    "Status" : "project_status",    
    "Project Site Country": "country",
    "Project Site Location": "in_country_region",
    "ARB Project Status": "compliance_program_status",
    "ARB ID": "compliance_program_id",
    "Project Website": "project_link",
}

car_project_tags_cols = {
    'Project Notes' : 'project_tags',
    'Cooperative/ Aggregate ID': 'project_tags',
    'Project Owner' : 'project_tags',
    'Offset Project Operator': 'project_tags',
    'Authorised Project Designee': 'project_tags',
    'Additional Certification(s)': 'project_tags',
    'Documents': 'project_tags',
    'Date': 'project_tags',
}

car_units_issued_cols = {
    "Project ID" : "project_id",
    "Project Owner": "unit_owner",
    "Project Site Location": "unit_issuance_location",
    "Project Site Country": "country_jurisdiction_of_owner",
    "Vintage": "vintage_year",
    "Total Offset Credits Issued": "unit_count",
    "Date Issued" : "issuance_start_date",
    "Reduction/Removal": "unit_type",
    "Offset Credits Currently in Reserve Buffer Pool": "buffer_count",
    "Verification Body": "verification_body",
}

car_units_retired_cols = {
    "Project ID" : "project_id",
    "Vintage": "vintage_year",
    "Quantity of Offset Credits": "unit_count",
    "Account Holder": "unit_owner",
    "Project Site Location": "unit_issuance_location",
    "Project Site Country": "country_jurisdiction_of_owner",
    "Retirement Reason": "unit_status_reason",
    "Status Effective" : "unit_status_time",
}  

car_unit_tags_cols = {
    "Project Type": "unit_tags",
    "CORSIA Eligible": "unit_tags",
    "Status": "unit_status",
    "Offset Credits Intended for ARB Buffer Pool" : "unit_tags",
    "Offset Credits Converted to VCUs": "unit_tags",
    "Canceled for ARB Compliance": "unit_tags",
    "Canceled" : "unit_tags",
    "Retirement Reason Details": "unit_tags",
}

car_sheet_to_cols = {
    "/car_projects.csv": car_projects_cols,
    "/car_credits_issued.csv": car_units_issued_cols,
    "/car_credits_retired.csv": car_units_retired_cols,
    "/car_credits_cancelled.csv": car_units_issued_cols,
}

gs_projects_cols = {
    "GSID" : "project_id",
    "Project Name" : "project_name",
    "Project Developer Name" : "project_developer",
    "Status" : "project_status",
    "Project Type" : "project_type",
    "Description" : "project_description",
    "Methodology": "methodology",
    'Country': 'country',
}

gs_project_tags_cols = {
    "Size": "project_tags",
    "Programme of Activities": "project_tags",
    "POA GSID": "project_tags",
}

gs_issuances_cols = {
    "GSID" : "project_id",
    "Monitoring Period Start" : "issuance_start_date",
    "Monitoring Period End" : "issuance_end_date",
    "Retirement Date": "unit_status_time",
    "Vintage" : "vintage_year",
}

gs_units_cols = {
    "Quantity" : "unit_count",
    "Credit Status": "unit_status",
    "Product Type": "unit_name",
    "Issuance Date": "issuance_date",
    "Retired for CORSIA?": "unit_tags",
    "Aeroplane Operator Name": "unit_owner",
    "CORSIA Authorisation": "unit_tags",
}

projects_enums = {
    "current_registry" : enums.Registries,
    "registry_of_origin" : enums.Registries,
    "sector" : enums.ProjectSector,
    "project_type": enums.ProjectType,
    "project_status": enums.ProjectStatusValues,
    "unit_metric": enums.UnitMetric,
    "methodology": enums.Methodology,
    "validation_body": enums.ValidationBody,
    "covered_by_ndc": enums.CoveredByNDC,
}

project_location_enums = {
    "country": enums.Countries,
}

project_rating_enums = {
    "rating_type": enums.RatingType,
}

labels_enums = {
    "label_type": enums.LabelType,
}

units_enums = {
    "unit_type": enums.UnitType,
    "unit_status": enums.UnitStatus,
    "corresponding_adjustment_declaration": enums.CorrespondingAdjustmentDeclaration,
    "corresponding_adjustment_status": enums.CorrespondingAdjustmentStatus,
}

co_benefit_enums = {
    "co_benefit": enums.SustainableDevelopmentGoals,
}

table_to_enums = {
    "project_location": project_location_enums,
    "projects": projects_enums,
    "labels": labels_enums,
    "units": units_enums,
    "project_rating": project_rating_enums,
    "co_benefits": co_benefit_enums,
}

cadt_co_benifit_enum_map = {
    "SDG 1 - No poverty": enums.SustainableDevelopmentGoals.NoPoverty,
    "SDG 2 - Zero hunger": enums.SustainableDevelopmentGoals.ZeroHunger,
    "SDG 3 - Good health and well-being": enums.SustainableDevelopmentGoals.GoodHealthAndWellBeing,
    "SDG 4 - Quality education": enums.SustainableDevelopmentGoals.QualityEducation,
    "SDG 5 - Gender equality": enums.SustainableDevelopmentGoals.GenderEquality,
    "SDG 6 - Clean water and sanitation": enums.SustainableDevelopmentGoals.CleanWaterAndSanitation,
    "SDG 7 - Affordable and clean energy": enums.SustainableDevelopmentGoals.AffordableAndCleanEnergy,
    "SDG 8 - Decent work and economic growth": enums.SustainableDevelopmentGoals.DecentWorkAndEconomicGrowth,
    "SDG 9 - Industry, innovation, and infrastructure": enums.SustainableDevelopmentGoals.IndustryInnovationAndInfrastructure,
    "SDG 10 - Reduced inequalities": enums.SustainableDevelopmentGoals.ReducedInequalities,
    "SDG 11 - Sustainable cities and communities": enums.SustainableDevelopmentGoals.SustainableCitiesAndCommunities,
    "SDG 12 - Responsible consumption and production": enums.SustainableDevelopmentGoals.ResponsibleConsumptionAndProduction,
    "SDG 13 - Climate action": enums.SustainableDevelopmentGoals.ClimateAction,
    "SDG 14 - Life below water": enums.SustainableDevelopmentGoals.LifeBelowWater,
    "SDG 15 - Life on land": enums.SustainableDevelopmentGoals.LifeOnLand,
    "SDG 16 - Peace and justice strong institutions": enums.SustainableDevelopmentGoals.PeaceJusticeAndStrongInstitutions,
    "SDG 17 - Partnerships for the goals": enums.SustainableDevelopmentGoals.PartnershipsForTheGoals,
}
