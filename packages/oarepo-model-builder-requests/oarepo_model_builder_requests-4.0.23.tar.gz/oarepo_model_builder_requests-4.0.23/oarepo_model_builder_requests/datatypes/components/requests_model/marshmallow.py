from typing import Dict

from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType
from oarepo_model_builder.datatypes.components.model.marshmallow import (
    MarshmallowModelComponent,
)
from oarepo_model_builder.datatypes.components.model.utils import set_default


class RequestsMarshmallowModelComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [MarshmallowModelComponent]

    def before_model_prepare(self, datatype, *, context, **kwargs):
        marshmallow: Dict = set_default(datatype, "marshmallow", {})
        marshmallow.get("base-classes", []).insert(
            0, "oarepo_requests.services.schema.RequestsSchemaMixin"
        )
