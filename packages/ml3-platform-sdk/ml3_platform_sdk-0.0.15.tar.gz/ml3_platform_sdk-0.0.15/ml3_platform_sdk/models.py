from abc import abstractmethod
from datetime import datetime
from typing import Any

from pydantic import Extra, SerializeAsAny

from ml3_platform_sdk.core.enums import RawDataSourceType
from ml3_platform_sdk.core.models import ML3BaseModel as BaseModel
from ml3_platform_sdk.enums import (
    ColumnRole,
    Currency,
    DataStructure,
    DataType,
    DetectionEventActionType,
    DetectionEventSeverity,
    DetectionEventType,
    ExternalIntegration,
    FileType,
    FolderType,
    KPIStatus,
    ModelMetricName,
    ModelStatus,
    MonitoringMetric,
    MonitoringTarget,
    RetrainTriggerType,
    StoragePolicy,
    SuggestionType,
    TaskStatus,
    TaskType,
    TextLanguage,
    UserCompanyRole,
)

# Used for polymorphic classes (de)serialization
subclass_registry: dict = {}


class Company(BaseModel):
    """
    Company model

    Attributes:
        company_id: str
        name: str
        address: str
        vat: str
    """

    company_id: str
    name: str
    address: str
    vat: str


class Project(BaseModel):
    """
    Project model

    Attributes:
        project_id: str
        name: str

    """

    project_id: str
    name: str


class TaskCostInfo(BaseModel):
    """
    Base class for task cost info.
    It depends on TaskType because classification is different from
    regression in terms of business costs due to errors
    """

    currency: Currency

    class Config:
        """
        Allow extra fields
        """

        extra = Extra.allow


class RegressionTaskCostInfo(TaskCostInfo):
    """
    Regression cost info is expressed in two terms:
    - cost due to overestimation
    - cost due to underestimation

    Fields:
        currency
        overestimation_cost
        underestimation_cost
    """

    overestimation_cost: float
    underestimation_cost: float


class BinaryClassificationTaskCostInfo(TaskCostInfo):
    """
    Binary classification cost info is expressed in two terms:
    - cost of false positive
    - cost of false negative
    """

    false_positive_cost: float
    false_negative_cost: float


class MulticlassClassificationTaskCostInfo(TaskCostInfo):
    """
    Multiclass classification cost info is expressed in terms of
    the misclassification costs for each class
    """

    misclassification_cost: dict[str | int, float]


class MultilabelClassificationTaskCostInfo(TaskCostInfo):
    """
    Multilabel classification cost info is expressed in terms of
    false positive and false negative costs for each class
    """

    false_positive_costs: dict[str, float]
    false_negative_costs: dict[str, float]


# type to use in BaseModels
TaskCostInfoUnion = (
    RegressionTaskCostInfo
    | BinaryClassificationTaskCostInfo
    | MulticlassClassificationTaskCostInfo
    | MultilabelClassificationTaskCostInfo
)


class Task(BaseModel):
    """
    Task model

    Attributes:
        task_id: str
        name: str
        type: TaskType
        input_status: TaskStatus
        input_status_insert_datetime: str
        concept_status: TaskStatus
        concept_status_insert_datetime: str
    """

    task_id: str
    name: str
    type: TaskType
    input_status: TaskStatus
    input_status_insert_datetime: str
    concept_status: TaskStatus
    concept_status_insert_datetime: str
    cost_info: TaskCostInfoUnion | None = None
    optional_target: bool
    monitoring_targets: list[str]
    monitoring_metrics: None | dict[str, list[str]] = None
    positive_class: str | int | bool | None = None
    text_language: TextLanguage | None = None


class RetrainTrigger(BaseModel):
    """
    Base model to define a retrain trigger

    Fields:
        type
        credentials_id
    """

    type: RetrainTriggerType
    credentials_id: str


class AWSEventBridgeRetrainTrigger(RetrainTrigger):
    """
    Base model to define an AWS EventBridge retrain trigger

    Fields:
        type
        credentials_id
        aws_region_name
        event_bus_name
    """

    type: RetrainTriggerType = RetrainTriggerType.AWS_EVENT_BRIDGE
    aws_region_name: str
    event_bus_name: str


class GCPPubSubRetrainTrigger(RetrainTrigger):
    """
    Base model to define a GCP PubSub retrain trigger

    Fields:
        type
        credentials_id
        topic_name
    """

    type: RetrainTriggerType = RetrainTriggerType.GCP_PUBSUB
    topic_name: str


class AzureEventGridRetrainTrigger(RetrainTrigger):
    """
    Base model to define an Azure EventGrid retrain trigger

    Fields:
        type
        credentials_id
        topic_endpoint
    """

    type: RetrainTriggerType = RetrainTriggerType.AZURE_EVENT_GRID
    topic_endpoint: str


