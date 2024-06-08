import hashlib
import os
import re
import uuid

import pandas as pd

from . import constants
from carbon_registry_indexer.models import enums

class IDGenerator:

    null_uuid: uuid.UUID = uuid.UUID("1a34b958-2b3c-4d5f-b6e7-a718c23a9e77")

    def __init__(self, root_uuid: str | uuid.UUID | None = None) -> None:
        self.root_uuid: uuid.UUID = self.null_uuid
        if root_uuid is not None:
            if isinstance(root_uuid, str):
                self.root_uuid = uuid.UUID(root_uuid)
            else:
                self.root_uuid = root_uuid

    def get(self, name: str) -> str:
        return uuid.uuid5(namespace=self.root_uuid, name=name).hex

generator = IDGenerator()

def generate_uuid_from_row(row, key_columns):
    unique_string = '-'.join(str(row[col]) for col in key_columns if col in row)
    row_hash = hashlib.sha256(unique_string.encode('utf-8')).hexdigest()

    return generator.get(row_hash)

def update_csv(data, csv_path, schema=None, check_schema=False):
    """
    Updates a CSV file with new data or creates a new file if it does not exist.

    Parameters:
        data (list of dict): The new data to be added.
        csv_path (str): The path to the CSV file.
    """
    if isinstance(data, list):
        new_data_df = pd.DataFrame(data)
        
    elif isinstance(data, pd.DataFrame):
        new_data_df = data
    else:
        raise ValueError("Data must be a list of dictionaries or a pandas DataFrame.")

    if os.path.exists(csv_path):
        existing_df = pd.read_csv(csv_path)
    else:
        existing_df = pd.DataFrame()

    combined_columns = set(existing_df.columns).union(new_data_df.columns)
    if schema and check_schema:
        combined_columns = set(schema).union(combined_columns)
    
    existing_df = existing_df.reindex(columns=combined_columns)
    new_data_df = new_data_df.reindex(columns=combined_columns)

    final_df = pd.concat([existing_df, new_data_df], ignore_index=True)
    final_df.to_csv(csv_path, index=False)  

def direct_merge_and_update_csv(new_data_df, csv_path, primary_key_col="cmhq_project_id"):
    """
    Update a row in a CSV file based on a primary key or creates a new file if it does not exist.

    Parameters:
        data (Dataframe): The new data to be updated.
        csv_path (str): The path to the CSV file.
        primary_key_col (str): The name of the primary key column.
    """
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"File {csv_path} does not exist.")

    existing_df = pd.read_csv(csv_path)
    
    if primary_key_col not in existing_df.columns:
        raise ValueError(f"Primary key column '{primary_key_col}' does not exist in the CSV file.")
    
    if primary_key_col not in new_data_df.columns:
        raise ValueError(f"Primary key column '{primary_key_col}' does not exist in the new data.")

    # Find the index of the row to update
    existing_df.set_index(primary_key_col, inplace=True)
    new_data_df.set_index(primary_key_col, inplace=True)

    existing_df.update(new_data_df)
    existing_df.reset_index(inplace=True)

    existing_df.to_csv(csv_path, index=False)

def camel_to_snake(name):
    """
    Convert a camelCase string to snake_case.
    """
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

def snake_to_camel(name):
    """
    Convert a snake_case string to camelCase.
    """
    return ''.join(word.title() for word in name.split('_'))

def create_reverse_mapping(enum) :
    """
    Create a reverse mapping of an Enum.

    Parameters:
    - enum: The Enum class for which to create a reverse mapping.
    """
    return {item.value: item.name for item in enum}

def map_registries_for_id(registry):
    return {
        enums.Registries.CDMRegistry.name : 'CDM',
        enums.Registries.GlobalCarbonTrace.name: 'GCT',
        enums.Registries.Verra.name: 'VCS',
        enums.Registries.GlobalCarbonCouncil.name: 'GCC',
        enums.Registries.EcoRegistry.name: 'ER',
        enums.Registries.RoyalKingdomOfBhutan.name: 'RKB',
        enums.Registries.BioCarbonRegistry.name: 'BCS',
        enums.Registries.BioCarbonStandard.name: 'BCS'
    }.get(registry, None)

