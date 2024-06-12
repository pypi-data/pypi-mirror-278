from oarepo_model_builder.datatypes import DataTypeComponent
from oarepo_model_builder.datatypes.components.model.defaults import (
    DefaultsModelComponent,
)
from oarepo_model_builder.datatypes.components.model.record import RecordModelComponent
from oarepo_model_builder.datatypes.components.model.utils import set_default
from oarepo_model_builder.utils.python_name import parent_module

from oarepo_model_builder_communities.datatypes import RecordCommunitiesDataType


class WorkflowMetadataModelComponent(DataTypeComponent):
    eligible_datatypes = [RecordCommunitiesDataType]
    depends_on = [DefaultsModelComponent, RecordModelComponent]

    def before_model_prepare(self, datatype, context, **kwargs):
        published = datatype.published_record
        records_module = parent_module(published.definition["record"]["module"])
        prefix = published.definition["module"]["prefix"]
        alias = published.definition["module"]["alias"]

        metadata = set_default(datatype, "workflow-metadata", {})
        metadata.setdefault("generate", True)
        metadata_module = metadata.setdefault("module", f"{records_module}.models")
        metadata.setdefault("class", f"{metadata_module}.{prefix}WorkflowMetadata")
        metadata.setdefault(
            "base-classes",
            [
                "invenio_db.db{db.Model}",
                "oarepo_communities.records.models.RecordWorkflowModelMixin",
            ],
        )
        metadata.setdefault("extra-code", "")
        metadata.setdefault(
            "imports",
            [],
        )
        metadata.setdefault(
            "table",
            f"{published.definition['module']['prefix-snake']}_workflow_metadata",
        )
        metadata.setdefault("alias", alias)
        metadata.setdefault("use-versioning", False)
