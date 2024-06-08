import json
import os

import pandas as pd

from carbon_registry_indexer.models import enums
from carbon_registry_indexer.integrations import utils, constants

def preprocess_car_projects(df, table_name):
    """
    Preprocess CAR projects data.
    """
    df['project_status_date'] = None
    total_number_of_credits_registered = df['Total Number of Offset Credits Registered ']

    for index, row in df.iterrows():
        if row['project_status'] == "Listed":
            df.at[index, 'project_status_date'] = row['Project Listed Date']
        elif row['project_status'] == "Registered":
            df.at[index, 'project_status_date'] = row['Project Registered Date']

    utils.map_enums(table_name, df)
    country = df['country']
    country = utils.map_countries_to_enums(country)
    in_country_region = df['in_country_region']
    arb_ids = df['compliance_program_id']
    df_cleaned = df.where(pd.notnull(df), None)
    df_cleaned['cmhq_project_id'] = [pid for pid in df_cleaned['project_id']]
    df_cleaned['current_registry'] = enums.Registries.ClimateActionReserveCAR.name
    df_cleaned['registry_of_origin'] = enums.Registries.ClimateActionReserveCAR.name
    df_cleaned['validation_body'] = df_cleaned['validation_body'].apply(lambda x: x if x is not None else enums.ValidationBody.Other.name)
    df_cleaned['project_tags'] = None
    project_locations_list = []
    labels_list = []
    estimations_list = []
    co_benefits_list = []
    for index, row in df_cleaned.iterrows():
        if row['SDG Impact']:
            list_of_all_sdgs = row['SDG Impact'].split(";")
            for sdg in list_of_all_sdgs:
                sdg = sdg.split(".")[-1].strip()
                co_benefit = {
                    "cmhq_project_id": row['cmhq_project_id'],
                    "co_benefit": utils.co_benefit_reverse_mapping(sdg)
                }
                co_benefits_list.append(co_benefit)
        unit_count = total_number_of_credits_registered[index]
        if pd.isna(unit_count):
            unit_count = None
        estimation = {
            "cmhq_project_id": row['cmhq_project_id'],
            "unit_count": unit_count
        }
        estimations_list.append(estimation)
        project_tags = {}
        for k, _ in constants.car_project_tags_cols.items():
            if k in row and not pd.isna(row[k]):
                project_tags.update({k: row[k]})
        if project_tags:
            df_cleaned.at[index, 'project_tags'] = json.dumps(project_tags)
        if arb_ids[index] != 'NA':
            label = {
                "label_type": enums.LabelType.Certification.name,
                "label": "ARB compliant",
                "cmhq_project_id": row['cmhq_project_id']
            }
        elif df_cleaned['CORSIA Eligible'] == 'Yes':
            label = {
                "label_type": enums.LabelType.Certification.name,
                "label": "CORSIA eligible",
                "cmhq_project_id": row['cmhq_project_id']
            }
        project_location = {
            "cmhq_project_id": row['cmhq_project_id'],
            "country": country[index],
            "in_country_region": in_country_region[index],
        }
        if label:
            labels_list.append(label)
        project_locations_list.append(project_location)
            
    return df_cleaned, labels_list, project_locations_list, co_benefits_list, estimations_list

def preprocess_car_issuances(df, projects_sheet):
    """
    Preprocess CAR issuances data.
    """
    df_cleaned = df.where(pd.notnull(df), None)
    cmhq_project_ids = {projects_sheet['project_id'][i]: projects_sheet['cmhq_project_id'][i] for i in range(len(projects_sheet))}
    df_cleaned['cmhq_project_id'] = [cmhq_project_ids[pid] for pid in df_cleaned['project_id']]
    df_cleaned['vintage_year'] = df_cleaned['vintage_year'].astype(int)

    return df_cleaned

def preprocess_car_units(df, status, projects_sheet, projects_mapping, issuance_sheet, labels_file_path):
    """
    Preprocess CAR units data.
    """
    df['unit_status'] = [status for _ in range(len(df))]
    df['issuance_id'] = None
    df['unit_tags'] = None
    df['corresponding_adjustment_declaration'] = None
    df['corresponding_adjustment_status'] = None
    df['unit_block_start'] = None
    df['unit_block_end'] = None
    df['label_id'] = None
    records = []
    for index, row in df.iterrows():
        if 'Offset Credit Serial Numbers' in row:
            if row['Offset Credit Serial Numbers']:
                df.loc[index, 'unit_block_start'] = row['Offset Credit Serial Numbers']
                df.loc[index, 'unit_block_end'] = row['Offset Credit Serial Numbers']
        try:
            if row['Corresponding Adjustment'] == 'Yes':
                df.loc[index, 'corresponding_adjustment_declaration'] = enums.CorrespondingAdjustmentDeclaration.Committed.name
                df.loc[index, 'corresponding_adjustment_status'] = enums.CorrespondingAdjustmentStatus.Completed.name
            elif row['Corresponding Adjustment'] == 'No':
                df.loc[index, 'corresponding_adjustment_declaration'] = enums.CorrespondingAdjustmentDeclaration.Unknown.name
                df.loc[index, 'corresponding_adjustment_status'] = enums.CorrespondingAdjustmentStatus.NotStarted.name
        except KeyError as e:
            print(f"Error updating corresponding_adjustment: {e}")
        try:
            cmhq_project_id = projects_mapping.get(row['project_id'])
            if not cmhq_project_id:
                raise Exception(f"No project found for project {row['project_id']}")
            
            if status == enums.UnitStatus.Issued.name:
                issuance = issuance_sheet[
                    (issuance_sheet['cmhq_project_id'] == cmhq_project_id) &
                    (issuance_sheet['issuance_start_date'] == row['unit_status_time']) &
                    (issuance_sheet['vintage_year'] == row['vintage_year'])    
                ]
            else:
                issuance = issuance_sheet[
                    (issuance_sheet['cmhq_project_id'] == cmhq_project_id) &
                    (issuance_sheet['vintage_year'] == row['vintage_year'])    
                ]

            if issuance.empty:
                raise Exception(f"Issuance not found for project {cmhq_project_id} & {row['vintage_year']}")
            
            issuance_id = issuance['issuance_id'].values[0]
            df.loc[index, 'issuance_id'] = issuance_id

        except Exception as e:
            print(f"Error fetching related issuance: {e}")
            continue

        try:
            if os.path.exists(labels_file_path):
                labels = pd.read_csv(labels_file_path)
                label = labels[labels['cmhq_project_id'] == cmhq_project_id]
                if not label.empty:
                    df.loc[index, 'label_id'] = label['label_id'].values[0]
        except Exception as e:
            print(f"Error fetching related Label: {e}")

        if "Protocol Version" in row:
            if row["Protocol Version"]:
                methodology = utils.car_map_methodology_enum(row["Protocol Version"])
                if methodology:
                    projects_sheet.loc[projects_sheet['cmhq_project_id'] == cmhq_project_id, "methodology"] = methodology
                    print(f"Updated methodology for project {cmhq_project_id} to {methodology}")
        
        unit_tags = {}

        for k, _ in constants.car_unit_tags_cols.items():
            if k in row and not pd.isna(row[k]):
                unit_tags.update({k: row[k]})
        
        df.loc[index, 'unit_tags'] = json.dumps(unit_tags)
        records.append(df.loc[index].to_dict())

    return records