def map_enums(table, df):
    enum = constants.table_to_enums.get(table)
    if not enum:
        return
    for col, enum in enum.items():
        reverse_mapping = create_reverse_mapping(enum)
        if col in df.columns:           
            if col == "sector":
                df[col] = df[col].apply(lambda x: reverse_mapping.get(x, project_sector_duplicate_mapping(x)))
            elif col == "project_type":
                df[col] = df[col].apply(lambda x: reverse_mapping.get(x, project_type_duplicate_mapping(x)))
            elif col == "validation_body":
                df[col] = df[col].apply(lambda x: reverse_mapping.get(x, validation_body_duplicate_mapping(x)))
            elif col == "methodology":
                df[col] = df[col].apply(lambda x: reverse_mapping.get(x, methodology_duplicate_mapping(x)))
            else:
                df[col] = df[col].apply(lambda x: reverse_mapping.get(x, None))

def map_co_benefits_to_enums_cadt(value):
    return constants.cadt_co_benifit_enum_map.get(value, None)

def map_cadt_co_benefits(df):
    df['co_benefit'] = df['co_benefit'].map(map_co_benefits_to_enums_cadt).where(pd.notnull(df['co_benefit']), None)

def co_benefit_reverse_mapping(sdg):
    if sdg == "Partnership for the Goals":
        return enums.SustainableDevelopmentGoals.PartnershipsForTheGoals.name
    for _, value in enums.SustainableDevelopmentGoals.__members__.items():
        if sdg in value.value:
            return value.name
        
def co_benefit_number_reverse_mapping(sdg):
    if 1 <= sdg <= 17:
        return list(enums.SustainableDevelopmentGoals)[sdg - 1].name
    else:
        return None
    
def car_map_methodology_enum(methodology):
    methodology = 'CAR - ' + methodology
    reverse_mapping = create_reverse_mapping(enums.Methodology)
    return reverse_mapping.get(methodology, None)