class Model(BaseModel):
    """
    Base model to define model item

    Attributes:
        model_id: str
        task_id: str
        name: str
        version: str
        status: ModelStatus
        status_data_start_timestamp: Optional[float]
        status_insert_datetime: datetime
        prediction_status: ModelStatus
        prediction_status_data_start_timestamp: Optional[float]
        prediction_status_insert_datetime: datetime
        metric_name: performance or error metric associated with
            the model
        creation_datetime: Optional[datetime]
        retrain_trigger: Optional[RetrainTrigger]
    """

    model_id: str
    task_id: str
    name: str
    version: str
    status: ModelStatus
    status_data_start_timestamp: float | None = None
    status_insert_datetime: datetime
    prediction_status: str
    prediction_status_data_start_timestamp: float | None = None
    prediction_status_insert_datetime: datetime
    metric_name: ModelMetricName
    creation_datetime: datetime | None = None
    retrain_trigger: (
        AWSEventBridgeRetrainTrigger
        | GCPPubSubRetrainTrigger
        | AzureEventGridRetrainTrigger
        | None
    ) = None
    retraining_cost: float


class Job(BaseModel):
    """
    Job information item model

    Attributes:
        job_id: str
        job_group: str
        project_id: str
        project_name: str
        task_id: str
        task_name: str
        model_id: Optional[str]
        model_name: Optional[str]
        status: str
        error: Optional[str]

    """

    job_id: str
    job_group: str
    project_id: str
    project_name: str
    task_id: str
    task_name: str
    model_id: str | None = None
    model_name: str | None = None
    status: str
    error: str | None = None


class ColumnInfo(BaseModel):
    """
    Column base model

    Attributes:
        name: str
        role: ColumnRole
        is_nullable: bool
        data_type: DataType
        predicted_target: Optional[str] = None
        possible_values: Optional[list[str | int | bool]] = None
        model_id: Optional[str] = None
        dims: Optional[tuple[int]] = None
            it is mandatory when data_type is Array
        classes_names: Optional[list[str]] = None
            it is mandatory when the column is the target
            in multilabel classification tasks
    """

    name: str
    role: ColumnRole
    is_nullable: bool
    data_type: DataType
    predicted_target: str | None = None
    possible_values: list[str | int | bool] | None = None
    model_id: str | None = None
    dims: tuple[int, ...] | None = None
    classes_names: list[str] | None = None


class DataSchema(BaseModel):
    """
    Data schema base model

    Attributes:
        columns: List[ColumnInfo]

    """

    columns: list[ColumnInfo]


class KPI(BaseModel):
    """
    KPI base model

    Attributes:
        kpi_id: str
        name: str
        status: ModelStatus
        status_kpi_start_timestamp: Optional[datetime]
        status_insert_datetime: datetime
    """

    kpi_id: str
    name: str
    status: KPIStatus
    status_kpi_start_timestamp: datetime | None = None
    status_insert_datetime: datetime


class SuggestionInfo(BaseModel):
    """
    SuggestionInfo base model

    Attributes:
        id: str
        executed: bool
        timestamp: float
    """

    id: str
    executed: bool
    timestamp: float


class Suggestion(BaseModel):
    """
    Suggestion base model

    Attributes:
        suggestion_id: str
        suggestion_type: SuggestionType
    """

    suggestion_id: str
    suggestion_type: SuggestionType
    sample_ids: list[str]

    class Config:
        """
        Config class for Suggestion
        """

        extra = Extra.allow


class SampleWeightsSuggestion(Suggestion):
    """
    SampleWeightsSuggestion base model

    Attributes:
        suggestion_id: str
        suggestion_type: SuggestionType
        sample_ids: List[str]
        sample_weights: List[float]
    """

    sample_weights: list[float]


class ResampledDatasetSuggestion(Suggestion):
    """
    ResampledDatasetSuggestion base model

    Attributes:
        suggestion_id: str
        suggestion_type: SuggestionType
        sample_ids: List[str]
        sample_counts: List[int]
    """

    sample_counts: list[int]


class RetrainingReport(BaseModel):
    """
    base model for Retraining Report

    Attributes:
        report_id: str
        suggestion: Suggestion
        effective_sample_size: float
        model_metric_name: str
        performance_upper_bound: float
        performance_lower_bound: float
        cost_upper_bound: float
        cost_lower_bound: float
    """

    report_id: str
    suggestion: SerializeAsAny[Suggestion]
    effective_sample_size: float
    model_metric_name: str
    performance_upper_bound: float
    performance_lower_bound: float
    cost_upper_bound: float | None = None
    cost_lower_bound: float | None = None


class CompanyUser(BaseModel):
    """
    base model for company user

    Attributes:
        user_id: str
        company_role: UserCompanyRole
    """

    user_id: str
    company_role: UserCompanyRole


