from sqlalchemy.dialects.postgresql import JSONB

from StudioPulse.app import db
from StudioPulse.app.models.serializer import SerializerMixin
from StudioPulse.app.models.base import BaseMixin


class DataImportError(db.Model, BaseMixin, SerializerMixin):
    """
    Table to allow the storage of import errors.
    """

    event_data = db.Column(JSONB, nullable=False)
    source = db.Column(db.Enum("csv", "shotgun", name="import_source_enum"))
