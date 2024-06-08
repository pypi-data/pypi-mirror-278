import os

from carbon_registry_indexer.models import target
from carbon_registry_indexer.preprocessing import preprocess_acr as preprocessor
from . import utils

import pandas as pd


def acr_projects_upsert(df, data_dir, table_name, project_locations_file_name, labels_file_name, co_benefits_file_name, estimations_file_name):
    """
    Upserts ACR projects.
    """
    target_csv_path = os.path.join(data_dir, table_name + ".csv")
    project_locations_file_path = os.path.join(data_dir, project_locations_file_name + ".csv")
    labels_file_path = os.path.join(data_dir, labels_file_name + ".csv")
    co_benefits_file_path = os.path.join(data_dir, co_benefits_file_name + ".csv")
    estimations_file_path = os.path.join(data_dir, estimations_file_name + ".csv")

    # schema
    project_schema = target.Project.__table__.columns.keys()
    project_locations_schema = target.ProjectLocation.__table__.columns.keys()
    labels_schema = target.Label.__table__.columns.keys()
    co_benefits_schema = target.CoBenefit.__table__.columns.keys()
    estimations_schema = target.Estimation.__table__.columns.keys()

    df_cleaned, labels_list, project_locations_list, cobenefits_list, estimations_list = preprocessor.preprocess_projects(df, table_name)

    if labels_list:
        labels_df = pd.DataFrame(labels_list)
        labels_df['label_id'] = labels_df.apply(
            lambda row: utils.generate_uuid_from_row(row, ['cmhq_project_id']),
            axis=1
        )
        utils.update_csv(labels_df,
                         labels_file_path,
                         labels_schema,
                         check_schema=True)
        print(f"Processed {len(labels_list)} labels. Data saved to {labels_file_path}.")

    if project_locations_list:
        project_locations_df = pd.DataFrame(project_locations_list)
        project_locations_df['project_location_id'] = project_locations_df.apply(
            lambda row: utils.generate_uuid_from_row(row, ['cmhq_project_id']),
            axis=1
        )
        utils.update_csv(project_locations_df,
                         project_locations_file_path,
                         project_locations_schema,
                         check_schema=True)
        print(f"Processed {len(project_locations_list)} project locations. Data saved to {project_locations_file_path}.")

    if cobenefits_list:
        cobenefits_df = pd.DataFrame(cobenefits_list)
        cobenefits_df['co_benefit_id'] = cobenefits_df.apply(
            lambda row: utils.generate_uuid_from_row(row, ['cmhq_project_id', 'co_benefit']),
            axis=1
        )
        utils.update_csv(cobenefits_df,
                         co_benefits_file_path,
                         co_benefits_schema,
                         check_schema=True)
        print(f"Processed {len(cobenefits_list)} co-benefits. Data saved to {co_benefits_file_path}.")

    if estimations_list:
        estimations_df = pd.DataFrame(estimations_list)
        estimations_df['estimation_id'] = estimations_df.apply(
            lambda row: utils.generate_uuid_from_row(row, ['cmhq_project_id']),
            axis=1
        )
        utils.update_csv(estimations_df,
                         estimations_file_path,
                         estimations_schema,
                         check_schema=True)
        print(f"Processed {len(estimations_list)} estimations. Data saved to {estimations_file_path}.")

    if not df_cleaned.empty:
        existing_columns = [col for col in project_schema if col in df_cleaned.columns]
        df_cleaned = df_cleaned[existing_columns]
        utils.update_csv(df_cleaned,
                         target_csv_path,
                         check_schema=False)
        print(f"Processed {len(df)} projects. Data saved to {target_csv_path}.")


def acr_issuances_upsert(df, data_dir, table_name, projects_file_name):
    """
    Upserts ACR issuances.
    """
    target_csv_path = os.path.join(data_dir, table_name + ".csv")
    projects_file_path = os.path.join(data_dir, projects_file_name + ".csv")
    schema = target.Issuance.__table__.columns.keys()

    df_cleaned = preprocessor.preprocess_issuances(df, projects_file_path)
    existing_columns = [col for col in schema if col in df_cleaned.columns]
    df_cleaned = df_cleaned[existing_columns]
    df_cleaned['issuance_id'] = df_cleaned.apply(
        lambda row: utils.generate_uuid_from_row(row, ['cmhq_project_id', 'issuance_start_date', 'issuance_end_date', 'vintage_year', 'unit_status']),
        axis=1
    )
    df_cleaned = df_cleaned.drop_duplicates(subset=['issuance_id'], keep='first')
    utils.update_csv(df_cleaned,
                     target_csv_path,
                     check_schema=False)
    print(f"Processed {len(df_cleaned)} issuances. Data saved to {target_csv_path}.")
    

