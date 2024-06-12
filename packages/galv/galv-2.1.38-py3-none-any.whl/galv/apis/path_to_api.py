import typing_extensions

from galv.paths import PathValues
from galv.apis.paths.access_levels_ import AccessLevels
from galv.apis.paths.activate_ import Activate
from galv.apis.paths.additional_storage_ import AdditionalStorage
from galv.apis.paths.additional_storage_id_ import AdditionalStorageId
from galv.apis.paths.arbitrary_files_ import ArbitraryFiles
from galv.apis.paths.arbitrary_files_id_ import ArbitraryFilesId
from galv.apis.paths.arbitrary_files_id_file_ import ArbitraryFilesIdFile
from galv.apis.paths.cell_chemistries_ import CellChemistries
from galv.apis.paths.cell_families_ import CellFamilies
from galv.apis.paths.cell_families_id_ import CellFamiliesId
from galv.apis.paths.cell_form_factors_ import CellFormFactors
from galv.apis.paths.cell_manufacturers_ import CellManufacturers
from galv.apis.paths.cell_models_ import CellModels
from galv.apis.paths.cells_ import Cells
from galv.apis.paths.cells_id_ import CellsId
from galv.apis.paths.cells_id_rdf_ import CellsIdRdf
from galv.apis.paths.column_mappings_ import ColumnMappings
from galv.apis.paths.column_mappings_id_ import ColumnMappingsId
from galv.apis.paths.column_types_ import ColumnTypes
from galv.apis.paths.column_types_id_ import ColumnTypesId
from galv.apis.paths.create_token_ import CreateToken
from galv.apis.paths.cycler_tests_ import CyclerTests
from galv.apis.paths.cycler_tests_id_ import CyclerTestsId
from galv.apis.paths.equipment_ import Equipment
from galv.apis.paths.equipment_id_ import EquipmentId
from galv.apis.paths.equipment_families_ import EquipmentFamilies
from galv.apis.paths.equipment_families_id_ import EquipmentFamiliesId
from galv.apis.paths.equipment_manufacturers_ import EquipmentManufacturers
from galv.apis.paths.equipment_models_ import EquipmentModels
from galv.apis.paths.equipment_types_ import EquipmentTypes
from galv.apis.paths.experiments_ import Experiments
from galv.apis.paths.experiments_id_ import ExperimentsId
from galv.apis.paths.files_ import Files
from galv.apis.paths.files_id_ import FilesId
from galv.apis.paths.files_id_applicable_mappings_ import FilesIdApplicableMappings
from galv.apis.paths.files_id_extra_metadata_ import FilesIdExtraMetadata
from galv.apis.paths.files_id_png_ import FilesIdPng
from galv.apis.paths.files_id_reimport_ import FilesIdReimport
from galv.apis.paths.files_id_summary_ import FilesIdSummary
from galv.apis.paths.galv_storage_ import GalvStorage
from galv.apis.paths.galv_storage_id_ import GalvStorageId
from galv.apis.paths.harvest_errors_ import HarvestErrors
from galv.apis.paths.harvest_errors_id_ import HarvestErrorsId
from galv.apis.paths.harvesters_ import Harvesters
from galv.apis.paths.harvesters_id_ import HarvestersId
from galv.apis.paths.labs_ import Labs
from galv.apis.paths.labs_id_ import LabsId
from galv.apis.paths.login_ import Login
from galv.apis.paths.monitored_paths_ import MonitoredPaths
from galv.apis.paths.monitored_paths_id_ import MonitoredPathsId
from galv.apis.paths.parquet_partitions_ import ParquetPartitions
from galv.apis.paths.parquet_partitions_id_ import ParquetPartitionsId
from galv.apis.paths.parquet_partitions_id_file_ import ParquetPartitionsIdFile
from galv.apis.paths.schedule_families_ import ScheduleFamilies
from galv.apis.paths.schedule_families_id_ import ScheduleFamiliesId
from galv.apis.paths.schedule_identifiers_ import ScheduleIdentifiers
from galv.apis.paths.schedules_ import Schedules
from galv.apis.paths.schedules_id_ import SchedulesId
from galv.apis.paths.schema_validations_ import SchemaValidations
from galv.apis.paths.schema_validations_id_ import SchemaValidationsId
from galv.apis.paths.teams_ import Teams
from galv.apis.paths.teams_id_ import TeamsId
from galv.apis.paths.tokens_ import Tokens
from galv.apis.paths.tokens_id_ import TokensId
from galv.apis.paths.units_ import Units
from galv.apis.paths.units_id_ import UnitsId
from galv.apis.paths.users_ import Users
from galv.apis.paths.users_id_ import UsersId
from galv.apis.paths.validation_schemas_ import ValidationSchemas
from galv.apis.paths.validation_schemas_id_ import ValidationSchemasId
from galv.apis.paths.validation_schemas_keys_ import ValidationSchemasKeys

