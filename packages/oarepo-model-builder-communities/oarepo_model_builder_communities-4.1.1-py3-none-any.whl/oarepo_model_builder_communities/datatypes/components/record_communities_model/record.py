from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
from oarepo_model_builder.datatypes.components import RecordModelComponent
from oarepo_model_builder.datatypes.components.model.utils import set_default

from oarepo_model_builder_communities.datatypes import RecordCommunitiesDataType


class CommunityRecordModelComponent(RecordModelComponent):
    eligible_datatypes = [RecordCommunitiesDataType]
    dependency_remap = RecordModelComponent

    def before_model_prepare(self, datatype, *, context, **kwargs):
        record = set_default(datatype, "record", {})
        record.setdefault(
            "class", f"{context['published_record'].definition['record']['class']}"
        )
        super().before_model_prepare(datatype, context=context, **kwargs)


class RecordExtraFieldsModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    affects = [RecordModelComponent]

    def before_model_prepare(self, datatype, *, context, **kwargs):

        if datatype.root.profile == "record":
            record = set_default(datatype, "record", {})
            fields = record.setdefault("fields", {})
            fields["status"] = (
                "{{oarepo_communities.records.systemfields.status.RecordStatusField}}(initial='published')"
            )
        if datatype.root.profile == "draft":
            record = set_default(datatype, "record", {})
            fields = record.setdefault("fields", {})
            fields["status"] = (
                "{{oarepo_communities.records.systemfields.status.RecordStatusField}}()"
            )
