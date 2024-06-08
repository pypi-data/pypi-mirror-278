import json
import traceback
import os

from carbon_registry_indexer.models import enums
from carbon_registry_indexer.integrations import utils, constants

import pandas as pd

def preprocess_projects(df, table_name):
    """
    Preprocess ACR projects data.
    """
    country = df['country']
    country = utils.map_countries_to_enums(country)
    in_country_region = df['in_country_region']
    state = df['state']
    compliance = df['compliance_program_status']
    SDG = df['Sustainable Development Goal(s)']
    crediting_period_start = df['Current Crediting Period Start Date']
    crediting_period_end = df['Current Crediting Period End Date']
    total_number_of_credits_registered = df['Total Number of Credits Registered ']
    df['methodology'] = df['methodology'].apply(lambda x: f"ACR - {x}")

    utils.map_enums(table_name, df)
    df_cleaned = df.where(pd.notnull(df), None)
    df_cleaned['current_registry'] = [enums.Registries.AmericanCarbonRegistryACR.name for _ in range(len(df_cleaned))]
    df_cleaned['registry_of_origin'] = [enums.Registries.AmericanCarbonRegistryACR.name for _ in range(len(df_cleaned))]
    df_cleaned['cmhq_project_id'] = [pid for pid in df_cleaned['project_id']]
    df_cleaned['validation_body'] = df_cleaned['validation_body'].apply(lambda x: x if x is not None else enums.ValidationBody.Other.name)

    labels_list = []
    project_locations_list = []
    cobenefits_list = []
    estimations_list = []
    label = None
    df_cleaned['project_tags'] = None

    for index, row in df_cleaned.iterrows():
        unit_count = total_number_of_credits_registered[index]
        if pd.isna(unit_count):
            unit_count = None
        project_tags = {}
        for k, v in constants.acr_project_tags_cols.items():
            if k in row and not pd.isna(row[k]):
                project_tags.update({k: row[k]})
        if project_tags:
            df_cleaned.loc[index, 'project_tags'] = json.dumps(project_tags)

        estimation = {
            "cmhq_project_id": row['cmhq_project_id'],
            "unit_count": unit_count,
            "crediting_period_start": crediting_period_start[index],
            "crediting_period_end": crediting_period_end[index],
        }
        estimations_list.append(estimation)

        if compliance[index] in ["ARB Completed", "ARB Inactive", "Listed - Active ARB Project", "ARB Terminated", "Transferred ARB or Ecology Project"]:
            label = {
                "label_type": enums.LabelType.Certification.name,
                "label": "ARB compliant",
                "cmhq_project_id": row['cmhq_project_id']
            }
        elif compliance[index] in ["Listed - Active Ecology Project", "Transferred ARB or Ecology Project"]:
            label = {
                "label_type": enums.LabelType.Certification.name,
                "label": "Ecology compliant",
                "cmhq_project_id": row['cmhq_project_id']
            }
        project_location = {
            "cmhq_project_id": row['cmhq_project_id'],
            "country": country[index],
            "in_country_region": in_country_region[index],
            "state": state[index]
        }
        if SDG[index]:
            if isinstance(SDG[index], float):
                list_of_all_sdgs = []
            else:
                list_of_all_sdgs = SDG[index].split(',')
            for goal in list_of_all_sdgs:
                sdg = goal.split(":")[-1].strip()
                co_benefit = {
                    "cmhq_project_id": row['cmhq_project_id'],
                    "co_benefit": utils.co_benefit_reverse_mapping(sdg)
                }
                cobenefits_list.append(co_benefit)
        if label:
            labels_list.append(label)
            label = None
        project_locations_list.append(project_location)

    return df_cleaned, labels_list, project_locations_list, cobenefits_list, estimations_list

def preprocess_issuances(df, projects_file_path):
    """
    Preprocess ACR issuances data.
    """
    df_cleaned = df.where(pd.notnull(df), None)
    acr_project_ids = [str(i) for i in df['project_id']]
    projects_sheet = pd.read_csv(projects_file_path)
    cmhq_project_ids = {projects_sheet['project_id'][i]: projects_sheet['cmhq_project_id'][i] for i in range(len(projects_sheet))}
    df_cleaned['cmhq_project_id'] = [cmhq_project_ids[pid] for pid in acr_project_ids]
    df_cleaned['vintage_year'] = df_cleaned['vintage_year'].astype(int)
    return df_cleaned

def preprocess_acr_units(df, status, issuance_sheet, labels_file_path, projects_mapping):
    """
    Preprocess ACR units dataframe.
    """
    df['unit_type'] = df.get('unit_type', None)
    df['issuance_id'] = None
    df['unit_tags'] = None
    df['corresponding_adjustment_declaration'] = None
    df['corresponding_adjustment_status'] = None
    df['unit_status'] = status
    df['unit_block_start'] = None
    df['unit_block_end'] = None
    df['label_id'] = None

    labels = pd.read_csv(labels_file_path) if os.path.exists(labels_file_path) else None

    records = []

    for index, row in df.iterrows():
        try:
            if 'Credit Serial Numbers' in row and row['Credit Serial Numbers']:
                df.loc[index, 'unit_block_start'], df.loc[index, 'unit_block_end'] = row['Credit Serial Numbers'], row['Credit Serial Numbers']

            cmhq_project_id = projects_mapping.get(row['project_id'])

            if not cmhq_project_id:
                raise Exception(f"Project not found for project {row['project_id']}")

            if labels is not None:
                label = labels[labels['cmhq_project_id'] == cmhq_project_id]
                if not label.empty:
                    df.loc[index, 'label_id'] = label['label_id'].values[0]
            if status == enums.UnitStatus.Issued.name:
                issuance = issuance_sheet[
                    (issuance_sheet['cmhq_project_id'] == cmhq_project_id) &
                    (issuance_sheet['issuance_start_date'] == row['issuance_start_date']) &
                    (issuance_sheet['issuance_end_date'] == row['issuance_end_date']) &
                    (issuance_sheet['vintage_year'] == row['vintage_year'])
                ]
            else:
                issuance = issuance_sheet[
                    (issuance_sheet['cmhq_project_id'] == cmhq_project_id) &
                    (issuance_sheet['vintage_year'] == row['vintage_year'])
                ]

            if issuance.empty:
                raise Exception(f"Issuance not found for project {cmhq_project_id}, {row['issuance_start_date']}, {row['issuance_end_date']} & {row['vintage_year']}")
            
            issuance_id = issuance['issuance_id'].values[0]
            df.loc[index, 'issuance_id'] = issuance_id
        
        except Exception as e:
            # print error with traceback
            print(f"Error fetching related issuance: {e}") 
            traceback.print_exc()
            continue
        
        unit_tags = {}

        for k, _ in constants.acr_unit_tags_cols.items():
            if k in row and not pd.isna(row[k]):
                unit_tags.update({k: row[k]})

        df.loc[index, 'unit_tags'] = json.dumps(unit_tags)
        records.append(df.loc[index].to_dict())

    return records
