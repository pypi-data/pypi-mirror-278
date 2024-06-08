import io
import json
import os
from typing import List

import carbon_registry_indexer.integrations as sync
from carbon_registry_indexer.integrations import constants
from carbon_registry_indexer.models import enums

import pandas as pd
from azure.storage.blob import BlobServiceClient

class CarbonRegistryIndexer:
    """
    This class is the main entry point for the Carbon Registry Indexer.
    It is responsible for syncing data from all sources.
    """
    def __init__(self, 
                storage_dir="./data", 
                azure_blob_conn_str=None,
                azure_blob_container=None):
        if not azure_blob_conn_str or not azure_blob_container:
            raise ValueError("Azure Blob Storage connection string and container name must be provided.")
        self.storage_dir = storage_dir
        self.azure_blob_conn_str = azure_blob_conn_str
        self.azure_blob_container = azure_blob_container

    def get_blob_data(self, file_name, sheet_name: List[str] = None, max_retries=3):
        """
        Get data from Azure Blob Storage and load it directly into a pandas DataFrame.
        
        Parameters:
        - file_name: The name of the file in the Azure Blob container.

        Returns:
        - A pandas DataFrame containing the data loaded from the Azure Blob file.
        """
        retry_count = 0
        while retry_count < max_retries:
            try:
                # Create a BlobServiceClient using the connection string
                blob_service_client = BlobServiceClient.from_connection_string(self.azure_blob_conn_str)
                
                # Get the BlobClient for the specific file
                blob_client = blob_service_client.get_container_client(self.azure_blob_container).get_blob_client(file_name)
                
                # Download the blob data
                blob_data = blob_client.download_blob().readall()
                
                # Load the blob data into a pandas DataFrame based on the file format
                if file_name.endswith('.csv'):
                    df = pd.read_csv(io.BytesIO(blob_data), encoding='ISO-8859-1', on_bad_lines='skip')
                elif file_name.endswith('.json'):
                    df = pd.read_json(io.BytesIO(blob_data))
                elif file_name.endswith('.xlsx'):
                    if sheet_name:
                        df = {}
                        for sheet in sheet_name:
                            df[sheet] = pd.read_excel(io.BytesIO(blob_data), sheet_name=sheet)
                    else:
                        df = pd.read_excel(io.BytesIO(blob_data), sheet_name=None)
                else:
                    raise ValueError("Unsupported file format")
                return df
            except Exception as e:
                print(f"Error loading data from {file_name}: {e}")
                retry_count += 1

        raise Exception(f"Failed to load data from {file_name} after {max_retries} retries")

    def get_json_files(self, max_retries=3):
        """
        Get all JSON files from the Azure Blob Storage container.
        
        Returns:
        - A list of JSON file names in the Azure Blob container.
        """
        retry_count = 0
        while retry_count < max_retries:
            try:
                blob_service_client = BlobServiceClient.from_connection_string(self.azure_blob_conn_str)
                json_files = constants.JSON_FILES
                all_data = []
                for json_file in json_files:
                    print(f"Getting JSON file: {json_file}")
                    blob_client = blob_service_client.get_container_client(self.azure_blob_container).get_blob_client(json_file)
                    blob_data = blob_client.download_blob().readall()
                    all_data.extend(json.loads(blob_data).get("data"))

                # print(all_data)
                return all_data
            except Exception as e:
                print(f"Error loading JSON files: {e}")
                retry_count += 1
            
        raise Exception(f"Failed to load JSON files after {max_retries} retries")
    
    def get_cadt_data(self, file_name):
        """
        Get CADT data from Azure Blob Storage.
        """
        print("Getting CADT data from Azure Blob Storage")
        dfs = self.get_blob_data(file_name, list(constants.sheets_to_tables.keys()))
        json_files = self.get_json_files()
        
        return dfs, json_files

    def get_gs_data(self, file_name):
        """
        Get Gold Standard data from Azure Blob Storage.
        """
        print("Getting Gold Standard data from Azure Blob Storage")
        dfs = self.get_blob_data(file_name, constants.GS_SHEET_NAMES)
        
        projects_sheet = dfs[constants.GS_SHEET_NAMES[0]].rename(columns=constants.gs_projects_cols)
        issuances_sheet = dfs[constants.GS_SHEET_NAMES[1]].rename(columns=constants.gs_issuances_cols)
        retirements_sheet = dfs[constants.GS_SHEET_NAMES[2]].rename(columns=constants.gs_issuances_cols)

        return projects_sheet, issuances_sheet, retirements_sheet

    def get_acr_data(self):
        """
        Get ACR data from Azure Blob Storage.
        """
        dfs = {}
        for file_name, cols_info in constants.acr_sheet_to_cols.items():
            print(f"Getting ACR data from Azure Blob Storage for {file_name}")
            df = self.get_blob_data(file_name)
            df = df.rename(columns=cols_info)

            dfs[file_name.split(".")[0][1:]] = df

        return dfs["acr_projects"], dfs["acr_credits_issued"], dfs["acr_credits_retired"], dfs["acr_credits_cancelled"]

    def get_car_data(self):
        """
        Get CAR data from Azure Blob Storage.
        """
        dfs = {}
        for file_name, cols_info in constants.car_sheet_to_cols.items():
            print(f"Getting CAR data from Azure Blob Storage for {file_name}")
            df = self.get_blob_data(file_name)
            df = df.rename(columns=cols_info)

            dfs[file_name.split(".")[0][1:]] = df

        return dfs["car_projects"], dfs["car_credits_issued"], dfs["car_credits_retired"], dfs["car_credits_cancelled"]
    
    def get_art_data(self):
        """
        Get ART data from Azure Blob Storage.
        """
        dfs = {}
        for file_name, cols_info in constants.art_sheet_to_cols.items():
            print(f"Getting ART data from Azure Blob Storage for {file_name}")
            df = self.get_blob_data(file_name)
            df = df.rename(columns=cols_info)

            dfs[file_name.split(".")[0][1:]] = df

        return dfs["art_projects"], dfs["art_credits_issued"], dfs["art_credits_retired"], dfs["art_credits_cancelled"]

    def get_puro_data(self):
        """
        Get PURO data from Azure Blob Storage.
        """
        dfs = {}
        print("Getting PURO data from Azure Blob Storage")
        for file_name, cols_info in constants.puro_sheet_to_cols.items():
            print(f"Getting PURO data from Azure Blob Storage for {file_name}")
            df = self.get_blob_data(file_name)
            df = df.rename(columns=cols_info)

            dfs[file_name.split(".")[0][1:]] = df

        return dfs["puro_projects"], dfs["puro_retirements"]

    def _check_if_dir_exists(self, dir_path):
        """
        Check if a directory exists and create it if it does not.
        """
        if not os.path.exists(dir_path):
            print(f"Creating directory: {dir_path}")
            os.makedirs(dir_path)
        else:
            self._purge_files_for_reinsert(dir_path)

    def _purge_files_for_reinsert(self, dir_path):
        """
        Purge all files in a directory.
        """
        for file in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error deleting file: {file_path}")

    def sync_all(self):
        """
        Syncs data from all sources.
        """
        self._check_if_dir_exists(self.storage_dir)

        self.sync_climate_action_data_trust()
        self.sync_gold_standard()
        self.sync_american_carbon_registry()
        self.sync_climate_action_reserve()
        self.sync_puro_earth()

    def setup_storage(self):
        """
        Setup the storage directory.
        """
        self._check_if_dir_exists(self.storage_dir)

    def sync_puro_earth(self):
        """
        Syncs data from PURO Earth.
        """
        projects_sheet, retirements_sheet = self.get_puro_data()
        projects_sheet = projects_sheet.rename(columns=constants.puro_projects_cols)
        retirements_sheet = retirements_sheet.rename(columns=constants.puro_units_cols)
        sync.puro_projects_upsert(projects_sheet,
                                  self.storage_dir,
                                  constants.PROJECTS_STORAGE_FILE_NAME,
                                  constants.PROJECT_LOCATIONS_STORAGE_FILE_NAME)
        sync.puro_units_upsert(retirements_sheet,
                               self.storage_dir,
                               constants.ISSUANCES_STORAGE_FILE_NAME,
                               constants.PROJECTS_STORAGE_FILE_NAME,
                               constants.UNITS_STORAGE_FILE_NAME)
        
    def sync_art(self):
        """
        Syncs data from ART.
        """
        projects_sheet, units_issued_sheet, units_retired_sheet, units_cancelled_sheet = self.get_art_data()
        projects_sheet = projects_sheet.rename(columns=constants.art_projects_cols)
        print(projects_sheet.columns)
        sync.art_projects_upsert(projects_sheet,
                                 self.storage_dir,
                                 constants.PROJECTS_STORAGE_FILE_NAME,
                                 constants.PROJECT_LOCATIONS_STORAGE_FILE_NAME)
        units_issued_sheet = units_issued_sheet.rename(columns=constants.art_units_issued_cols)
        units_retired_sheet = units_retired_sheet.rename(columns=constants.art_units_retired_cols)
        units_cancelled_sheet = units_cancelled_sheet.rename(columns=constants.art_units_issued_cols)
        sync.art_issuances_upsert(units_issued_sheet,
                                  self.storage_dir,
                                  constants.ISSUANCES_STORAGE_FILE_NAME,
                                  constants.PROJECTS_STORAGE_FILE_NAME)
        units_issued_sheet = units_issued_sheet.rename(columns={'issuance_start_date' : 'unit_status_time'})
        sync.art_units_issued_upsert(units_issued_sheet,
                                    self.storage_dir,
                                    constants.UNITS_STORAGE_FILE_NAME,
                                    constants.PROJECTS_STORAGE_FILE_NAME,
                                    constants.ISSUANCES_STORAGE_FILE_NAME,
                                    constants.LABELS_STORAGE_FILE_NAME,
                                    enums.UnitStatus.Issued.name)
        sync.art_units_retired_cancelled_upsert(units_retired_sheet,
                                    self.storage_dir,
                                    constants.UNITS_STORAGE_FILE_NAME,
                                    constants.PROJECTS_STORAGE_FILE_NAME,
                                    constants.ISSUANCES_STORAGE_FILE_NAME,
                                    constants.LABELS_STORAGE_FILE_NAME,
                                    enums.UnitStatus.Retired.name)
        sync.art_units_retired_cancelled_upsert(units_cancelled_sheet,
                                    self.storage_dir,
                                    constants.UNITS_STORAGE_FILE_NAME,
                                    constants.PROJECTS_STORAGE_FILE_NAME,
                                    constants.ISSUANCES_STORAGE_FILE_NAME,
                                    constants.LABELS_STORAGE_FILE_NAME,
                                    enums.UnitStatus.Cancelled.name)
        
    def sync_gold_standard(self):
        """
        Syncs data from Gold Standard.
        """
        projects_sheet, issuances_sheet, retirements_sheet = self.get_gs_data(constants.GS_FILE_NAME)
        projects_sheet = projects_sheet.rename(columns=constants.gs_projects_cols)
        countries, cmhq_project_ids = sync.gs_projects_upsert(projects_sheet, 
                                                              self.storage_dir, 
                                                              constants.PROJECTS_STORAGE_FILE_NAME, 
                                                              constants.CO_BENEFITS_STORAGE_FILE_NAME,
                                                              constants.ESTIMATIONS_STORAGE_FILE_NAME)
        sync.gs_project_locations_upsert(projects_sheet,
                                         self.storage_dir,
                                         constants.PROJECT_LOCATIONS_STORAGE_FILE_NAME,
                                         countries,
                                         cmhq_project_ids)

        # # Issuances and units
        issuance_sheet = issuances_sheet.rename(columns=constants.gs_issuances_cols)
        retirements_sheet = retirements_sheet.rename(columns=constants.gs_issuances_cols)
        sync.gs_issuance_upsert(issuance_sheet,
                                self.storage_dir,
                                constants.ISSUANCES_STORAGE_FILE_NAME,
                                constants.PROJECTS_STORAGE_FILE_NAME)
        sync.gs_units_upsert(issuance_sheet, 
                             constants.gs_units_cols,
                             self.storage_dir,
                             constants.UNITS_STORAGE_FILE_NAME,
                             constants.PROJECTS_STORAGE_FILE_NAME,
                             constants.ISSUANCES_STORAGE_FILE_NAME,
                             constants.LABELS_STORAGE_FILE_NAME)
        constants.gs_units_cols.update({"Note" : "unit_status_reason"})
        sync.gs_units_upsert(retirements_sheet,
                             constants.gs_units_cols,
                             self.storage_dir,
                             constants.UNITS_STORAGE_FILE_NAME,
                             constants.PROJECTS_STORAGE_FILE_NAME,  
                             constants.ISSUANCES_STORAGE_FILE_NAME,
                             constants.LABELS_STORAGE_FILE_NAME)

    def sync_climate_action_data_trust(self):
        """
        Syncs data from CADT.
        """
        dfs, json_files = self.get_cadt_data(constants.CADT_FILE_NAME)
        for sheet_name, table_name in constants.sheets_to_tables.items():
            if sheet_name == "projects":
                sync.cadt_projects_upsert(dfs[sheet_name], 
                                      self.storage_dir, 
                                      table_name)
            elif sheet_name == "units":
                sync.cadt_units_upsert(dfs[sheet_name], 
                                   self.storage_dir, 
                                   table_name, 
                                   constants.ISSUANCES_STORAGE_FILE_NAME,
                                   constants.UNITS_SCHEMA_NAME)
                if json_files:
                    sync.cadt_units_json_handler(json_files, 
                                                 self.storage_dir, 
                                                 table_name, 
                                                 constants.ISSUANCES_STORAGE_FILE_NAME,
                                                 constants.UNITS_SCHEMA_NAME)
            else:
                sync.cadt_common_upsert(dfs[sheet_name], 
                                    self.storage_dir, 
                                    table_name,
                                    sheet_name[0].upper() + sheet_name[1:-1])


    def sync_american_carbon_registry(self):
        """
        Syncs data from ACR.
        """
        projects_sheet, units_issued_sheet, units_retired_sheet, units_cancelled_sheet = self.get_acr_data()
        # projects and project locations
        projects_sheet = projects_sheet.rename(columns=constants.acr_projects_cols)
        sync.acr_projects_upsert(projects_sheet,
                                 self.storage_dir,
                                 constants.PROJECTS_STORAGE_FILE_NAME,
                                 constants.PROJECT_LOCATIONS_STORAGE_FILE_NAME,
                                 constants.LABELS_STORAGE_FILE_NAME,
                                 constants.CO_BENEFITS_STORAGE_FILE_NAME,
                                 constants.ESTIMATIONS_STORAGE_FILE_NAME)
        units_issued_sheet = units_issued_sheet.rename(columns=constants.acr_units_issued_cols)
        units_retired_sheet = units_retired_sheet.rename(columns=constants.acr_units_retired_cols)
        units_cancelled_sheet = units_cancelled_sheet.rename(columns=constants.acr_units_issued_cols)
        sync.acr_issuances_upsert(units_issued_sheet,
                                self.storage_dir,
                                constants.ISSUANCES_STORAGE_FILE_NAME,
                                constants.PROJECTS_STORAGE_FILE_NAME)
        sync.acr_units_issued_upsert(units_issued_sheet,
                              self.storage_dir,
                              constants.UNITS_STORAGE_FILE_NAME,
                              constants.PROJECTS_STORAGE_FILE_NAME,
                              constants.ISSUANCES_STORAGE_FILE_NAME,
                              constants.LABELS_STORAGE_FILE_NAME,
                              enums.UnitStatus.Issued.name)
        sync.acr_units_retired_cancelled_upsert(units_retired_sheet,
                              self.storage_dir,
                              constants.UNITS_STORAGE_FILE_NAME,
                              constants.PROJECTS_STORAGE_FILE_NAME,
                              constants.ISSUANCES_STORAGE_FILE_NAME,
                              constants.LABELS_STORAGE_FILE_NAME,
                              enums.UnitStatus.Retired.name)
        sync.acr_units_retired_cancelled_upsert(units_cancelled_sheet,
                              self.storage_dir,
                              constants.UNITS_STORAGE_FILE_NAME,
                              constants.PROJECTS_STORAGE_FILE_NAME,
                              constants.ISSUANCES_STORAGE_FILE_NAME,
                              constants.LABELS_STORAGE_FILE_NAME,
                              enums.UnitStatus.Cancelled.name)

    def sync_climate_action_reserve(self):
        """
        Syncs data from CAR.
        """
        projects_sheet, units_issued_sheet, units_retired_sheet, units_cancelled_sheet = self.get_car_data()
        projects_sheet = projects_sheet.rename(columns=constants.car_projects_cols)
        sync.car_projects_upsert(projects_sheet,
                                 self.storage_dir,
                                 constants.PROJECTS_STORAGE_FILE_NAME,
                                 constants.PROJECT_LOCATIONS_STORAGE_FILE_NAME,
                                 constants.LABELS_STORAGE_FILE_NAME,
                                 constants.CO_BENEFITS_STORAGE_FILE_NAME,
                                 constants.ESTIMATIONS_STORAGE_FILE_NAME)
        units_issued_sheet = units_issued_sheet.rename(columns=constants.car_units_issued_cols)
        units_retired_sheet = units_retired_sheet.rename(columns=constants.car_units_retired_cols)
        units_cancelled_sheet = units_cancelled_sheet.rename(columns=constants.car_units_issued_cols)
        sync.car_issuances_upsert(units_issued_sheet,
                                  self.storage_dir,
                                  constants.ISSUANCES_STORAGE_FILE_NAME,
                                  constants.PROJECTS_STORAGE_FILE_NAME)
        units_issued_sheet = units_issued_sheet.rename(columns={'issuance_start_date' : 'unit_status_time'})
        sync.car_units_issued_upsert(units_issued_sheet,
                              self.storage_dir,
                              constants.UNITS_STORAGE_FILE_NAME,
                              constants.PROJECTS_STORAGE_FILE_NAME,
                              constants.ISSUANCES_STORAGE_FILE_NAME,
                              constants.LABELS_STORAGE_FILE_NAME,
                              enums.UnitStatus.Issued.name)
        sync.car_units_retired_cancelled_upsert(units_retired_sheet,
                              self.storage_dir,
                              constants.UNITS_STORAGE_FILE_NAME,
                              constants.PROJECTS_STORAGE_FILE_NAME,
                              constants.ISSUANCES_STORAGE_FILE_NAME,
                              constants.LABELS_STORAGE_FILE_NAME,
                              enums.UnitStatus.Retired.name)
        sync.car_units_retired_cancelled_upsert(units_cancelled_sheet,
                              self.storage_dir,
                              constants.UNITS_STORAGE_FILE_NAME,
                              constants.PROJECTS_STORAGE_FILE_NAME,
                              constants.ISSUANCES_STORAGE_FILE_NAME,
                              constants.LABELS_STORAGE_FILE_NAME,
                              enums.UnitStatus.Cancelled.name)
        