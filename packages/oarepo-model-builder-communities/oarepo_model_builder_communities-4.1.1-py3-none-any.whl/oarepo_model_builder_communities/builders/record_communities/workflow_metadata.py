from oarepo_model_builder_requests.invenio.overriding_builder import OverridingBuilder


class WorkflowMetadataBuilder(OverridingBuilder):
    TYPE = "workflow_metadata"
    section = "workflow-metadata"
    template = "record-metadata"
    overriden_sections = {"record-metadata": "workflow-metadata"}
