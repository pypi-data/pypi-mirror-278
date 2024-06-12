from enum import Enum


class TaskType(Enum):
    """
    **Fields:**

        - REGRESSION
        - CLASSIFICATION_BINARY
        - CLASSIFICATION_MULTICLASS
        - CLASSIFICATION_MULTILABEL
        - RAG
    """

    REGRESSION = "regression"
    CLASSIFICATION_BINARY = "classification_binary"
    CLASSIFICATION_MULTICLASS = "classification_multiclass"
    CLASSIFICATION_MULTILABEL = "classification_multilabel"
    RAG = "rag"

    def __str__(self):
        return self.value


class TaskStatus(Enum):
    """
    **Fields:**

        - OK
        - WARNING
        - DRIFT
    """

    OK = "ok"
    WARNING = "warning"
    DRIFT = "drift"

    def __str__(self):
        return self.value


class ModelStatus(Enum):
    """
    **Fields:**

        - NOT_INITIALIZED
        - OK
        - WARNING
        - DRIFT
    """

    NOT_INITIALIZED = "not_initialized"
    OK = "ok"
    WARNING = "warning"
    DRIFT = "drift"

    def __str__(self):
        return self.value


class KPIStatus(Enum):
    """
    **Fields:**

        - NOT_INITIALIZED
        - OK
        - WARNING
        - DRIFT
    """

    NOT_INITIALIZED = "not_initialized"
    OK = "ok"
    WARNING = "warning"
    DRIFT = "drift"

    def __str__(self):
        return self.value


class DataStructure(Enum):
    """
    Represents the typology of the data to send

    **Fields:**

        - TABULAR
        - IMAGE
        - TEXT
        - EMBEDDING
    """

    TABULAR = "tabular"
    IMAGE = "image"
    TEXT = "text"
    EMBEDDING = "embedding"

    def __str__(self):
        return self.value


class StoringDataType(Enum):
    """
    **Fields:**

        - HISTORICAL
        - REFERENCE
        - PRODUCTION
    """

    HISTORICAL = "historical"
    PRODUCTION = "production"
    TASK_TARGET = "task_target"
    KPI = "kpi"

    def __str__(self):
        return self.value


class FileType(Enum):
    """
    **Fields:**

        - CSV
        - JSON
    """

    CSV = "csv"
    JSON = "json"
    PARQUET = "parquet"
    PNG = "png"
    JPG = "jpg"
    NPY = "npy"

    def __str__(self):
        return self.value


class FolderType(Enum):
    """
    Type of folder

    **Fields**

        - UNCOMPRESSED
        - TAR
        - ZIP
    """

    UNCOMPRESSED = "uncompressed"
    TAR = "tar"
    ZIP = "zip"


class JobStatus(Enum):
    """
    **Fields:**

        - IDLE
        - STARTING
        - RUNNING
        - COMPLETED
        - ERROR
    """

    IDLE = "idle"
    STARTING = "starting"
    RUNNING = "running"
    COMPLETED = "completed"
    ERROR = "error"

    def __str__(self):
        return self.value


class UserCompanyRole(Enum):
    """
    **Fields:**

        - COMPANY_OWNER
        - COMPANY_ADMIN
        - COMPANY_USER
        - COMPANY_NONE
    """

    COMPANY_OWNER = "COMPANY_OWNER"
    COMPANY_ADMIN = "COMPANY_ADMIN"
    COMPANY_USER = "COMPANY_USER"
    COMPANY_NONE = "COMPANY_NONE"

    def __str__(self):
        return self.value


class UserProjectRole(Enum):
    """
    **Fields:**

        - PROJECT_ADMIN
        - PROJECT_USER
        - PROJECT_VIEW
    """

    PROJECT_ADMIN = "PROJECT_ADMIN"
    PROJECT_USER = "PROJECT_USER"
    PROJECT_VIEW = "PROJECT_VIEW"

    def __str__(self):
        return self.value


