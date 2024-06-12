import marshmallow as ma
from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType, Section
from oarepo_model_builder.datatypes.components import DefaultsModelComponent
from oarepo_model_builder.datatypes.components.model.utils import set_default

from oarepo_model_builder_communities.profiles.record_communities import (
    RecordCommunitiesProfile,
)


def get_record_communities_schema():
    from ..communities import RecordCommunitiesDataType

    return RecordCommunitiesDataType.validator()


class RecordCommunitiesComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    affects = [DefaultsModelComponent]

    class ModelSchema(ma.Schema):
        record_communities = ma.fields.Nested(
            get_record_communities_schema,
            data_key="record-communities",
            attribute="record-communities",
        )

    def process_links(self, datatype, section: Section, **kwargs):
        if datatype.root.profile == "record_communities":
            section.config = {}

    def process_mb_invenio_drafts_parent_additional_fields(
        self, datatype, section: Section, **kwargs
    ):
        if (
            hasattr(datatype, "published_record")
            and "record-communities" in datatype.published_record.definition
        ):
            ctx = RecordCommunitiesProfile.get_default_profile_context(datatype.schema)
            record_communities_record = datatype.schema.get_schema_section(
                ctx["profile"], ctx["model_path"], prepare_context=ctx["context"]
            )
            communities_field = (
                "{{invenio_communities.records.records.systemfields.CommunitiesField}}"
            )
            communities_metadata_field = (
                "{{"
                + record_communities_record.definition["record-metadata"]["class"]
                + "}}"
            )
            context_cls = "{{oarepo_communities.records.systemfields.communities.OARepoCommunitiesFieldContext}}"

            workflow_metadata = (
                "{{"
                + record_communities_record.definition["workflow-metadata"]["class"]
                + "}}"
            )
            workflow_field = (
                "{{oarepo_communities.records.systemfields.workflow.WorkflowField}}"
            )
            obj = section.config.setdefault("additional-fields", {})
            obj |= {
                "communities": f"{communities_field}({communities_metadata_field}, context_cls={context_cls})",
                "workflow": f"{workflow_field}({workflow_metadata})",
            }

    def process_mb_invenio_drafts_parent_marshmallow(
        self, datatype, section: Section, **kwargs
    ):
        if (
            hasattr(datatype, "published_record")
            and "record-communities" in datatype.published_record.definition
        ):
            obj = section.config.setdefault("additional-fields", {})
            obj |= {
                "communities": "ma_fields.Nested({{oarepo_communities.schemas.parent.CommunitiesParentSchema}})"
            }

    def before_model_prepare(self, datatype, *, context, **kwargs):
        if datatype.root.profile == "record_communities":
            set_default(datatype, "search-options", {}).setdefault("skip", True)
            set_default(datatype, "permissions", {}).setdefault("skip", True)
            set_default(datatype, "record-item", {}).setdefault("skip", True)
            set_default(datatype, "record-list", {}).setdefault("skip", True)