PathToApi = typing_extensions.TypedDict(
    'PathToApi',
    {
        PathValues.ACCESS_LEVELS_: AccessLevels,
        PathValues.ACTIVATE_: Activate,
        PathValues.ADDITIONAL_STORAGE_: AdditionalStorage,
        PathValues.ADDITIONAL_STORAGE_ID_: AdditionalStorageId,
        PathValues.ARBITRARY_FILES_: ArbitraryFiles,
        PathValues.ARBITRARY_FILES_ID_: ArbitraryFilesId,
        PathValues.ARBITRARY_FILES_ID_FILE_: ArbitraryFilesIdFile,
        PathValues.CELL_CHEMISTRIES_: CellChemistries,
        PathValues.CELL_FAMILIES_: CellFamilies,
        PathValues.CELL_FAMILIES_ID_: CellFamiliesId,
        PathValues.CELL_FORM_FACTORS_: CellFormFactors,
        PathValues.CELL_MANUFACTURERS_: CellManufacturers,
        PathValues.CELL_MODELS_: CellModels,
        PathValues.CELLS_: Cells,
        PathValues.CELLS_ID_: CellsId,
        PathValues.CELLS_ID_RDF_: CellsIdRdf,
        PathValues.COLUMN_MAPPINGS_: ColumnMappings,
        PathValues.COLUMN_MAPPINGS_ID_: ColumnMappingsId,
        PathValues.COLUMN_TYPES_: ColumnTypes,
        PathValues.COLUMN_TYPES_ID_: ColumnTypesId,
        PathValues.CREATE_TOKEN_: CreateToken,
        PathValues.CYCLER_TESTS_: CyclerTests,
        PathValues.CYCLER_TESTS_ID_: CyclerTestsId,
        PathValues.EQUIPMENT_: Equipment,
        PathValues.EQUIPMENT_ID_: EquipmentId,
        PathValues.EQUIPMENT_FAMILIES_: EquipmentFamilies,
        PathValues.EQUIPMENT_FAMILIES_ID_: EquipmentFamiliesId,
        PathValues.EQUIPMENT_MANUFACTURERS_: EquipmentManufacturers,
        PathValues.EQUIPMENT_MODELS_: EquipmentModels,
        PathValues.EQUIPMENT_TYPES_: EquipmentTypes,
        PathValues.EXPERIMENTS_: Experiments,
        PathValues.EXPERIMENTS_ID_: ExperimentsId,
        PathValues.FILES_: Files,
        PathValues.FILES_ID_: FilesId,
        PathValues.FILES_ID_APPLICABLE_MAPPINGS_: FilesIdApplicableMappings,
        PathValues.FILES_ID_EXTRA_METADATA_: FilesIdExtraMetadata,
        PathValues.FILES_ID_PNG_: FilesIdPng,
        PathValues.FILES_ID_REIMPORT_: FilesIdReimport,
        PathValues.FILES_ID_SUMMARY_: FilesIdSummary,
        PathValues.GALV_STORAGE_: GalvStorage,
        PathValues.GALV_STORAGE_ID_: GalvStorageId,
        PathValues.HARVEST_ERRORS_: HarvestErrors,
        PathValues.HARVEST_ERRORS_ID_: HarvestErrorsId,
        PathValues.HARVESTERS_: Harvesters,
        PathValues.HARVESTERS_ID_: HarvestersId,
        PathValues.LABS_: Labs,
        PathValues.LABS_ID_: LabsId,
        PathValues.LOGIN_: Login,
        PathValues.MONITORED_PATHS_: MonitoredPaths,
        PathValues.MONITORED_PATHS_ID_: MonitoredPathsId,
        PathValues.PARQUET_PARTITIONS_: ParquetPartitions,
        PathValues.PARQUET_PARTITIONS_ID_: ParquetPartitionsId,
        PathValues.PARQUET_PARTITIONS_ID_FILE_: ParquetPartitionsIdFile,
        PathValues.SCHEDULE_FAMILIES_: ScheduleFamilies,
        PathValues.SCHEDULE_FAMILIES_ID_: ScheduleFamiliesId,
        PathValues.SCHEDULE_IDENTIFIERS_: ScheduleIdentifiers,
        PathValues.SCHEDULES_: Schedules,
        PathValues.SCHEDULES_ID_: SchedulesId,
        PathValues.SCHEMA_VALIDATIONS_: SchemaValidations,
        PathValues.SCHEMA_VALIDATIONS_ID_: SchemaValidationsId,
        PathValues.TEAMS_: Teams,
        PathValues.TEAMS_ID_: TeamsId,
        PathValues.TOKENS_: Tokens,
        PathValues.TOKENS_ID_: TokensId,
        PathValues.UNITS_: Units,
        PathValues.UNITS_ID_: UnitsId,
        PathValues.USERS_: Users,
        PathValues.USERS_ID_: UsersId,
        PathValues.VALIDATION_SCHEMAS_: ValidationSchemas,
        PathValues.VALIDATION_SCHEMAS_ID_: ValidationSchemasId,
        PathValues.VALIDATION_SCHEMAS_KEYS_: ValidationSchemasKeys,
    }
)

