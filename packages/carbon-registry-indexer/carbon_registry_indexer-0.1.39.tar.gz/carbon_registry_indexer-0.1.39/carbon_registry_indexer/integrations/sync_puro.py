import os

from carbon_registry_indexer.models import target
from carbon_registry_indexer.preprocessing import preprocess_puro as preprocessor
from . import utils

def puro_projects_upsert(df, data_dir, table_name, project_location_file_name):
    """
    Process PURO projects data and save to csv.
    """
    target_csv_path = os.path.join(data_dir, table_name + ".csv")
    project_location_file_path = os.path.join(data_dir, project_location_file_name + ".csv")

    df_cleaned = preprocessor.preprocess_projects(df)
    df_project_location = preprocessor.preprocess_project_locations(df_cleaned)

    if not df_project_location.empty:
        utils.update_csv(df_project_location, project_location_file_path, check_schema=False)
        print(f"Processed {len(df_project_location)} project locations. Data saved to {project_location_file_path}.")

    # Project
    existing_columns = [col for col in target.Project.__table__.columns.keys() if col in df.columns]
    df_cleaned = df_cleaned[existing_columns]

    if not df_cleaned.empty:
        utils.update_csv(df_cleaned, target_csv_path, check_schema=False)
        print(f"Processed {len(df)} projects. Data saved to {target_csv_path}.")


def puro_units_upsert(df, data_dir, table_name, projects_file_name, units_file_name):
    """
    Process PURO issuances data and save to csv.
    """
    target_csv_path = os.path.join(data_dir, table_name + ".csv")
    projects_file_path = os.path.join(data_dir, projects_file_name + ".csv")
    units_file_path = os.path.join(data_dir, units_file_name + ".csv")

    df_cleaned = preprocessor.preprocess_units(df, projects_file_path)
    df_cleaned_issuances = preprocessor.preprocess_units_issuances(df_cleaned)
    df_cleaned_units = preprocessor.preprocess_units_data(df_cleaned)

    if not df_cleaned_issuances.empty:
        utils.update_csv(df_cleaned_issuances, target_csv_path, check_schema=False)
        print(f"Processed {len(df_cleaned_issuances)} issuances. Data saved to {target_csv_path}.")

    if not df_cleaned_units.empty:
        utils.update_csv(df_cleaned_units, units_file_path, check_schema=False)
        print(f"Processed {len(df_cleaned_units)} units. Data saved to {units_file_path}.")
