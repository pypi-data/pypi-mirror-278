from StudioPulse.app.models.search_filter_group import SearchFilterGroup

from StudioPulse.app.blueprints.crud.base import BaseModelResource, BaseModelsResource


class SearchFilterGroupsResource(BaseModelsResource):
    def __init__(self):
        BaseModelsResource.__init__(self, SearchFilterGroup)


class SearchFilterGroupResource(BaseModelResource):
    def __init__(self):
        BaseModelResource.__init__(self, SearchFilterGroup)
