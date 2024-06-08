import json
import os

from carbon_registry_indexer.models import target
from carbon_registry_indexer.preprocessing import preprocess_art as preprocessor
from . import utils

import pandas as pd

def art_projects_upsert(df, data_dir, table_name, project_locations_file_name):
    """
    Process ART projects data and save to csv.
    """
    target_csv_path = os.path.join(data_dir, table_name + ".csv")
    project_locations_file_path = os.path.join(data_dir, project_locations_file_name + ".csv")

    # Preprocess data
    df_cleaned, project_locations_list = preprocessor.preprocess_art_projects(df, table_name)

    # Save data to CSV files
    utils.update_csv(df_cleaned, target_csv_path, check_schema=False)
    print(f"Processed {len(df)} projects. Data saved to {target_csv_path}.")

    if project_locations_list:
        project_locations_df = pd.DataFrame(project_locations_list)
        project_locations_df['project_location_id'] = project_locations_df.apply(
            lambda row: utils.generate_uuid_from_row(row, ['cmhq_project_id']),
            axis=1
        )
        utils.update_csv(project_locations_df, project_locations_file_path, check_schema=True)
        print(f"Processed {len(project_locations_list)} project locations. Data saved to {project_locations_file_path}.")

def art_issuances_upsert(df, data_dir, table_name, projects_file_name):
    """
    Process ART issuances data and save to csv.
    """
    target_csv_path = os.path.join(data_dir, table_name + ".csv")
    projects_file_path = os.path.join(data_dir, projects_file_name + ".csv")

    schema = target.Issuance.__table__.columns.keys()

    projects_sheet = pd.read_csv(projects_file_path)
    df_cleaned = preprocessor.preprocess_art_issuances(df, projects_sheet)

    existing_columns = [col for col in schema if col in df_cleaned.columns]
    df_cleaned = df_cleaned[existing_columns]
    df_cleaned['issuance_id'] = df_cleaned.apply(
        lambda row: utils.generate_uuid_from_row(row, ['cmhq_project_id', 'issuance_start_date', 'vintage_year']),
        axis=1
    )
    df_cleaned = df_cleaned.drop_duplicates(subset=['issuance_id'], keep='first')
    utils.update_csv(df_cleaned, target_csv_path, check_schema=False)
    print(f"Processed {len(df_cleaned)} issuances. Data saved to {target_csv_path}.")

def art_units_issued_upsert(df, data_dir, table_name, projects_file_name, issuances_file_name, labels_file_name, status):
    """
    Process ART units data and save to csv.
    """
    art_project_ids = [str(i) for i in df['project_id']]
    target_csv_path = os.path.join(data_dir, table_name + ".csv")
    projects_file_path = os.path.join(data_dir, projects_file_name + ".csv")
    issuance_file_path = os.path.join(data_dir, issuances_file_name + ".csv")
    labels_file_path = os.path.join(data_dir, labels_file_name + ".csv")
    schema = target.Unit.__table__.columns.keys()

    projects_sheet = pd.read_csv(projects_file_path)
    if not os.path.exists(issuance_file_path):
        raise FileNotFoundError(f"Issuances file {issuance_file_path} not found.")
    issuance_sheet = pd.read_csv(issuance_file_path)
    projects = projects_sheet[projects_sheet['project_id'].isin(art_project_ids)]
    projects_mapping = {}
    for _, row in projects.iterrows():
        projects_mapping[row['project_id']] = row['cmhq_project_id']
    
    records = preprocessor.preprocess_art_units(df, status, projects_mapping, issuance_sheet, labels_file_path)

    # update projects
    utils.direct_merge_and_update_csv(projects_sheet, projects_file_path)
    
    if records:
        df_cleaned = pd.DataFrame(records)
        df_cleaned = df_cleaned.where(pd.notnull(df_cleaned), None)
        df_cleaned['cmhq_unit_id'] = df_cleaned.apply(
            lambda row: utils.generate_uuid_from_row(row, ['issuance_start_date', 'issuance_id', 'vintage_year', 'project_id', 'unit_status', 'unit_count', 'buffer_count', 'unit_owner']),
            axis=1
        )
        existing_columns = [col for col in schema if col in df_cleaned.columns]
        df_cleaned = df_cleaned[existing_columns]
        target_csv_path = os.path.join(data_dir, table_name + ".csv")
        utils.update_csv(df_cleaned, 
                         target_csv_path, 
                         check_schema=False)
        print(f"Processed {len(df)} units. Data saved to {table_name}.csv.")


def art_units_retired_cancelled_upsert(df, data_dir, table_name, projects_file_name, issuances_file_name, labels_file_name, status):
    """
    Process ART units data and save to csv.
    """
    art_project_ids = [str(i) for i in df['project_id']]
    target_csv_path = os.path.join(data_dir, table_name + ".csv")
    projects_file_path = os.path.join(data_dir, projects_file_name + ".csv")
    issuance_file_path = os.path.join(data_dir, issuances_file_name + ".csv")
    labels_file_path = os.path.join(data_dir, labels_file_name + ".csv")
    schema = target.Unit.__table__.columns.keys()

    projects_sheet = pd.read_csv(projects_file_path)
    if not os.path.exists(issuance_file_path):
        raise FileNotFoundError(f"Issuances file {issuance_file_path} not found.")
    issuance_sheet = pd.read_csv(issuance_file_path)
    projects = projects_sheet[projects_sheet['project_id'].isin(art_project_ids)]
    projects_mapping = {}
    for _, row in projects.iterrows():
        projects_mapping[row['project_id']] = row['cmhq_project_id']
    
    records = preprocessor.preprocess_art_units(df, status, projects_sheet, projects_mapping, issuance_sheet, labels_file_path)

    # update projects
    utils.direct_merge_and_update_csv(projects_sheet, projects_file_path)
    
    if records:
        df_cleaned = pd.DataFrame(records)
        df_cleaned = df_cleaned.where(pd.notnull(df_cleaned), None)
        df_cleaned['cmhq_unit_id'] = df_cleaned.apply(
            lambda row: utils.generate_uuid_from_row(row, ['project_id', 'issuance_id', 'unit_status', 'unit_status_time', 'unit_count']),
            axis=1
        )
        existing_columns = [col for col in schema if col in df_cleaned.columns]
        df_cleaned = df_cleaned[existing_columns]
        target_csv_path = os.path.join(data_dir, table_name + ".csv")
        utils.update_csv(df_cleaned, 
                         target_csv_path, 
                         check_schema=False)
        print(f"Processed {len(df)} units. Data saved to {table_name}.csv.")
