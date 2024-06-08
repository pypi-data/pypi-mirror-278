import os

from carbon_registry_indexer.models import target
from carbon_registry_indexer.preprocessing import preprocess_gs as preprocessor
from . import utils

import pandas as pd

def gs_projects_upsert(df, data_dir, table_name, co_benefits_file_name, estimations_file_name):
    """
    Process GS projects data and save to csv.
    """
    target_csv_path = os.path.join(data_dir, table_name + ".csv")
    co_benefits_csv_path = os.path.join(data_dir, co_benefits_file_name + ".csv")
    estimations_csv_path = os.path.join(data_dir, estimations_file_name + ".csv")

    sdg_goals = df['Sustainable Development Goals']
    estimated_annual_credits = df['Estimated Annual Credits']

    df_cleaned = preprocessor.preprocess_projects_data(df, table_name)

    if not df_cleaned.empty:
        df_cleaned['cmhq_project_id'] = ["GS" + str(pid) for pid in df_cleaned['project_id']]
        cmhq_project_ids = df_cleaned['cmhq_project_id']
        df_cleaned['project_tags'] = {}

        co_benefits = preprocessor.preprocess_co_benefits_data(df_cleaned, sdg_goals)
        estimations = preprocessor.preprocess_estimations_data(df_cleaned, estimated_annual_credits)

        if co_benefits:
            co_benefits_df = pd.DataFrame(co_benefits)
            co_benefits_df['co_benefit_id'] = co_benefits_df.apply(lambda row: utils.generate_uuid_from_row(row, ['cmhq_project_id', 'co_benefit']), axis=1)
            utils.update_csv(co_benefits_df, co_benefits_csv_path, target.CoBenefit.__table__.columns.keys(), check_schema=True)
            print(f"Processed {len(co_benefits)} co-benefits. Data saved to {co_benefits_csv_path}.")

        if estimations:
            estimations_df = pd.DataFrame(estimations)
            estimations_df['estimation_id'] = estimations_df.apply(lambda row: utils.generate_uuid_from_row(row, ['cmhq_project_id']), axis=1)
            utils.update_csv(estimations_df, estimations_csv_path, target.Estimation.__table__.columns.keys(), check_schema=True)
            print(f"Processed {len(estimations)} estimations. Data saved to {estimations_csv_path}.")

        utils.update_csv(df_cleaned, target_csv_path, check_schema=False)
        print(f"Processed {len(df_cleaned)} projects. Data saved to {target_csv_path}.")

    return df['country'], cmhq_project_ids

def gs_project_locations_upsert(df, data_dir, table_name, countries, cmhq_project_ids):
    """
    Process GS project locations data and save to csv.
    """
    target_csv_path = os.path.join(data_dir, table_name + ".csv")

    df_cleaned = preprocessor.preprocess_project_locations_data(df, cmhq_project_ids, countries)
    df_cleaned['project_location_id'] = df_cleaned.apply(lambda row: utils.generate_uuid_from_row(row, ['cmhq_project_id']), axis=1)

    if not df_cleaned.empty:
        utils.update_csv(df_cleaned, target_csv_path, check_schema=False)
        print(f"Processed {len(df)} project locations. Data saved to {target_csv_path}.")

def gs_issuance_upsert(df, data_dir, table_name, projects_file_name):
    """
    Process GS issuances data and save to csv.
    """
    target_csv_path = os.path.join(data_dir, table_name + ".csv")

    df_cleaned = preprocessor.preprocess_issuance_data(df, os.path.join(data_dir, projects_file_name + ".csv"))
    df_cleaned['issuance_id'] = df_cleaned.apply(lambda row: utils.generate_uuid_from_row(row, ['cmhq_project_id', 'issuance_start_date', 'issuance_end_date', 'vintage_year']), axis=1)
    df_cleaned = df_cleaned.drop_duplicates(subset=['issuance_id'])

    if not df_cleaned.empty:
        utils.update_csv(df_cleaned, target_csv_path, check_schema=False)
        print(f"Processed {len(df)} issuances. Data saved to {target_csv_path}.")

def gs_units_upsert(df, unit_cols, data_dir, table_name, projects_file_name, issuance_file_name, labels_file_name):
    """
    Process GS units data and save to csv.
    """
    projects_file_path = os.path.join(data_dir, projects_file_name + ".csv")
    issuance_file_path = os.path.join(data_dir, issuance_file_name + ".csv")
    labels_file_path = os.path.join(data_dir, labels_file_name + ".csv")

    df_cleaned, label_records = preprocessor.preprocess_units_data(df, projects_file_path, issuance_file_path, unit_cols)

    if not label_records.empty:
        label_records['label_id'] = label_records.apply(lambda row: utils.generate_uuid_from_row(row, ['cmhq_project_id']), axis=1)
        label_records = label_records.drop_duplicates(subset=['label_id'])
        utils.update_csv(label_records, labels_file_path, target.Label.__table__.columns.keys(), check_schema=True)
        print(f"Processed {len(label_records)} labels. Data saved to {labels_file_path}.")

    if not df_cleaned.empty:
        df_cleaned['cmhq_unit_id'] = df_cleaned.apply(lambda row: utils.generate_uuid_from_row(row, ['Serial Number', 'project_id', 'issuance_id', 'unit_status', 'issuance_date']), axis=1)
        df_cleaned = df_cleaned.drop_duplicates(subset=['cmhq_unit_id'])
        target_csv_path = os.path.join(data_dir, table_name + ".csv")
        utils.update_csv(df_cleaned, target_csv_path, check_schema=False)
        print(f"Processed {len(df)} units. Data saved to {target_csv_path}.")
