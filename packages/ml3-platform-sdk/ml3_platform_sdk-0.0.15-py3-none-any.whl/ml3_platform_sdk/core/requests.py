from pydantic import Field, SerializeAsAny

from ml3_platform_sdk.core.enums import RawDataSourceType
from ml3_platform_sdk.core.models import ML3BaseModel as BaseModel
from ml3_platform_sdk.enums import (
    ApiKeyExpirationTime,
    DataStructure,
    DetectionEventSeverity,
    DetectionEventType,
    FileType,
    FolderType,
    MonitoringMetric,
    MonitoringTarget,
    StoragePolicy,
    TaskType,
    TextLanguage,
    UserCompanyRole,
    UserProjectRole,
)
from ml3_platform_sdk.models import (
    DataSchema,
    RetrainTrigger,
    TaskCostInfoUnion,
)


class LocalDataSourceInfo(BaseModel):
    """
    Data source info for local uploaded data
    """

    storing_process_id: str


class RemoteDataSourceInfo(BaseModel):
    """
    Data source info for data uploaded from remote storage
    """

    file_type: FileType
    data_source_type: RawDataSourceType
    remote_path: str
    is_folder: bool
    folder_type: FolderType | None
    credentials_id: str | None
    storage_policy: StoragePolicy | None


class DataInfo(BaseModel):
    """
    Model that contains information about data to transfer to
    ML cube Platform
    """

    data_structure: DataStructure
    source: LocalDataSourceInfo | RemoteDataSourceInfo


class TabularDataInfo(DataInfo):
    """
    Model that contains information about tabular data to transfer
    to ML cube Platform
    """

    data_structure: DataStructure = DataStructure.TABULAR


class EmbeddingDataInfo(DataInfo):
    """
    Model that contains information about tabular data to transfer
    to ML cube Platform
    """

    data_structure: DataStructure = DataStructure.EMBEDDING


class ImageDataInfo(DataInfo):
    """
    Model that contains information for image unstructured data to
    transfer to ML cube Platform
    """

    data_structure: DataStructure = DataStructure.IMAGE
    mapping_source: LocalDataSourceInfo | RemoteDataSourceInfo
    embedding_source: LocalDataSourceInfo | RemoteDataSourceInfo | None


class TextDataInfo(DataInfo):
    """Model that contains information for text unstructured data"""

    data_structure: DataStructure = DataStructure.TEXT
    embedding_source: LocalDataSourceInfo | RemoteDataSourceInfo | None


class CreateCompanyRequest(BaseModel):
    """
    CreateCompanyRequest
    """

    name: str
    address: str
    vat: str


class UpdateCompanyRequest(BaseModel):
    """
    UpdateCompanyRequest
    """

    name: str | None
    address: str | None
    vat: str | None


class CreateProjectRequest(BaseModel):
    """
    CreateProjectRequest
    """

    name: str
    description: str | None
    default_storage_policy: StoragePolicy


class UpdateProjectRequest(BaseModel):
    """
    UpdateProjectRequest
    """

    project_id: str
    name: str | None
    description: str | None
    default_storage_policy: StoragePolicy | None


class GetTasksRequest(BaseModel):
    """
    GetTasksRequest
    """

    project_id: str


class GetTaskRequest(BaseModel):
    """
    GetTaskRequest
    """

    task_id: str


class CreateModelRequest(BaseModel):
    """
    CreateModelRequest
    """

    task_id: str
    name: str
    version: str
    metric_name: str
    retraining_cost: float
    preferred_suggestion_type: str
    resampled_dataset_size: int | None


class SetModelSuggestionTypeRequest(BaseModel):
    """
    SetModelSuggestionTypeRequest
    """

    model_id: str
    preferred_suggestion_type: str
    resampled_dataset_size: int | None = None


class GetModelsRequest(BaseModel):
    """
    Get models request model
    """

    task_id: str


class GetModelRequest(BaseModel):
    """
    Get model request model
    """

    model_id: str


class GetSuggestionsRequest(BaseModel):
    """
    Get models request model
    """

    model_id: str
    model_version: str


class UpdateModelVersionBySuggestionIDRequest(BaseModel):
    """
    Update Model Version By SuggestionInfo ID Request
    """

    model_id: str
    new_model_version: str
    suggestion_id: str


class UpdateModelVersionFromTimeRangeRequest(BaseModel):
    """
    Update Model Version From Raw Data Request
    """

    model_id: str
    new_model_version: str
    from_timestamp: float
    to_timestamp: float


class AddHistoricalRequest(BaseModel):
    """
    Add Historical Request model

    `target` is optional only when the Task
    has the `optional_target` attribute set to True i.e., when actually
    the target is allowed to be optional.
    """

    task_id: str
    inputs: SerializeAsAny[DataInfo]
    target: SerializeAsAny[DataInfo] | None


class AddTargetRequest(BaseModel):
    """
    Add Target Request model
    """

    task_id: str
    data: SerializeAsAny[DataInfo]


class AddProductionRequest(BaseModel):
    """
    Add Production Request model
    """

    task_id: str
    inputs: SerializeAsAny[DataInfo] | None
    target: SerializeAsAny[DataInfo] | None
    predictions: list[tuple[str, DataInfo]] | None


class SetModelReferenceRequest(BaseModel):
    """
    Set Reference Request model
    """

    model_id: str
    from_timestamp: float
    to_timestamp: float


class CreateDataSchemaRequest(BaseModel):
    """
    Create Data Schema Request model
    """

    task_id: str
    data_schema: DataSchema


