from StudioPulse.app.models.StudioPulse import StudioPulse

from StudioPulse.app.blueprints.crud.base import BaseModelsResource, BaseModelResource

from StudioPulse.app.services import tasks_service


class StudioPulsesResource(BaseModelsResource):
    def __init__(self):
        BaseModelsResource.__init__(self, StudioPulse)

    def check_read_permissions(self):
        return True

    def post_creation(self, instance):
        tasks_service.clear_StudioPulse_cache(str(instance.id))
        return instance.serialize()


class StudioPulseResource(BaseModelResource):
    def __init__(self):
        BaseModelResource.__init__(self, StudioPulse)

    def check_read_permissions(self, instance):
        return True

    def post_update(self, instance_dict, data):
        tasks_service.clear_StudioPulse_cache(instance_dict["id"])
        return instance_dict

    def post_delete(self, instance_dict):
        tasks_service.clear_StudioPulse_cache(instance_dict["id"])
        return instance_dict
