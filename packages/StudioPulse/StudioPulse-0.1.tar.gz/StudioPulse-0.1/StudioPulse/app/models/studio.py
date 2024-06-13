from StudioPulse.app import db
from StudioPulse.app.models.serializer import SerializerMixin
from StudioPulse.app.models.base import BaseMixin


class StudioPulse(db.Model, BaseMixin, SerializerMixin):
    """
    Describe a StudioPulse.
    """

    name = db.Column(db.String(80), unique=True, nullable=False)
    color = db.Column(db.String(7), nullable=False)
    archived = db.Column(db.Boolean(), default=False)
