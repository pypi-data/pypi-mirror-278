import json
from datetime import datetime

from carbon_registry_indexer.models import enums, target
from carbon_registry_indexer.integrations import utils

import pandas as pd

def preprocess_projects_data(df, table_name):
    project_schema = target.Project.__table__.columns.keys()
    existing_columns = [col for col in project_schema if col in df.columns]
    utils.map_enums(table_name, df)
    df = df[existing_columns]
    df['current_registry'] = enums.Registries.GoldStandard.name
    df['registry_of_origin'] = enums.Registries.GoldStandard.name
    return df.where(pd.notnull(df), None)

def preprocess_co_benefits_data(df, sdg_goals):
    co_benefits = []
    for index, row in df.iterrows():
        if sdg_goals[index]:
            if isinstance(sdg_goals[index], int):
                sdg_goal = [sdg_goals[index]]
            elif isinstance(sdg_goals[index], str):
                sdg_goal = sdg_goals[index].split(',')
            else:
                sdg_goal = []

            for goal in sdg_goal:
                cb = utils.co_benefit_number_reverse_mapping(int(goal))
                if cb:
                    co_benefit = {"cmhq_project_id": row['cmhq_project_id'], "co_benefit": cb}
                    co_benefits.append(co_benefit)
    return co_benefits


def preprocess_estimations_data(df, estimated_annual_credits):
    estimations = []
    for index, row in df.iterrows():
        if estimated_annual_credits[index]:
            estimation = {"cmhq_project_id": row['cmhq_project_id'], "unit_count": estimated_annual_credits[index]}
            estimations.append(estimation)
    return estimations

def preprocess_project_locations_data(df, cmhq_project_ids, countries):
    schema = target.ProjectLocation.__table__.columns.keys()
    existing_columns = [col for col in schema if col in df.columns]
    df = df[existing_columns]
    df['cmhq_project_id'] = cmhq_project_ids
    df['country'] = countries
    return df.where(pd.notnull(df), None)

def preprocess_issuance_data(df, projects_file_path):
    gs_project_ids = [i for i in df['project_id']]
    projects_sheet = pd.read_csv(projects_file_path)
    cmhq_project_ids = {projects_sheet['project_id'][i]: projects_sheet['cmhq_project_id'][i] for i in range(len(projects_sheet)) if projects_sheet['project_id'][i] in gs_project_ids}
    df = df[df['project_id'].apply(lambda x: x in cmhq_project_ids)]
    for index, row in df.iterrows():
        df.at[index, 'cmhq_project_id'] = cmhq_project_ids.get(row['project_id'])
    return df.where(pd.notnull(df), None)

def preprocess_units_data(df, projects_file_path, issuance_file_path, unit_cols):
    projects_sheet = pd.read_csv(projects_file_path)
    project_id_mapping = {row['project_id']: row['cmhq_project_id'] for _, row in projects_sheet.iterrows()}

    issuances_sheet = pd.read_csv(issuance_file_path)
    issuance_id_mapping = {row['cmhq_project_id']: row['issuance_id'] for _, row in issuances_sheet.iterrows()}

    records = []
    label_records = []
    for _, row in df.iterrows():
        cmhq_project_id = project_id_mapping.get(row['project_id'])
        cmhq_issuance_id = issuance_id_mapping.get(cmhq_project_id)
        if cmhq_project_id is None or cmhq_issuance_id is None:
            continue

        row['unit_block_start'] = row['Serial Number']
        row['unit_block_end'] = row['Serial Number']
        row['issuance_id'] = cmhq_issuance_id
        row['unit_tags'] = {}

        for sheet_col, db_col in unit_cols.items():
            if db_col != "unit_tags":
                row[db_col] = row.pop(sheet_col)
            else:
                if isinstance(row[sheet_col], datetime):
                    row[sheet_col] = row[sheet_col].strftime("%Y-%m-%d")
                row['unit_tags'].update({sheet_col: row.pop(sheet_col)})

        if row['Eligible for CORSIA?'] == 'Yes':
            label_records.append({
                "label_type": enums.LabelType.Certification.name,
                'label': 'CORSIA',
                'cmhq_project_id': cmhq_project_id,
            })

        row['unit_tags'] = json.dumps(row['unit_tags'])
        records.append(row)

    return pd.DataFrame(records), pd.DataFrame(label_records)

