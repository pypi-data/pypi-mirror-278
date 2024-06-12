from typing import Literal


class Endpoints:
    """Endpoints for the Vizportal API"""

    class Get:
        """Endpoints for GET requests"""

        Workbooks: Literal["getWorkbooks"] = "getWorkbooks"
        Workbook: Literal["getWorkbook"] = "getWorkbook"
        Datasource: Literal["getDatasource"] = "getDatasource"
        Datasources: Literal["getDatasources"] = "getDatasources"
        Projects: Literal["getProjects"] = "getProjects"
        User: Literal["getUser"] = "getUser"
        Users: Literal["getUsers"] = "getUsers"
        Group: Literal["getGroup"] = "getGroup"
        Groups: Literal["getGroups"] = "getGroups"
        View: Literal["getView"] = "getView"
        Views: Literal["getViews"] = "getViews"
        Favorites: Literal["getFavorites"] = "getFavorites"
        Flow: Literal["getFlow"] = "getFlow"
        Flows: Literal["getFlows"] = "getFlows"
        Metrics: Literal["getMetrics"] = "getMetrics"
        Schedule: Literal["getSchedule"] = "getSchedule"
        Schedules: Literal["getSchedules"] = "getSchedules"
        Lenses: Literal["getLenses"] = "getLenses"
        Subscriptions: Literal["getSubscriptions"] = "getSubscriptions"
        DataRoles: Literal["getDataRoles"] = "getDataRoles"
        DetailedRecents: Literal["getDetailedRecents"] = "getDetailedRecents"
        Recommendations: Literal["getRecommendations"] = "getRecommendations"
        DataConnections: Literal["getDataConnections"] = "getDataConnections"
        BackgroundJobs: Literal["getBackgroundJobs"] = "getBackgroundJobs"
        ContentForUser: Literal["getContentForUser"] = "getContentForUser"
        PersonalAccessTokenNames: Literal["getPersonalAccessTokenNames"] = (
            "getPersonalAccessTokenNames"
        )
        SiteUsers: Literal["getSiteUsers"] = "getSiteUsers"
        UsersGroupMembership: Literal["getUsersGroupMembership"] = (
            "getUsersGroupMembership"
        )
        Sites: Literal["getSites"] = "getSites"
        Site: Literal["getSite"] = "getSite"
        Task: Literal["getTask"] = "getTask"
        Tasks: Literal["getTasks"] = "getTasks"
        Webhook: Literal["getWebhook"] = "getWebhook"
        Webhooks: Literal["getWebhooks"] = "getWebhooks"
        Alert: Literal["getAlert"] = "getAlert"
        Alerts: Literal["getAlerts"] = "getAlerts"
        ViewByPath: Literal["getViewByPath"] = "getViewByPath"
        ViewActions: Literal["getViewActions"] = "getViewActions"
        UsersGroupMembership: Literal["getUsersGroupMembership"] = (
            "getUsersGroupMembership"
        )
        Tags: Literal["getTags"] = "getTags"
        ExplicitPermissions: Literal["getExplicitPermissions"] = (
            "getExplicitPermissions"
        )
        UserSettings: Literal["getUserSettings"] = "getUserSettings"
        SiteSettings: Literal["getSiteSettings"] = "getSiteSettings"
        ServerSettings: Literal["getServerSettings"] = "getServerSettings"
        ServerSettingsUnauthenticated: Literal["getServerSettingsUnauthenticated"] = (
            "getServerSettingsUnauthenticated"
        )
        ServerInfo: Literal["getServerInfo"] = "getServerInfo"
        ServerVersion: Literal["getServerVersion"] = "getServerVersion"
        ServerStatus: Literal["getServerStatus"] = "getServerStatus"
        ProjectActions: Literal["getProjectActions"] = "getProjectActions"
        Project: Literal["getProject"] = "getProject"
        ProjectNames: Literal["getProjectNames"] = "getProjectNames"
        ProjectPermissions: Literal["getProjectPermissions"] = "getProjectPermissions"
        LastActiveDirectoryGroupSyncTime: Literal[
            "getLastActiveDirectoryGroupSyncTime"
        ] = "getLastActiveDirectoryGroupSyncTime"
        Comments: Literal["getComments"] = "getComments"
        SessionInfo: Literal["getSessionInfo"] = "getSessionInfo"
        SharedWithMe: Literal["getSharedWithMe"] = "getSharedWithMe"
        CustomizedViews: Literal["getCustomizedViews"] = "getCustomizedViews"
        AccelerationRecommendations: Literal["getAccelerationRecommendations"] = (
            "getAccelerationRecommendations"
        )
        NotificationEnabledSettingsForUser: Literal[
            "getNotificationEnabledSettingsForUser"
        ] = "getNotificationEnabledSettingsForUser"
        MarkAnimationEnabledSetting: Literal["getMarkAnimationEnabledSetting"] = (
            "getMarkAnimationEnabledSetting"
        )
        Languages: Literal["getLanguages"] = "getLanguages"
        Locales: Literal["getLocales"] = "getLocales"
        UserSelectableTimeZones: Literal["getUserSelectableTimeZones"] = (
            "getUserSelectableTimeZones"
        )
        UserRefreshTokenCount: Literal["getUserRefreshTokenCount"] = (
            "getUserRefreshTokenCount"
        )
        LocalAuthenticationConfiguration: Literal[
            "getLocalAuthenticationConfiguration"
        ] = "getLocalAuthenticationConfiguration"
        Databases: Literal["getDatabases"] = "getDatabases"
        Tables: Literal["getTables"] = "getTables"


    class Explore:
        FavoriteContentForUser: Literal["favoriteContentForUser"] = (
            "exploreFavoriteContentForUser"
        )

    class Update:
        """Endpoints for UPDATE requests"""

        Workbook: Literal["updateWorkbook"] = "updateWorkbook"
        Datasource: Literal["updateDatasource"] = "updateDatasource"
        Project: Literal["updateProject"] = "updateProject"
        Group: Literal["updateGroup"] = "updateGroup"
        User: Literal["updateUser"] = "updateUser"
        Site: Literal["updateSite"] = "updateSite"
        Flow: Literal["updateFlow"] = "updateFlow"
        UserStartPage: Literal["updateUserStartPage"] = "updateUserStartPage"
        UserGroupMembership: Literal["updateUserGroupMembership"] = (
            "updateUserGroupMembership"
        )
        UsersSiteRole: Literal["updateUsersSiteRole"] = "updateUsersSiteRole"
        UserEmail: Literal["updateUserEmail"] = "updateUserEmail"
        ProjectDescription: Literal["updateProjectDescription"] = (
            "updateProjectDescription"
        )
        ProjectOwner: Literal["updateProjectOwner"] = "updateProjectOwner"
        ProjectParent: Literal["updateProjectParent"] = "updateProjectParent"
        ProjectTags: Literal["updateProjectTags"] = "updateProjectTags"
        ProjectPermissions: Literal["updateProjectPermissions"] = (
            "updateProjectPermissions"
        )
        Connections: Literal["updateConnections"] = "updateConnections"
        UserLanguage: Literal["updateUserLanguage"] = "updateUserLanguage"

    class Create:
        """Endpoints for CREATE requests"""

        CreateProject: Literal["createProject"] = "createProject"
        CreateGroup: Literal["createGroup"] = "createGroup"
        CreateUser: Literal["createUser"] = "createUser"
        PublishWorkbook: Literal["publishWorkbook"] = "publishWorkbook"
        PublishDatasource: Literal["publishDatasource"] = "publishDatasource"
        PublishFlow: Literal["publishFlow"] = "publishFlow"
        PublicKey: Literal["generatePublicKey"] = "generatePublicKey"
        Commonet: Literal["createComment"] = "createComment"
        ExtractTasks: Literal["createExtractTasks"] = "createExtractTasks"

    class Add:
        """Endpoints for ADD requests"""

        Favorite: Literal["addFavorite"] = "addFavorite"
        TagsToDatasources: Literal["addTagsToDatasources"] = "addTagsToDatasources"
        TagsToViews: Literal["addTagsToViews"] = "addTagsToViews"
        TagsToWorkbooks: Literal["addTagsToWorkbooks"] = "addTagsToWorkbooks"

    class Delete:
        """Endpoints for DELETE requests"""

        WorkbookVersions: Literal["deleteWorkbookVersions"] = "deleteWorkbookVersions"
        UserRefreshTokens: Literal["deleteUserRefreshTokens"] = (
            "deleteUserRefreshTokens"
        )
        TagsFromWorkbooks: Literal["removeTagsFromWorkbooks"] = (
            "removeTagsFromWorkbooks"
        )
        Comment: Literal["deleteComment"] = "deleteComment"

    class Move:
        """Endpoints for MOVE requests"""

        MoveWorkbooksToProject: Literal["moveWorkbooksToProject"] = (
            "moveWorkbooksToProject"
        )

    class Set:
        """Endpoints for SET requests"""

        WorkbooksOwner: Literal["setWorkbooksOwner"] = "setWorkbooksOwner"
        WorkbookDescription: Literal["setWorkbookDescription"] = (
            "setWorkbookDescription"
        )
        DisplayTabs: Literal["setDisplayTabs"] = "setDisplayTabs"
        ExtractTaskPriority: Literal["setExtractTaskPriority"] = (
            "setExtractTaskPriority"
        )
        ExtractTasksSchedule: Literal["setExtractTasksSchedule"] = (
            "setExtractTasksSchedule"
        )

    class Check:
        PersonalAccessTokenCreationIsAllowed: Literal[
            "checkPersonalAccessTokenCreationIsAllowed"
        ] = "checkPersonalAccessTokenCreationIsAllowed"

        CheckConnection: Literal["checkConnection"] = "checkConnection"
