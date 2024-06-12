from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class RecordCommunitiesViewsBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "record_communities_views"
    template = "record-communities-views"
    section = "api-blueprint"

    def finish(self, **extra_kwargs):
        super().finish(
            published_record=self.current_model.published_record, **extra_kwargs
        )
