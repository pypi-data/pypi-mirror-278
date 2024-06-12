import marshmallow as ma
from oarepo_model_builder.datatypes import ModelDataType


class RecordCommunitiesDataType(ModelDataType):
    model_type = "record-communities"

    class ModelSchema(ModelDataType.ModelSchema):
        type = ma.fields.Str(
            load_default="record-communities",
            required=False,
            validate=ma.validate.Equal("record-communities"),
        )

    def prepare(self, context):
        self.published_record = context["published_record"]
        self.draft_record = context["draft_record"]
        super().prepare(context)
