from carbon_registry_indexer.integrations import utils

import pandas as pd

# CADT
def preprocess_cadt_projects(df):
    df.columns = [utils.camel_to_snake(col) for col in df.columns]
    df.rename(columns={"warehouse_project_id": "cadt_project_id", "description": "project_description"}, inplace=True)
    df['cmhq_project_id'] = None
    utils.map_enums("projects", df)

    # Handle special case for project_id
    for index, row in df.iterrows():
        project_id = row['project_id']
        if project_id.startswith("CDM Registry "):
            df.at[index, 'project_id'] = project_id.replace("CDM Registry ", "")
        
        _id = utils.map_registries_for_id(row['current_registry']) + project_id
        if _id in df['cmhq_project_id'] and row['origin_project_id'] != project_id:
            _id = utils.map_registries_for_id(row['current_registry']) + row['origin_project_id']
        df.at[index, 'cmhq_project_id'] = _id

    df.drop_duplicates(subset=['cmhq_project_id'], inplace=True)
    df_cleaned = df.where(pd.notnull(df), None)

    return df_cleaned

def preprocess_cadt_common(df, schema, table_name, project_id_mapping):
    df.columns = [utils.camel_to_snake(col) for col in df.columns]
    if "project_id" in df.columns:
        df.rename(columns={"project_id": "cadt_project_id"}, inplace=True)
    if "cobenefit" in df.columns:
        df.rename(columns={"cobenefit": "co_benefit"}, inplace=True)
        utils.map_cadt_co_benefits(df)
    new_id = f"{utils.camel_to_snake(schema)}_id"
    df.rename(columns={"id": new_id }, inplace=True)
    utils.map_enums(table_name, df)
    df['cmhq_project_id'] = df['cadt_project_id'].map(project_id_mapping)
    df = df[df['cmhq_project_id'].notna()]
    df_cleaned = df.where(pd.notnull(df), None)

    return df_cleaned

def preprocess_cadt_units(df, issuances_file_path):
    df.columns = [utils.camel_to_snake(col) for col in df.columns]
    df.rename(columns={"warehouse_unit_id": "cadt_unit_id"}, inplace=True)
    utils.map_enums("units", df)
    issuances_df = pd.read_csv(issuances_file_path)
    
    df = df[df['issuance_id'].isin(issuances_df['issuance_id'])]
    df_cleaned = df.where(pd.notnull(df), None)
    df_cleaned['cmhq_unit_id'] = df_cleaned.apply(
        lambda row: utils.generate_uuid_from_row(row, ['cadt_unit_id']),
        axis=1
    )

    retired_df = df_cleaned[df_cleaned['unit_status'] == 'Retired']
    issued_df = df_cleaned[df_cleaned['unit_status'] == 'Issued']
    issued_cadt_unit_ids = set(issued_df['cadt_unit_id'])
    additional_rows = retired_df[~retired_df['cadt_unit_id'].isin(issued_cadt_unit_ids)].copy()
    additional_rows['unit_status'] = 'Issued'
    df_cleaned = pd.concat([df_cleaned, additional_rows], ignore_index=True)

    return df_cleaned
