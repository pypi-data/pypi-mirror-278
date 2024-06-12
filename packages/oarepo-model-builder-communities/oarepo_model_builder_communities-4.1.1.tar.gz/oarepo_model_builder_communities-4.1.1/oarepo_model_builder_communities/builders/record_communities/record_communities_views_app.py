from oarepo_model_builder.invenio.invenio_base import InvenioBaseClassPythonBuilder


class RecordCommunitiesViewsAppBuilder(InvenioBaseClassPythonBuilder):
    TYPE = "record_communities_views_app"
    template = "record-communities-views"
    section = "app-blueprint"

    def finish(self, **extra_kwargs):
        super().finish(
            published_record=self.current_model.published_record, **extra_kwargs
        )