path_to_api = PathToApi(
    {
        PathValues.ACCESS_LEVELS_: AccessLevels,
        PathValues.ACTIVATE_: Activate,
        PathValues.ADDITIONAL_STORAGE_: AdditionalStorage,
        PathValues.ADDITIONAL_STORAGE_ID_: AdditionalStorageId,
        PathValues.ARBITRARY_FILES_: ArbitraryFiles,
        PathValues.ARBITRARY_FILES_ID_: ArbitraryFilesId,
        PathValues.ARBITRARY_FILES_ID_FILE_: ArbitraryFilesIdFile,
        PathValues.CELL_CHEMISTRIES_: CellChemistries,
        PathValues.CELL_FAMILIES_: CellFamilies,
        PathValues.CELL_FAMILIES_ID_: CellFamiliesId,
        PathValues.CELL_FORM_FACTORS_: CellFormFactors,
        PathValues.CELL_MANUFACTURERS_: CellManufacturers,
        PathValues.CELL_MODELS_: CellModels,
        PathValues.CELLS_: Cells,
        PathValues.CELLS_ID_: CellsId,
        PathValues.CELLS_ID_RDF_: CellsIdRdf,
        PathValues.COLUMN_MAPPINGS_: ColumnMappings,
        PathValues.COLUMN_MAPPINGS_ID_: ColumnMappingsId,
        PathValues.COLUMN_TYPES_: ColumnTypes,
        PathValues.COLUMN_TYPES_ID_: ColumnTypesId,
        PathValues.CREATE_TOKEN_: CreateToken,
        PathValues.CYCLER_TESTS_: CyclerTests,
        PathValues.CYCLER_TESTS_ID_: CyclerTestsId,
        PathValues.EQUIPMENT_: Equipment,
        PathValues.EQUIPMENT_ID_: EquipmentId,
        PathValues.EQUIPMENT_FAMILIES_: EquipmentFamilies,
        PathValues.EQUIPMENT_FAMILIES_ID_: EquipmentFamiliesId,
        PathValues.EQUIPMENT_MANUFACTURERS_: EquipmentManufacturers,
        PathValues.EQUIPMENT_MODELS_: EquipmentModels,
        PathValues.EQUIPMENT_TYPES_: EquipmentTypes,
        PathValues.EXPERIMENTS_: Experiments,
        PathValues.EXPERIMENTS_ID_: ExperimentsId,
        PathValues.FILES_: Files,
        PathValues.FILES_ID_: FilesId,
        PathValues.FILES_ID_APPLICABLE_MAPPINGS_: FilesIdApplicableMappings,
        PathValues.FILES_ID_EXTRA_METADATA_: FilesIdExtraMetadata,
        PathValues.FILES_ID_PNG_: FilesIdPng,
        PathValues.FILES_ID_REIMPORT_: FilesIdReimport,
        PathValues.FILES_ID_SUMMARY_: FilesIdSummary,
        PathValues.GALV_STORAGE_: GalvStorage,
        PathValues.GALV_STORAGE_ID_: GalvStorageId,
        PathValues.HARVEST_ERRORS_: HarvestErrors,
        PathValues.HARVEST_ERRORS_ID_: HarvestErrorsId,
        PathValues.HARVESTERS_: Harvesters,
        PathValues.HARVESTERS_ID_: HarvestersId,
        PathValues.LABS_: Labs,
        PathValues.LABS_ID_: LabsId,
        PathValues.LOGIN_: Login,
        PathValues.MONITORED_PATHS_: MonitoredPaths,
        PathValues.MONITORED_PATHS_ID_: MonitoredPathsId,
        PathValues.PARQUET_PARTITIONS_: ParquetPartitions,
        PathValues.PARQUET_PARTITIONS_ID_: ParquetPartitionsId,
        PathValues.PARQUET_PARTITIONS_ID_FILE_: ParquetPartitionsIdFile,
        PathValues.SCHEDULE_FAMILIES_: ScheduleFamilies,
        PathValues.SCHEDULE_FAMILIES_ID_: ScheduleFamiliesId,
        PathValues.SCHEDULE_IDENTIFIERS_: ScheduleIdentifiers,
        PathValues.SCHEDULES_: Schedules,
        PathValues.SCHEDULES_ID_: SchedulesId,
        PathValues.SCHEMA_VALIDATIONS_: SchemaValidations,
        PathValues.SCHEMA_VALIDATIONS_ID_: SchemaValidationsId,
        PathValues.TEAMS_: Teams,
        PathValues.TEAMS_ID_: TeamsId,
        PathValues.TOKENS_: Tokens,
        PathValues.TOKENS_ID_: TokensId,
        PathValues.UNITS_: Units,
        PathValues.UNITS_ID_: UnitsId,
        PathValues.USERS_: Users,
        PathValues.USERS_ID_: UsersId,
        PathValues.VALIDATION_SCHEMAS_: ValidationSchemas,
        PathValues.VALIDATION_SCHEMAS_ID_: ValidationSchemasId,
        PathValues.VALIDATION_SCHEMAS_KEYS_: ValidationSchemasKeys,
    }
)
