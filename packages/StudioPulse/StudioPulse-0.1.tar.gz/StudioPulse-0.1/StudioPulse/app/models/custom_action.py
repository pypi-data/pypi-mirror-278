from StudioPulse.app import db
from StudioPulse.app.models.serializer import SerializerMixin
from StudioPulse.app.models.base import BaseMixin


class CustomAction(db.Model, BaseMixin, SerializerMixin):
    """
    Custom actions are HTTP links that can be activated outside of the API.
    They are mainly aimed at being used by the web frontend to allow StudioPulse
    to make custom HTTP calls.
    """

    name = db.Column(db.String(80), nullable=False)
    url = db.Column(db.String(400))
    entity_type = db.Column(db.String(40), default="all")
    is_ajax = db.Column(db.Boolean(), default=False)