def acr_units_issued_upsert(df, data_dir, table_name, projects_file_name, issuances_file_name, labels_file_name, status):
    """
    Upserts ACR units.
    """
    acr_project_ids = df['project_id'].tolist()
    projects_file_path = os.path.join(data_dir, projects_file_name + ".csv")
    issuance_file_path = os.path.join(data_dir, issuances_file_name + ".csv")
    labels_file_path = os.path.join(data_dir, labels_file_name + ".csv")
    schema = target.Unit.__table__.columns.keys()

    df['unit_status'] = [status for _ in range(len(df))]

    projects_sheet = pd.read_csv(projects_file_path)
    issuance_sheet = pd.read_csv(issuance_file_path)

    projects = projects_sheet[projects_sheet['project_id'].isin(acr_project_ids)]
    projects_mapping = {row['project_id']: row['cmhq_project_id'] for _, row in projects.iterrows()}

    records = preprocessor.preprocess_acr_units(df, status, issuance_sheet, labels_file_path, projects_mapping)

    if records:
        df_cleaned = pd.DataFrame(records)
        df_cleaned = df_cleaned.where(pd.notnull(df_cleaned), None)
        df_cleaned['cmhq_unit_id'] = df_cleaned.apply(
            lambda row: utils.generate_uuid_from_row(row, ['project_id', 'issuance_id', 'issuance_start_date', 'issuance_end_date', 'vintage_year', 'unit_status_time', 'unit_count']),
            axis=1
        )
        existing_columns = [col for col in schema if col in df_cleaned.columns]
        df_cleaned = df_cleaned[existing_columns]
        target_csv_path = os.path.join(data_dir, table_name + ".csv")
        utils.update_csv(df_cleaned, 
                         target_csv_path, 
                         check_schema=False)
        print(f"Processed {len(df)} units. Data saved to {table_name}.csv.")

def acr_units_retired_cancelled_upsert(df, data_dir, table_name, projects_file_name, issuances_file_name, labels_file_name, status):
    """
    Upserts ACR units.
    """
    acr_project_ids = df['project_id'].tolist()
    projects_file_path = os.path.join(data_dir, projects_file_name + ".csv")
    issuance_file_path = os.path.join(data_dir, issuances_file_name + ".csv")
    labels_file_path = os.path.join(data_dir, labels_file_name + ".csv")
    schema = target.Unit.__table__.columns.keys()

    df['unit_status'] = [status for _ in range(len(df))]

    projects_sheet = pd.read_csv(projects_file_path)
    issuance_sheet = pd.read_csv(issuance_file_path)

    projects = projects_sheet[projects_sheet['project_id'].isin(acr_project_ids)]
    projects_mapping = {row['project_id']: row['cmhq_project_id'] for _, row in projects.iterrows()}

    records = preprocessor.preprocess_acr_units(df, status, issuance_sheet, labels_file_path, projects_mapping)

    if records:
        df_cleaned = pd.DataFrame(records)
        df_cleaned = df_cleaned.where(pd.notnull(df_cleaned), None)
        df_cleaned['cmhq_unit_id'] = df_cleaned.apply(
            lambda row: utils.generate_uuid_from_row(row, ['Credit Serial Numbers', 'project_id', 'issuance_id', 'unit_status', 'unit_status_time', 'unit_count']),
            axis=1
        )
        existing_columns = [col for col in schema if col in df_cleaned.columns]
        df_cleaned = df_cleaned[existing_columns]
        
        target_csv_path = os.path.join(data_dir, table_name + ".csv")
        utils.update_csv(df_cleaned, 
                         target_csv_path, 
                         check_schema=False)
        print(f"Processed {len(df)} units. Data saved to {table_name}.csv.")