class ApiKey(BaseModel):
    """
    base model for api key

    Attributes:
        api_key: str
    """

    api_key: str
    name: str
    expiration_time: str | None = None


class DetectionEvent(BaseModel):
    """
    An event created during the detection process.

    Attributes:
        event_id: str
        event_type: DetectionEventType
        monitoring_target: MonitoringTarget
        severity_type: Optional[DetectionEventSeverity]
        insert_datetime: str
        sample_timestamp: float
        sample_id: str
        model_id: Optional[str]
        model_name: Optional[str]
        model_version: Optional[str]
    """

    event_id: str
    event_type: DetectionEventType
    monitoring_target: MonitoringTarget
    monitoring_metric: MonitoringMetric | None = None
    severity_type: DetectionEventSeverity | None = None
    insert_datetime: str
    sample_timestamp: float
    sample_id: str
    model_id: str | None = None
    model_name: str | None = None
    model_version: str | None = None


class DetectionEventAction(BaseModel):
    """
    Generic action that can be performed

    Attributes:
        type: DetectionEventActionType
    """

    type: DetectionEventActionType

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        subclass_registry[cls.__name__] = cls


class DiscordNotificationAction(DetectionEventAction):
    """
    Action that sends a notification to a Discord server through
    a webhook that you configure

    Attributes:
        type = DetectionEventActionType.DISCORD_NOTIFICATION
        webhook: str
    """

    type: DetectionEventActionType = (
        DetectionEventActionType.DISCORD_NOTIFICATION
    )
    webhook: str


class SlackNotificationAction(DetectionEventAction):
    """
    Action that sends a notification to a Slack channel through
    a webhook that you configure.

    Attributes:
        type = DetectionEventActionType.SLACK_NOTIFICATION
        webhook: str
        channel: str
    """

    type: DetectionEventActionType = (
        DetectionEventActionType.SLACK_NOTIFICATION
    )
    webhook: str
    channel: str


class EmailNotificationAction(DetectionEventAction):
    """
    Base Model for Email Notification Action

    Attributes:
        type = DetectionEventActionType.EMAIL_NOTIFICATION
        address: str
    """

    type: DetectionEventActionType = (
        DetectionEventActionType.EMAIL_NOTIFICATION
    )
    address: str


class TeamsNotificationAction(DetectionEventAction):
    """
    Base Model for Teams Notification Action

    Attributes:
        type: DetectionEventActionType.TEAMS_NOTIFICATION
        webhook: str
    """

    type: DetectionEventActionType = (
        DetectionEventActionType.TEAMS_NOTIFICATION
    )
    webhook: str


class RetrainAction(DetectionEventAction):
    """
    Base Model for Retrain Action

    Attributes:
        type: DetectionEventActionType.RETRAIN
        model_name: str
    """

    type: DetectionEventActionType = DetectionEventActionType.RETRAIN
    model_name: str | None = None


def deserialize_actions(**kwargs):
    """
    Deserializes polymorphic actions from dict to their models.
    """

    for index in range(len(kwargs["actions"])):
        current_action = kwargs["actions"][index]
        if isinstance(current_action, dict):
            item_action_keys = sorted(current_action.keys())
            for subclass in subclass_registry.values():
                registered_keys = sorted(subclass.__fields__.keys())
                if (
                    item_action_keys == registered_keys
                    and current_action["type"]
                    == subclass.__fields__["type"].default.value
                ):
                    current_action = subclass(**current_action)
                    break
            kwargs["actions"][index] = current_action


class DetectionEventRule(BaseModel):
    """
    A rule that can be triggered by a detection event, and executes
    a series of actions.

    Attributes:
        rule_id: str
        name: str
        task_id: str
        model_name: Optional[str]
        severity: DetectionEventSeverity
        detection_event_type: DetectionEventType
        monitoring_target: MonitoringTarget
        actions: List[DetectionEventAction]
    """

    rule_id: str
    name: str
    task_id: str
    model_name: str | None = None
    severity: DetectionEventSeverity
    detection_event_type: DetectionEventType
    monitoring_target: MonitoringTarget
    monitoring_metric: MonitoringMetric | None = None
    actions: list[SerializeAsAny[DetectionEventAction]]

    # Dynamically instantiate the correct subclass of every ActionModel
    # in the list of actions
    def __init__(self, **kwargs):
        if "actions" in kwargs and kwargs["actions"] is not None:
            deserialize_actions(**kwargs)
        super().__init__(**kwargs)


class IntegrationCredentials(BaseModel):
    """
    Credentials to authenticate to a 3rd party service provider
    via an integration.

    Attributes:
        credentials_id: str
        name: str
        default: bool
        type: ExternalIntegration
    """

    credentials_id: str
    name: str
    default: bool
    type: ExternalIntegration


