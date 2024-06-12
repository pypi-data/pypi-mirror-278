from oarepo_model_builder.datatypes import DataTypeComponent
from oarepo_model_builder.datatypes.components.model.search_options import (
    SearchOptionsModelComponent,
)
from oarepo_model_builder.datatypes.components.model.utils import set_default

from oarepo_model_builder_communities.datatypes import RecordCommunitiesDataType


class RecordCommunitiesSearchOptionsModelComponent(DataTypeComponent):
    eligible_datatypes = [RecordCommunitiesDataType]
    affects = [SearchOptionsModelComponent]

    def before_model_prepare(self, datatype, *, context, **kwargs):
        record_search_options = set_default(datatype, "search-options", {})
        record_search_options.setdefault(
            "class", datatype.published_record.definition["search-options"]["class"]
        )