class CreateTaskRequest(BaseModel):
    """
    Create Data Schema Request model
    """

    project_id: str
    name: str
    tags: list[str] | None
    task_type: TaskType
    data_structure: DataStructure
    cost_info: TaskCostInfoUnion | None
    optional_target: bool
    text_language: TextLanguage | None = None
    positive_class: str | int | bool | None = None


class UpdateTaskRequest(BaseModel):
    """
    Update a task request payload
    """

    task_id: str
    name: str | None
    tags: list[str] | None
    cost_info: TaskCostInfoUnion | None


class ComputeRetrainingReportRequest(BaseModel):
    """
    request to compute retraining report
    """

    model_id: str


class GetRetrainingReportRequest(BaseModel):
    """
    request to obtain a previously
    computed retraining report
    """

    model_id: str


class GetDataSchemaRequest(BaseModel):
    """
    Get data schema request model
    """

    task_id: str


class GetJobRequest(BaseModel):
    """
    Get Job Information Request model
    """

    project_id: str | None
    task_id: str | None
    model_id: str | None
    status: str | None
    job_id: str | None


class GetPresignedUrlRequest(BaseModel):
    """
    Get a presigned url for uploading new data
    into ML3 platform
    """

    project_id: str | None
    task_id: str | None
    data_structure: str
    storing_data_type: str
    file_name: str
    file_type: str
    is_folder: bool
    folder_type: str | None
    file_checksum: str
    data_category: str | None
    model_id: str | None = None
    kpi_id: str | None = None


class CreateCompanyUserRequest(BaseModel):
    """
    TODO
    """

    name: str
    surname: str
    username: str
    password: str
    email: str
    company_role: UserCompanyRole


class RemoveUserFromCompanyRequest(BaseModel):
    """
    TODO
    """

    user_id: str


class AddUserToCompanyRequest(BaseModel):
    """
    TODO
    """

    user_id: str


class ChangeUserCompanyRoleRequest(BaseModel):
    """
    TODO
    """

    user_id: str
    company_role: UserCompanyRole


class AddUserProjectRoleRequest(BaseModel):
    """
    TODO
    """

    user_id: str
    project_id: str
    project_role: UserProjectRole


class DeleteUserProjectRoleRequest(BaseModel):
    """
    TODO
    """

    user_id: str
    project_id: str


class CreateApiKeyRequest(BaseModel):
    """
    TODO
    """

    name: str
    expiration_time: ApiKeyExpirationTime


class DeleteApiKeyRequest(BaseModel):
    """
    TODO
    """

    api_key: str


class GetUserApiRequest(BaseModel):
    """
    TODO
    """

    user_id: str


class CreateUserApiRequest(BaseModel):
    """
    TODO
    """

    user_id: str
    name: str
    expiration_time: ApiKeyExpirationTime


class DeleteUserApiKeyRequest(BaseModel):
    """
    TODO
    """

    user_id: str
    api_key: str


class ChangeCompanyOwnerRequest(BaseModel):
    """
    TODO
    """

    user_id: str


class CreateDetectionEventRuleRequest(BaseModel):
    """
    Create a rule that can be triggered by a detection event.
    """

    name: str
    task_id: str
    model_name: str | None
    severity: DetectionEventSeverity
    detection_event_type: DetectionEventType
    monitoring_target: MonitoringTarget
    monitoring_metric: MonitoringMetric | None
    actions: list[dict]


class UpdateDetectionEventRuleRequest(BaseModel):
    """
    Update a rule that can be triggered by a detection event.
    """

    rule_id: str
    name: str | None
    model_name: str | None
    severity: DetectionEventSeverity | None
    detection_event_type: DetectionEventType | None
    monitoring_target: MonitoringTarget | None
    actions: list[dict] | None


class DeleteCompanyUserRequest(BaseModel):
    """
    Delete a user from the company
    """

    user_id: str


class CreateAWSIntegrationCredentialsRequest(BaseModel):
    """
    Request to create integration credentials for AWS on a
    given project.
    """

    name: str
    default: bool
    project_id: str
    role_arn: str


class GCPAccountInfo(BaseModel):
    """
    Information needed to assume a service role.
    """

    type: str
    project_id: str
    private_key_id: str
    private_key: str
    client_email: str
    client_id: str
    auth_uri: str
    token_uri: str
    auth_provider_x509_cert_url: str
    client_x509_cert_url: str
    universe_domain: str


class AzureSPCredentials(BaseModel):
    """
    Information needed to authenticate as an SP.
    """

    app_id: str = Field(alias="appId")
    display_name: str = Field(alias="displayName")
    password: str
    tenant: str


class CreateGCPIntegrationCredentialsRequest(BaseModel):
    """
    Request to create integration credentials for GCP on a
    given project.
    """

    name: str
    default: bool
    project_id: str
    account_info: GCPAccountInfo


class CreateAzureIntegrationCredentialsRequest(BaseModel):
    """
    Request to create integration credentials for Azure on a
    given project.
    """

    name: str
    default: bool
    project_id: str
    credentials: AzureSPCredentials


class CreateKPIRequest(BaseModel):
    """
    Create KPI request
    """

    project_id: str
    name: str


class GetKPIsRequest(BaseModel):
    """
    Get projects request model
    """

    project_id: str


class GetKPIRequest(BaseModel):
    """
    Get KPI request model
    """

    kpi_id: str


class AddKPIDataRequest(BaseModel):
    """
    Add KPI Data Request model
    """

    kpi_id: str
    kpi: SerializeAsAny[DataInfo]


class TestRetrainTriggerRequest(BaseModel):
    """
    Test retrain trigger request
    """

    model_id: str
    retrain_trigger: SerializeAsAny[RetrainTrigger]


class RetrainModelRequest(BaseModel):
    """
    Retrain model request
    """

    model_id: str