class DetectionEventSeverity(Enum):
    """
    **Fields:**

        - LOW
        - MEDIUM
        - HIGH
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

    def __str__(self):
        return self.value


class DetectionEventType(Enum):
    """
    **Fields:**

        - DRIFT
    """

    WARNING_OFF = "warning_off"
    WARNING_ON = "warning_on"
    DRIFT_ON = "drift_on"
    DRIFT_OFF = "drift_off"

    def __str__(self):
        return self.value


class MonitoringTarget(Enum):
    """
    **Fields:**

        - ERROR
        - INPUT
        - CONCEPT
        - PREDICTION
    """

    ERROR = "error"
    INPUT = "input"
    CONCEPT = "concept"
    PREDICTION = "prediction"

    def __str__(self):
        return self.value


class MonitoringMetric(Enum):
    """
    **Fields:**

        - FEATURE
        - TEXT_TOXICITY
        - TEXT_EMOTION
        - TEXT_SENTIMENT
    """

    FEATURE = "feature"
    TEXT_TOXICITY = "text_toxicity"
    TEXT_EMOTION = "text_emotion"
    TEXT_SENTIMENT = "text_sentiment"
    TEXT_LENGTH = "text_length"

    def __str__(self):
        return self.value


class DetectionEventActionType(Enum):
    """
    **Fields:**

        - DISCORD_NOTIFICATION
        - SLACK_NOTIFICATION

    """

    DISCORD_NOTIFICATION = "discord_notification"
    SLACK_NOTIFICATION = "slack_notification"
    EMAIL_NOTIFICATION = "email_notification"
    TEAMS_NOTIFICATION = "teams_notification"
    RETRAIN = "retrain"

    def __str__(self):
        return self.value


class ModelMetricName(Enum):
    """
    Name of the model metrics that is associated with the model

    **Fields:**
        - RMSE
        - RSQUARE
    """

    RMSE = "rmse"
    RSQUARE = "rsquare"
    ACCURACY = "accuracy"

    def __str__(self):
        return self.value


class SuggestionType(Enum):
    """
    Enum to specify the preferred
    type of suggestion

    **Fields:**
        - SAMPLE_WEIGHTS
        - RESAMPLED_DATASET
    """

    SAMPLE_WEIGHTS = "sample_weights"
    RESAMPLED_DATASET = "resampled_dataset"

    def __str__(self):
        return self.value


class ApiKeyExpirationTime(Enum):
    """
    **Fields:**

        - ONE_MONTH
        - THREE_MONTHS
        - SIX_MONTHS
        - ONE_YEAR
        - NEVER

    """

    ONE_MONTH = "one_month"
    THREE_MONTHS = "three_months"
    SIX_MONTHS = "six_months"
    ONE_YEAR = "one_year"
    NEVER = "never"

    def __str__(self):
        return self.value


class ExternalIntegration(Enum):
    """
    An integration with a 3rd party service provider

    **Fields:**
        - AWS
        - GCP
        - AZURE
    """

    AWS = "aws"
    GCP = "gcp"
    AZURE = "azure"

    def __str__(self):
        return self.value


class StoragePolicy(Enum):
    """
    Enumeration that specifies the storage policy for the data sent to
    ML cube Platform

    **Fields:**
        - MLCUBE: data are copied and stored into the ML cube Platform
            cloud
        - CUSTOMER: data are kept only in your cloud and ML cube
            Platform will access to this storage source every time
            it needs to read data
    """

    MLCUBE = "mlcube"
    CUSTOMER = "customer"

    def __str__(self):
        return self.value


class RetrainTriggerType(Enum):
    """
    Enumeration of the possible retrain triggers
    """

    AWS_EVENT_BRIDGE = "aws_event_bridge"
    GCP_PUBSUB = "gcp_pubsub"
    AZURE_EVENT_GRID = "azure_event_grid"

    def __str__(self):
        return self.value


class Currency(Enum):
    """
    Currency of to use for the Task
    """

    EURO = "euro"
    DOLLAR = "dollar"

    def __str__(self):
        return self.value


class DataType(Enum):
    """
    Data type enum
    Describe data type of an input
    """

    FLOAT = "float"
    STRING = "string"
    CATEGORICAL = "categorical"

    # array can have multiple dimensions each of them with n elemens
    # for instance, an image is an array with c channels, hence it is
    # an array_3 with [h, w, c] where h is the number of pixels over
    # the height axis, w over the width axis and c is the number of
    # channels (3 for RGB images).

    # array [h]  # noqa
    ARRAY_1 = "array_1"
    # array [h, w]  # noqa
    ARRAY_2 = "array_2"
    # array [h, w, c]  # noqa
    ARRAY_3 = "array_3"


class ColumnRole(Enum):
    """
    Column role enum
    Describe the role of a column
    """

    INPUT = "input"
    INPUT_MASK = "input_mask"
    PREDICTION = "prediction"
    TARGET = "target"
    ERROR = "error"
    ID = "id"
    TIME_ID = "time_id"
    KPI = "kpi"
    INPUT_ADDITIONAL_EMBEDDING = "input_additional_embedding"
    TARGET_ADDITIONAL_EMBEDDING = "target_additional_embedding"
    PREDICTION_ADDITIONAL_EMBEDDING = "prediction_additional_embedding"


class TextLanguage(Enum):
    """Enumeration of text language used in nlp tasks.

    Fields
    ------

    ITALIAN
    ENGLISH
    MULTILANGUAGE
    """

    ITALIAN = "italian"
    ENGLISH = "english"
    MULTILANGUAGE = "multilanguage"
