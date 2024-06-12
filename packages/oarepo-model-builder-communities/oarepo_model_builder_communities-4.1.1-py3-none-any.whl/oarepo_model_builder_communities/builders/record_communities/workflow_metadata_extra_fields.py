from oarepo_model_builder_requests.invenio.overriding_builder import OverridingBuilder


class WorkflowMetadataExtraFieldsBuilder(OverridingBuilder):
    TYPE = "workflow_metadata_extra_fields"
    section = "workflow-metadata"
    template = "record-metadata-extra-fields"
    overriden_sections = {"record-metadata": "workflow-metadata"}

    def finish(self, **extra_kwargs):
        super().finish(
            published_record=self.current_model.published_record, **extra_kwargs
        )
