## Carbon Registry Indexer

Welcome to the CarbonMarketsHQ Data Indexer! This tool is designed to consolidate data from multiple carbon market registries into a unified schema, making it easier to analyze and utilize carbon market data. This project is open source and we welcome contributions from the community.

### Supported data sources
- [Gold Standard](https://registry.goldstandard.org/projects)
- [American Carbon Registry (ACR)](https://acr2.apx.com/mymodule/mypage.asp)
- [Climate Action Reserve (CAR)](https://thereserve2.apx.com/mymodule/mypage.asp)
- [Climate Action Data Trust (CADT)](https://observer.climateactiondata.org/)
- [Puro Earth](https://registry.puro.earth/carbon-sequestration/retirements)

### Installation
To install the package, you can use pip:
```
pip install carbon-registry-indexer
```

### license
All the code in this repository is MIT licensed.

### Sample Usage

```
indexer = CarbonRegistryIndexer(storage_dir='your_storage_dir'
                            azure_blob_conn_str='your_conn_str', 
                            azure_blob_container='your_container_name')
indexer.setup_storage()  # creates or purges data folder

# calls to initiate sync
indexer.sync_gold_standard()
indexer.sync_climate_action_data_trust()
indexer.sync_american_carbon_registry()
indexer.sync_climate_action_reserve()
indexer.sync_puro_earth()
```

### Output model

- `ProjectLocation`: Stores information about the location of a project, including country, state, and geographic identifier.
- `ProjectRating`: Captures project-level ratings from different rating entities.
- `CoBenefit`: Links a project to the UN Sustainable Development Goals (SDGs) it contributes to.
- `Project`: The core table representing a carbon project. It includes meta information about a project.
- `RelatedProject`: Captures relationships between different projects.
- `Issuance`: Represents an issuance of carbon credits from a project.
- `Label`: Defines a label associated with an issuance, specifying the crediting period and validity.
- `Unit`: Represents the life-cycle of credit units Issued, retired, cancelled, etc.
- `Governance`: Stores picklist values used for governance-related fields.
- `Estimation`: Contains estimated credit information for a project.