def methodology_duplicate_mapping(methodology):
    return {
        "Methodology for Metered & Measured Energy Cooking Devices" : enums.Methodology.GsMethodologyForMeteredMeasuredEnergyCookingDevices.name,
        "GS TPDDTEC v3.1": enums.Methodology.GsTPDDTECV3.name,
        "GS TPDDTEC v 3.": enums.Methodology.GsTPDDTECV3.name,
        "GS TPDDTEC V4.0: REDUCED EMISSIONS FROM COOKING AND HEATING - TECHNOLOGIES AND PRACTICES TO DISPLACE DECENTRALIZED THERMAL ENERGY CONSUMPTION": enums.Methodology.GsTPDDTECV4.name,
        "AMS-I.C. Thermal energy production with or without electricity": enums.Methodology.CdmAmsIc.name,
        "AMS-III.H. Methane recovery in wastewater treatment" : enums.Methodology.CdmAmsIIIh.name,
        "CDM METHODOLOGY - AMS-III.AU “METHANE EMISSION REDUCTION BY ADJUSTED WATER MANAGEMENT PRACTICE IN RICE CULTIVATION" : enums.Methodology.CdmAmsIIIau.name,
        "AMS-II.G. Energy Efficiency Measures in Thermal Applications of Non-Renewable Biomass": enums.Methodology.CdmAmsIIg.name,
        "AMS-I.D. Grid connected renewable electricity generation": enums.Methodology.CdmAmsId.name,
        "AMS-I.L. Electrification of rural communities using renewable energy": enums.Methodology.CdmAmsIl.name,
        "AMS-I.E. Switch from Non-Renewable Biomass for Thermal Applications by the User": enums.Methodology.CdmAmsIe.name,
        "AMS-III.AS. Switch from fossil fuel to biomass in existing manufacturing facilities for non-energy applications": enums.Methodology.CdmAmsIIIAs.name,
        "AMS-II.E. Energy efficiency and fuel switching measures for buildings": enums.Methodology.CdmAmsIIe.name,
        "AMS-III.AJ. Recovery and recycling of materials from solid wastes": enums.Methodology.CdmAmsIIIaj.name,
        "AMS-III.AV. Low greenhouse gas emitting water purification systems": enums.Methodology.CdmAmsIIIav.name,
        "AMS-III.S. Introduction of low-emission vehicles/technologies to commercial vehicle fleets": enums.Methodology.CdmAmsIIIs.name,
        "AMS-III.BM: Lightweight two and three wheeled personal transportation version 1.0": enums.Methodology.CdmAmsIIIbm.name,
        "AMS-III.AR. Substituting fossil fuel based lighting with LED lighting systems": enums.Methodology.CdmAmsIIIar.name,
        "AMS-I.A. Electricity generation by the user": enums.Methodology.CdmAmsIa.name,
        "AMS-III.BA Recovery and recycling of materials from E-waste": enums.Methodology.CdmAmsIIIba.name,
        "AMS-III.BL. Integrated methodology for electrification of communities v2.0": enums.Methodology.CdmAmsIIIbl.name,
        "AMS-II.L Demand-side activities for efficient outdoor and street lighting technologies": enums.Methodology.CdmAmsIIl.name,
        "AMS-III.C. Emission reductions by electric and hybrid vehicles": enums.Methodology.CdmAmsIIIc.name,
        "AMS-III.AO. Methane recovery through controlled anaerobic digestion of animal manure": enums.Methodology.CdmAmsIIIAo.name,
        "AMS-III.G. Landfill methane recovery": enums.Methodology.CdmAmsIIIg.name,
        "AMS-III.F. Avoidance of methane emissions through controlled biological treatment of biomass": enums.Methodology.CdmAmsIIIf.name,
        "AMS-I.K. Solar cookers for households": enums.Methodology.CdmAmsIk.name,
        "AMS-I.I. Biogas/biomass thermal applications for households/small users": enums.Methodology.CdmAmsIi.name,
        "AMS-III.Z. Fuel Switch = 159, process improvement and energy efficiency in brick manufacture": enums.Methodology.CdmAmsIIIz.name,
        "AMS-I.B. Mechanical energy for the user with or without electrical energy": enums.Methodology.CdmAmsIb.name,
        "AMS-III.BG Emission reduction through sustainable charcoal production and consumption": enums.Methodology.CdmAmsIIIbg.name,
        "AMS-III.I. Avoidance of methane production in wastewater treatment through replacement of anaerobic systems by aerobic systems": enums.Methodology.CdmAmsIIIi.name,
        "AMS-II.C. Demand-side energy efficiency activities for specific technologies": enums.Methodology.CdmAmsIIc.name,
        "AMS-III.Z. Fuel Switch, process improvement and energy efficiency in brick manufacture": enums.Methodology.CdmAmsIIIz.name,
        "AMS-III.D. Methane recovery in animal manure management systems": enums.Methodology.CdmAmsIIId.name,
        "AMS-III.R. Methane recovery in agricultural activities at household/small farm level": enums.Methodology.CdmAmsIIIr.name,
        "AMS-III.Q. Waste Energy Recovery (gas/heat/pressure) Projects": enums.Methodology.CdmAmsIIIq.name,
        "AMS-II.J. Demand-side activities for efficient lighting technologies": enums.Methodology.CdmAmsIIj.name,
        "AMS-I.J. Solar water heating systems (SWH) ": enums.Methodology.CdmAmsIj.name,
        "AMS-II.M Demand-side energy efficiency activities for installation of low-flow hot water savings devices": enums.Methodology.CdmAmsIIm.name,
        "AMS-II.J. Demand-side activities for efficient lighting technologies ": enums.Methodology.CdmAmsIIj.name,
        "ACM0001 Flaring or use of landfill gas": enums.Methodology.CdmAm0001.name,
        "ACM0002 Grid-connected electricity generation from renewable sources": enums.Methodology.CdmAm0002.name,
        "ACM0006 Electricity and heat generation from biomass residues": enums.Methodology.CdmAm0006.name,
        "AM0073 GHG emission reductions through multi-site manure collection and treatment in a central plant": enums.Methodology.CdmAm0073.name,
        "ACM0010 GHG emission reductions from manure management systems": enums.Methodology.CdmAm0010.name,
        "AM0086 Installation of zero energy water purifier for safe drinking water application": enums.Methodology.CdmAm0086.name,
        "AM0072 Fossil Fuel Displacement by Geothermal Resources for Space Heating": enums.Methodology.CdmAm0072.name,
        "ACM0012 Waste energy recovery": enums.Methodology.CdmAm0012.name,
        "ACM0022 Alternative waste treatment processes": enums.Methodology.CdmAm0022.name,
        "AM0019 Renewable energy project activities replacing part of the electricity production of one single fossil-fuel-fired power plant that stands alone or supplies electricity to a grid = 21, excluding biomass projects": enums.Methodology.CdmAm0019.name,
        "ACM0014 Treatment of wastewater": enums.Methodology.CdmAm0014.name,
        "ACM0018 Electricity generation from biomass residues in power-only plants": enums.Methodology.CdmAm0018.name,
        "AM0058 Introduction of a district heating system": enums.Methodology.CdmAm0058.name,
        "AM0036 Fuel switch from fossil fuels to biomass residues in heat generation equipment": enums.Methodology.CdmAm0036.name,
        "AM0048 New cogeneration facilities supplying electricity and/or steam to multiple customers and displacing grid/off-grid steam and electricity generation with more carbon-intensive fuels": enums.Methodology.CdmAm0048.name,
        "GS Methodology for Improved Cook stoves and Kitchen Regimes v1.": enums.Methodology.GsMSMethodologyForEfficientCookstovesV1.name,
        "GS Methodology for Improved Cook stoves and Kitchen Regimes v2.": enums.Methodology.GsMSMethodologyForEfficientCookstovesV1.name,
        
    }.get(methodology, methodology)

