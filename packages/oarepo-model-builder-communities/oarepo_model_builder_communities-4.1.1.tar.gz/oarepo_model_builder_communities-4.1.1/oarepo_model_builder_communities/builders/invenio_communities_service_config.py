from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class InvenioCommunitiesServiceConfigBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "invenio_communities_record_service_config"
    section = "service-config"
    template = "drafts-record-service-config"

    def finish(self, **extra_kwargs):
        super().finish(
            published_record=self.current_model,
            draft_record=self.current_model.draft_record,
            **extra_kwargs,
        )
