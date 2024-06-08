from typing import List, Dict, Union

class VizportalRequestOptions:
    class Operator:
        Equals: str = "eq"
        GreaterThan: str = "gt"
        GreaterThanOrEqual: str = "gte"
        LessThan: str = "lt"
        LessThanOrEqual: str = "lte"
        In: str = "in"
        Has: str = "has"

    class Field:
        Args: str = "args"
        CompletedAt: str = "completedAt"
        CreatedAt: str = "createdAt"
        DomainName: str = "domainName"
        DomainNickname: str = "domainNickname"
        HitsTotal: str = "hitsTotal"
        IsLocal: str = "isLocal"
        JobType: str = "jobType"
        LastLogin: str = "lastLogin"
        MinimumSiteRole: str = "minimumSiteRole"
        Name: str = "name"
        Notes: str = "notes"
        OwnerDomain: str = "ownerDomain"
        OwnerEmail: str = "ownerEmail"
        OwnerName: str = "ownerName"
        ParentProjectId: str = "parentProjectId"
        Progress: str = "progress"
        ProjectName: str = "projectName"
        PublishSamples: str = "publishSamples"
        SiteRole: str = "siteRole"
        StartedAt: str = "startedAt"
        Status: str = "status"
        Subtitle: str = "subtitle"
        Tags: str = "tags"
        Title: str = "title"
        TopLevelProject: str = "topLevelProject"
        Type: str = "type"
        UpdatedAt: str = "updatedAt"
        UserCount: str = "userCount"
        HasAlert: str = "hasAlert"
        OwnerId: str = "ownerId"
        ServerName: str = "serverName"
        IsDefaultPort: str = "isDefaultPort"
        DatabaseUsername: str = "databaseUsername"
        HasEmbeddedPassword: str = "hasEmbeddedPassword"
        IsFavorite: str = "isFavorite"
        ExtractStatus: str = "extractStatus"
        IsCertified: str = "isCertified"
        IsPublished: str = "isPublished"
        WorkbookConnFilter: str = "workbookConnFilter"
        TopLevelProject: str = "topLevelProject"
        TaskType: str = "taskType"
        ContentType: str = "contentType"

    class Direction:
        Descending: str = "descending"
        Ascending: str = "ascending"

    class StatField:
        HitsTotal: str = "hitsTotal"
        FavoritesTotal: str = "favoritesTotal"
        HitsLastOneMonthTotal: str = "hitsLastOneMonthTotal"
        HitsLastThreeMonthsTotal: str = "hitsLastThreeMonthsTotal"
        HitsLastTwelveMonthsTotal: str = "hitsLastTwelveMonthsTotal"
        SubscriptionsTotal: str = "subscriptionsTotal"
        ConnectedWorkbooksCount: str = "connectedWorkbooksCount"

    class DatasourceType:
        Extract: str = "extract"
        Live: str = "live"
        LiveConnection: str = "liveConnection"

    class ContentType:
        Workbook: str = "workbook"
        Datasource: str = "datasource"
        Project: str = "project"
        View: str = "view"
        User: str = "user"
        Site: str = "site"
        Server: str = "server"
        Group: str = "group"
        Job: str = "job"
        Task: str = "task"
        DataRole: str = "dataRole"
        Lens: str = "lens"
        Flow: str = "flow"
        Metric: str = "metric"
        VirtualConnection: str = "virtualConnection"

    class TaskType:
        Extract: str = "extract"
        Refresh: str = "refresh"
        Schedule: str = "schedule"
        Subscription: str = "subscription"
        Sync: str = "sync"
        Webhook: str = "webhook"

    class SiteRole:
        Unlicensed: str = "Unlicensed"
        Guest: str = "Guest"
        Interactor: str = "Interactor"
        Explorer: str = "Explorer"
        Publisher: str = "Publisher"
        Creator: str = "Creator"
        Viewer: str = "Viewer"
        SiteAdministrator: str = "SiteAdministrator"
        SiteAdministratorCreator: str = "SiteAdministratorCreator"
        SiteAdministratorExplorer: str = "SiteAdministratorExplorer"
        SupportUser: str = "SupportUser"
        ServerAdministrator: str = "ServerAdministrator"
        ExplorerCanPublish: str = "ExplorerCanPublish"

    class DatasourceType:
        Live: str = "live"
        Published: str = "published"
        AllExtracts: str = "allExtracts"
        UnencryptedExtracts: str = "unencryptedExtracts"
        EncryptedExtracts: str = "encryptedExtracts"

class StatFieldBuilder:
    def __init__(self):
        self.stat_fields: List[str] = []

    @staticmethod
    def default() -> List[str]:
        return [
            "hitsTotal",
            "favoritesTotal",
            "hitsLastOneMonthTotal",
            "hitsLastThreeMonthsTotal",
            "hitsLastTwelveMonthsTotal",
            "subscriptionsTotal",
        ]

    def add_stat_field(self, stat_field: str):
        self.stat_fields.append(stat_field)

    def add_stat_fields(self, stat_fields: List[str]):
        self.stat_fields.extend(stat_fields)

    def build(self) -> List[str]:
        return self.stat_fields


class FilterClauseBuilder:
    def __init__(self, operator: str = "and"):
        self.operator = operator
        self._clauses = []

    @property
    def clauses(self) -> Dict[str, Union[str, List[Dict[str, str]]]]:
        return {"operator": self.operator, "clauses": self._clauses}

    def add_clause(self, operator: str, field: str, value: str):
        self._clauses.append({"operator": operator, "field": field, "value": value})


class SortBuilder:
    def __init__(
        self, field: str = None, direction: str = None, sort_dict: Dict[str, str] = None
    ):
        self._sorts = []
        self.sort_dict = sort_dict
        self.field = field
        self.direction = direction

        # If field and direction are provided, add the sort.
        if field and direction:
            self.add_sort(field, direction)
        # If sort_dict is provided, add the sort.
        elif sort_dict and isinstance(sort_dict, dict):
            if sort_dict.get("field") and sort_dict.get("direction"):
                self.add_sort(sort_dict["field"], sort_dict["direction"])

    @property
    def sorts(self) -> List[Dict[str, Union[str, bool]]]:
        return self._sorts

    def add_sort(self, field: str, direction: str):
        if direction.lower() not in ["asc", "desc", "ascending", "descending"]:
            raise ValueError("Direction must be either 'asc', 'desc', 'ascending' or 'descending'.")

        self._sorts.append({"field": field, "ascending": direction.lower() in ["asc", "ascending"]})
