from carbon_registry_indexer.models import enums, target
from carbon_registry_indexer.integrations import utils

import pandas as pd


def preprocess_projects(df):
    """
    Preprocess PURO projects data.
    """
    df['cmhq_project_id'] = ['Puro' + str(df['project_id'][i]) for i in range(len(df))]
    df['registry_of_origin'] = [enums.Registries.PuroEarth.value for _ in range(len(df))]
    df['current_registry'] = [enums.Registries.PuroEarth.value for _ in range(len(df))]
    df_cleaned = df.where(pd.notnull(df), None)
    utils.map_enums('projects', df_cleaned)
    
    return df_cleaned


def preprocess_project_locations(df_cleaned):
    """
    Preprocess project locations.
    """
    project_locations = []
    for _, row in df_cleaned.iterrows():
        project_location = {
            'cmhq_project_id': row['cmhq_project_id'],
            'country': row['country'],
        }
        project_locations.append(project_location)

    df_project_location = pd.DataFrame(project_locations)
    df_project_location['project_location_id'] = df_cleaned.apply(
        lambda row: utils.generate_uuid_from_row(row, ['cmhq_project_id']),
        axis=1
    )
    
    return df_project_location


def preprocess_units(df, projects_file_path):
    """
    Preprocess PURO units data.
    """
    projects_sheet = pd.read_csv(projects_file_path)
    project_name_to_id = dict(zip(projects_sheet['project_name'], projects_sheet['cmhq_project_id']))

    df = df.dropna()

    df['cmhq_project_id'] = [project_name_to_id[project_name] for project_name in df['project_name']]
    df['issuance_id'] = df.apply(
        lambda row: utils.generate_uuid_from_row(row, ['cmhq_project_id']),
        axis=1
    )

    df_cleaned = df.where(pd.notnull(df), None)
    return df_cleaned


def preprocess_units_issuances(df_cleaned):
    """
    Preprocess PURO units issuances data.
    """
    valid_columns = [col for col in target.Issuance.__table__.columns.keys() if col in df_cleaned.columns]
    df_cleaned = df_cleaned[valid_columns]

    return df_cleaned


def preprocess_units_data(df_cleaned):
    """
    Preprocess PURO units data.
    """
    df_cleaned['unit_status'] = [enums.UnitStatus.Retired.value for _ in range(len(df_cleaned))]

    # Double the df by copying retired units with status 'Issued'
    df_cleaned_issued = df_cleaned.copy()
    df_cleaned_issued['unit_status'] = 'Issued'
    df_cleaned = pd.concat([df_cleaned, df_cleaned_issued], ignore_index=True)

    df_cleaned['cmhq_unit_id'] = df_cleaned.apply(
        lambda row: utils.generate_uuid_from_row(row, ['last_status_update', 'unit_count', 'unit_type', 'unit_owner', 'unit_status_reason', 'cmhq_project_id', 'unit_status', 'issuance_id']),
        axis=1
    )
    
    valid_columns = [col for col in target.Unit.__table__.columns.keys() if col in df_cleaned.columns]
    df_cleaned = df_cleaned[valid_columns]

    # Remove completely empty rows
    df_cleaned = df_cleaned.dropna(how='all')
    df_cleaned.drop_duplicates(subset=['cmhq_unit_id'], inplace=True)

    return df_cleaned