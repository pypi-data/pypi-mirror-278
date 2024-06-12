from typing import Dict

from oarepo_model_builder.datatypes.components.model.ui_marshmallow import (
    UIMarshmallowModelComponent,
)
from oarepo_model_builder.datatypes.components.model.utils import set_default

from ... import RecordCommunitiesDataType


class RecordCommunitiesUIMarshmallowModelComponent(UIMarshmallowModelComponent):
    eligible_datatypes = [RecordCommunitiesDataType]
    dependency_remap = UIMarshmallowModelComponent

    def before_model_prepare(self, datatype, **kwargs):
        marshmallow: Dict = set_default(datatype, "ui", "marshmallow", {})
        marshmallow.setdefault("generate", False)
        marshmallow.setdefault(
            "class",
            f"oarepo_communities.services.record_communities.schema.RecordCommunitiesSchema",
        )
        super().before_model_prepare(datatype, **kwargs)
