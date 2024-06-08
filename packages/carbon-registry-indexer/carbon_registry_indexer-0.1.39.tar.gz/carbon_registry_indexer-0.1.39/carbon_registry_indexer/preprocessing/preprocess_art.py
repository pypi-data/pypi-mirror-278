import json
import os

import pandas as pd

from carbon_registry_indexer.models import enums
from carbon_registry_indexer.integrations import utils, constants

def preprocess_art_projects(df, table_name):
    """
    Preprocess CAR projects data.
    """
    utils.map_enums(table_name, df)
    country = df['country']
    country = utils.map_countries_to_enums(country)
    in_country_region = df['in_country_region']
    df_cleaned = df.where(pd.notnull(df), None)
    df_cleaned['cmhq_project_id'] = [pid for pid in df_cleaned['project_id']]
    df_cleaned['current_registry'] = enums.Registries.ArchitectureForREDDPlusTransactionsART.name
    df_cleaned['registry_of_origin'] = enums.Registries.ArchitectureForREDDPlusTransactionsART.name
    df_cleaned['validation_body'] = df_cleaned['validation_body'].apply(lambda x: x if x is not None else enums.ValidationBody.Other.name)
    df_cleaned['project_tags'] = None
    project_locations_list = []
    for index, row in df_cleaned.iterrows():
        project_tags = {}
        for k, _ in constants.art_project_tags_cols.items():
            if k in row and not pd.isna(row[k]):
                project_tags.update({k: row[k]})
        if project_tags:
            df_cleaned.at[index, 'project_tags'] = json.dumps(project_tags)
        project_location = {
            "cmhq_project_id": row['cmhq_project_id'],
            "country": country[index],
            "in_country_region": in_country_region[index],
        }
        project_locations_list.append(project_location)
            
    return df_cleaned, project_locations_list

def preprocess_art_issuances(df, projects_sheet):
    """
    Preprocess CAR issuances data.
    """
    df_cleaned = df.where(pd.notnull(df), None)
    cmhq_project_ids = {projects_sheet['project_id'][i]: projects_sheet['cmhq_project_id'][i] for i in range(len(projects_sheet))}
    df_cleaned['cmhq_project_id'] = [cmhq_project_ids[pid] for pid in df_cleaned['project_id']]
    df_cleaned['vintage_year'] = df_cleaned['vintage_year'].astype(int)

    return df_cleaned

def preprocess_art_units(df, status, projects_mapping, issuance_sheet, labels_file_path):
    """
    Preprocess CAR units data.
    """
    df['unit_status'] = [status for _ in range(len(df))]
    df['issuance_id'] = None
    df['unit_tags'] = None
    df['unit_block_start'] = None
    df['unit_block_end'] = None
    df['label_id'] = None
    records = []
    for index, row in df.iterrows():
        if 'Credit Serial Numbers' in row:
            if row['Credit Serial Numbers']:
                df.loc[index, 'unit_block_start'] = row['Credit Serial Numbers']
                df.loc[index, 'unit_block_end'] = row['Credit Serial Numbers']
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

        unit_tags = {}

        for k, _ in constants.art_unit_tags_cols.items():
            if k in row and not pd.isna(row[k]):
                unit_tags.update({k: row[k]})
        
        df.loc[index, 'unit_tags'] = json.dumps(unit_tags)
        records.append(df.loc[index].to_dict())

    return records