def project_type_duplicate_mapping(project_type):
    return {
        "Energy distribution": enums.ProjectType.EnergyDistribution.name,
        "REDD+: Reduced Emissions from Deforestation and Degradation": enums.ProjectType.ReducedEmissionsFromDeforestationAndDegradation.name,
        "Organic Waste Composting": enums.ProjectType.Compost.name,
        "Reforestation and Revegetation": enums.ProjectType.AfforestationOrReforestation.name,
        "Landfill Gas Capture/Combustion": enums.ProjectType.LandfillGas.name,
        "Fossil Fuel Switch": enums.ProjectType.FuelSwitching.name,
        "Fugitive Emissions from Fuels (Solid, Oil and Gas)": enums.ProjectType.Fugitive.name,
        "PFCs and SF6": enums.ProjectType.FugitiveEmissionsFromHalocarbonsAndSulphurHexafluoride.name,
        "Livestock - ARB Compliance": enums.ProjectType.Livestock.name,
        "Livestock - MX": enums.ProjectType.Livestock.name,
        "Improved Forest Management - ARB Compliance": enums.ProjectType.ImprovedForestManagement.name,
        "Conservation-Based Forest Management": enums.ProjectType.ImprovedForestManagement.name,
        "Mine Methane Capture - ARB Compliance": enums.ProjectType.CoalMineMethane.name,
        "Coal Mine Methane - Drainage": enums.ProjectType.CoalMineMethane.name,
        "Coal Mine Methane - VAM": enums.ProjectType.CoalMineMethane.name,
        "Ozone Depleting Substances - U.S. - ARB Compliance": enums.ProjectType.OzoneDepletingSubstances.name,
        "Ozone Depleting Substances - U.S.": enums.ProjectType.OzoneDepletingSubstances.name,
        "Ozone Depleting Substances - Article 5 Imports": enums.ProjectType.OzoneDepletingSubstances.name,
        "Avoided Conversion - ARB Compliance": enums.ProjectType.AvoidedConversion.name,
        "Solar Thermal - Electricity": enums.ProjectType.SolarThermalHeat.name,
        "Solar Electricity Systems": enums.ProjectType.SolarThermalHeat.name,
        "Biogas - Heat": enums.ProjectType.BiogasElectricity.name,
        "Energy Efficiency - Agriculture Sector": enums.ProjectType.EnergyEfficiency.name,
        "Energy Efficiency - Commercial Sector": enums.ProjectType.EnergyEfficiency.name,
        "Energy Efficiency - Transport Sector": enums.ProjectType.EnergyEfficiency.name,
        "CO2 Usage": enums.ProjectType.CarbonCaptureStorage.name,
        "Afforestation" : enums.ProjectType.AfforestationOrReforestation.name,
        "Reforestation" : enums.ProjectType.AfforestationOrReforestation.name,
        "A/R" : enums.ProjectType.AfforestationOrReforestation.name,
        "Energy Efficiency - Domestic": enums.ProjectType.EnergyEfficiency.name,
        "Energy Efficiency - Agriculture Sector": enums.ProjectType.EnergyEfficiency.name,
        "Energy Efficiency - Commercial Sector": enums.ProjectType.EnergyEfficiency.name,
        "Energy Efficiency - Transport Sector": enums.ProjectType.EnergyEfficiency.name,
        "Energy Efficiency - Industrial": enums.ProjectType.EnergyEfficiency.name,
        "Energy Efficiency - Public Sector": enums.ProjectType.EnergyEfficiency.name,
        "Biogas - Electricity" : enums.ProjectType.BiogasElectricity.name,
        "Solar Thermal - Heat": enums.ProjectType.SolarThermalHeat.name,
        "Biogas - Heat":  enums.ProjectType.BiogasElectricity.name,
        "Biomass, or Liquid Biofuel - Cogeneration": enums.ProjectType.BiomassOrLiquidBiofuelCogeneration.name,
        "Biomass, or Liquid Biofuel - Electricity" : enums.ProjectType.BiomassOrLiquidBiofuelElectricity.name,
        "Biogas - Cogeneration" : enums.ProjectType.BiogasElectricity.name,
        "Biomass, or Liquid Biofuel - Heat": enums.ProjectType.BiomassOrLiquidBiofuelHeat.name,
        "Small, Low - Impact Hydro" : enums.ProjectType.Hydro.name,
        "Other": enums.ProjectType.Other.name,

    }.get(project_type, project_type)

