import os

from carbon_registry_indexer.models import target
from carbon_registry_indexer.preprocessing import preprocess_cadt as preprocessor
from . import utils

import pandas as pd

project_id_mapping = {}

def cadt_projects_upsert(df, data_dir, table_name):
    """
    Process CADT projects data and save to csv.
    """
    target_csv_path = os.path.join(data_dir, table_name + ".csv")
    df_cleaned = preprocessor.preprocess_cadt_projects(df)
    projects_schema = target.Project.__table__.columns.keys()
    existing_columns = [col for col in projects_schema if col in df_cleaned.columns]
    df_cleaned = df_cleaned[existing_columns]
    df_cleaned.drop(columns=['project_tags'], inplace=True)
    for _, row in df_cleaned.iterrows():
        project_id_mapping[row['cadt_project_id']] = row['cmhq_project_id']
    if not df_cleaned.empty:
        utils.update_csv(df_cleaned, target_csv_path)
        print(f"Processed {len(df_cleaned)} projects. Data saved to {target_csv_path}.")

def cadt_common_upsert(df, data_dir, table_name, schema):
    """
    Process CADT common data and save to csv.
    """
    target_csv_path = os.path.join(data_dir, table_name + ".csv")
    df_cleaned = preprocessor.preprocess_cadt_common(df, schema, table_name, project_id_mapping)
    schema_columns = getattr(target, schema).__table__.columns.keys()
    existing_columns = [col for col in schema_columns if col in df_cleaned.columns]
    df_cleaned = df_cleaned[existing_columns]
    if not df_cleaned.empty:
        utils.update_csv(df_cleaned, target_csv_path)
        print(f"Processed {len(df_cleaned)} {table_name}. Data saved to {target_csv_path}.")

def cadt_units_upsert(df, data_dir, table_name, issuances_file_name, schema):
    """
    Process CADT units data and save to csv.
    """
    target_csv_path = os.path.join(data_dir, table_name + ".csv")
    issuances_file_path = os.path.join(data_dir, issuances_file_name + ".csv")
    if not os.path.exists(issuances_file_path):
        raise FileNotFoundError(f"Issuances file {issuances_file_path} not found.")
    df_cleaned = preprocessor.preprocess_cadt_units(df, issuances_file_path)
    schema_columns = getattr(target, schema).__table__.columns.keys()
    existing_columns = [col for col in schema_columns if col in df_cleaned.columns]
    df_cleaned = df_cleaned[existing_columns]
    if not df_cleaned.empty:
        utils.update_csv(df_cleaned, target_csv_path)
        print(f"Processed {len(df_cleaned)} units. Data saved to {target_csv_path}.")

def cadt_units_json_handler(all_data, data_dir, table_name, issuances_file_name, schema):
    """
    Process CADT units data and save to csv.
    """
    df = pd.json_normalize(all_data)
    cadt_units_upsert(df, data_dir, table_name, issuances_file_name, schema)