class AWSCredentials(IntegrationCredentials):
    """
    AWS integration credentials.

    Attributes:
        credentials_id: str
        name: str
        default: bool
        type: ExternalIntegration
        role_arn: The ARN of the role that should be assumed via STS
    """

    role_arn: str


class SecretAWSCredentials(AWSCredentials):
    """
    AWS integration credentials, that also include the external_id
    you need to set up the trust policy on AWS.

    Attributes:
        credentials_id: str
        name: str
        default: bool
        type: ExternalIntegration
        role_arn: The ARN of the IAM role that should be assumed
        external_id: Secret key used to assume the IAM role via STS
    """

    external_id: str

    def generate_trust_policy(self):
        """
        Generates a JSON trust policy that you can copy into the IAM
        role on AWS.
        """

        return f"""
{{
    "Effect": "Allow",
    "Principal": {{
        "AWS": "arn:aws:iam::883313729965:root"
    }},
    "Action": "sts:AssumeRole",
    "Condition": {{
        "StringEquals": {{
            "sts:ExternalId": "{self.external_id}"
        }}
    }}
}}
        """


class GCPCredentials(IntegrationCredentials):
    """
    GCP integration credentials.

    Attributes:
        credentials_id: str
        name: str
        default: bool
        type: ExternalIntegration
        gcp_project_id: The id of the project on GCP
        client_email: The email that identifies the service account
        client_id: The client id
    """

    gcp_project_id: str
    client_email: str
    client_id: str


class AzureCredentials(IntegrationCredentials):
    """
    Azure integration credentials.

    Attributes:
        app_id: The id of the service principal
    """

    app_id: str
    display_name: str
    tenant: str


class DataSource(BaseModel):
    """
    Generic data source.
    """

    file_type: FileType
    is_folder: bool
    folder_type: FolderType | None = None


class LocalDataSource(DataSource):
    """
    Use this data source if you want to upload a file from your
    local disk to the ML cube platform cloud.

    Attributes:
        file_path: str
    """

    file_path: str


class RemoteDataSource(DataSource):
    """
    A source that identifies where data is stored.

    Attributes:
        credentials_id: The id of the credentials to use to authenticate
        to the remote data source. If None, the default will be used
    """

    credentials_id: str | None = None
    storage_policy: StoragePolicy | None = None

    @abstractmethod
    def get_path(self) -> str:
        """
        Return the path of the object
        """

    @abstractmethod
    def get_source_type(self) -> RawDataSourceType:
        """
        Returns raw data source type
        """


class S3DataSource(RemoteDataSource):
    """
    A source that identifies a file in an S3 bucket.

    Attributes:
        object_path: str
    """

    object_path: str

    def get_path(self) -> str:
        return self.object_path

    def get_source_type(self) -> RawDataSourceType:
        return RawDataSourceType.AWS_S3


class GCSDataSource(RemoteDataSource):
    """
    A source that identifies a file in a GCS bucket.

    Attributes:
        object_path: str
    """

    object_path: str

    def get_path(self) -> str:
        return self.object_path

    def get_source_type(self) -> RawDataSourceType:
        return RawDataSourceType.GCS


class AzureBlobDataSource(RemoteDataSource):
    """
    A source that identifies a blob in Azure Storage.

    Attributes:
        object_path: str
    """

    object_path: str

    def get_path(self) -> str:
        return self.object_path

    def get_source_type(self) -> RawDataSourceType:
        return RawDataSourceType.ABS


class Data(BaseModel):
    """
    Generic data model that contains all information about a data

    Attributes:

        data_structure: DataStructure
        source: DataSource
    """

    data_structure: DataStructure
    source: SerializeAsAny[DataSource]


class TabularData(Data):
    """
    Tabular data model i.e., a data that can be represented via
    DataFrame and is stored in formats like: csv, parquet, json
    """

    data_structure: DataStructure = DataStructure.TABULAR


class EmbeddingData(Data):
    """
    Embedding data model i.e., a data that can be represented via
    DataFrame and is stored in formats like: csv, parquet, json.
    There is only one input that has type array_1
    """

    data_structure: DataStructure = DataStructure.EMBEDDING


class ImageData(Data):
    """
    Image data model i.e., images, text or other. Since it is
    composed of multiple files, it needs a mapping between customer ids
    and those files

    Attributes:

        mapping_source: DataSource
    """

    data_structure: DataStructure = DataStructure.IMAGE
    mapping_source: SerializeAsAny[DataSource]
    embedding_source: SerializeAsAny[DataSource] | None = None


class TextData(Data):
    """
    Text data model for nlp tasks.
    """

    data_structure: DataStructure = DataStructure.TEXT
    embedding_source: SerializeAsAny[DataSource] | None = None