def validation_body_duplicate_mapping(validation_body):
    return {
        "SCS Global Services (Scientific Certification Systems)": enums.ValidationBody.SCSGlobalServices.name,
        "TÜV SÜD America, Inc. - Ruby Canyon": enums.ValidationBody.TUVSUDAmericaIncRubyCanyon.name,
    }.get(validation_body, None)

def project_sector_duplicate_mapping(sector):
    return {
        "Energy Demand" : enums.ProjectSector.EnergyDemand.name,
        "Energy Industries - renewable/non-renewable sources" : enums.ProjectSector.EnergyIndustries.name,
        "Fugitive emissions from fuels (solid, oil and gas)" : enums.ProjectSector.FugitiveEmissionsFromFuels.name,
        "Chemical Industries" : enums.ProjectSector.ChemicalIndustries.name,
        "Energy Distribution" : enums.ProjectSector.EnergyDistribution.name,
    }.get(sector, sector)

def map_project_size(project_size):
    project_size = project_size.strip().lower()
    return {
        'small scale': enums.ProjectSize.Medium.name,
        'Micro scale': enums.ProjectSize.Small.name,
        'Microscale' : enums.ProjectSize.Small.name,
        'large scale': enums.ProjectSize.Large.name,
    }.get(project_size, None)

def map_countries_to_enums(countries):
    """
    Map country codes to their corresponding Enum names.
    If a country code does not match, retain the original country code.
    """
    mapper = {
        'US': enums.Countries.UnitedStatesOfAmerica.name,
        'MX': enums.Countries.Mexico.name,
        'CA': enums.Countries.Canada.name,
        'BR': enums.Countries.Brazil.name,
        'ML': enums.Countries.Mali.name,
        'MG': enums.Countries.Madagascar.name,
        'BO': enums.Countries.Bolivia.name,
        'SV': enums.Countries.ElSalvador.name,
        'NI': enums.Countries.Nicaragua.name,
        'FR': enums.Countries.France.name,
        'TH': enums.Countries.Thailand.name,
        'SA': enums.Countries.SaudiArabia.name,
    }
    return countries.apply(lambda x: mapper.get(x, x))
