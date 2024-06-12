import marshmallow as ma
from oarepo_model_builder.datatypes import DataTypeComponent, ModelDataType, Section
from oarepo_model_builder.datatypes.components import (
    DefaultsModelComponent,
    MarshmallowModelComponent,
)
from oarepo_model_builder.datatypes.components.model.blueprints import BlueprintSchema
from oarepo_model_builder.datatypes.components.model.resource import ResourceClassSchema
from oarepo_model_builder.datatypes.components.model.service import ServiceClassSchema
from oarepo_model_builder.datatypes.components.model.utils import set_default
from oarepo_model_builder.datatypes.model import Link
from oarepo_model_builder.utils.camelcase import camel_case, snake_case
from oarepo_model_builder.utils.links import url_prefix2link
from oarepo_model_builder.utils.python_name import (
    Import,
    convert_config_to_qualified_name,
)
from oarepo_model_builder.validation.utils import ImportSchema


class RequestActionSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    module = ma.fields.String(metadata={"doc": "Class module"})
    class_ = ma.fields.String(
        attribute="class",
        data_key="class",
    )
    generate = ma.fields.Bool()
    base_classes = ma.fields.List(
        ma.fields.Str(),
        attribute="base-classes",
        data_key="base-classes",
        metadata={"doc": "Request action base classes"},
    )
    # module = ma.fields.String(metadata={"doc": "Class module"})
    imports = ma.fields.List(
        ma.fields.Nested(ImportSchema), metadata={"doc": "List of python imports"}
    )


class RequestTypeSchema(ma.Schema):
    class Meta:
        unknown = ma.RAISE

    module = ma.fields.String(metadata={"doc": "Class module"})
    class_ = ma.fields.String(
        attribute="class",
        data_key="class",
    )
    generate = ma.fields.Bool()
    base_classes = ma.fields.List(
        ma.fields.Str(),
        attribute="base-classes",
        data_key="base-classes",
        metadata={"doc": "RequestType base classes"},
    )
    imports = ma.fields.List(
        ma.fields.Nested(ImportSchema), metadata={"doc": "List of python imports"}
    )
    allowed_receiver_ref_types = ma.fields.List(
        ma.fields.String,
        attribute="allowed-receiver-ref-types",
        data_key="allowed-receiver-ref-types",
    )
    allowed_receiver_topic_types = ma.fields.List(
        ma.fields.String,
        attribute="allowed-receiver-topic-types",
        data_key="allowed-receiver-topic-types",
    )
    needs_context = ma.fields.Dict(
        keys=ma.fields.String,
        values=ma.fields.String,
        attribute="needs-context",
        data_key="needs-context",
    )
    actions = ma.fields.Dict(
        keys=ma.fields.Str(), values=ma.fields.Nested(RequestActionSchema)
    )
    id_ = ma.fields.String(attribute="id", data_key="id")


class RequestsSchema(ma.Schema):
    types = ma.fields.Dict(
        keys=ma.fields.Str(),
        values=ma.fields.Nested(RequestTypeSchema),
    )
    api_blueprint = ma.fields.Nested(
        BlueprintSchema,
        attribute="api-blueprint",
        data_key="api-blueprint",
        metadata={"doc": "API blueprint details"},
    )
    app_blueprint = ma.fields.Nested(
        BlueprintSchema,
        attribute="app-blueprint",
        data_key="app-blueprint",
        metadata={"doc": "API blueprint details"},
    )
    service = ma.fields.Nested(
        ServiceClassSchema, metadata={"doc": "Requests service settings"}
    )
    resource = ma.fields.Nested(
        ResourceClassSchema, metadata={"doc": "Requests resource settings"}
    )
    additional_resolvers = ma.fields.List(
        ma.fields.String(),
        attribute="additional-resolvers",
        data_key="additional-resolvers",
        metadata={"doc": "Entity resolvers other than the ones generated with model"},
    )
    additional_ui_resolvers = ma.fields.Dict(
        keys=ma.fields.String(),
        values=ma.fields.String(),
        attribute="additional-ui-resolvers",
        data_key="additional-ui-resolvers",
        metadata={
            "doc": "Entity ui resolvers other than the ones generated with model"
        },
    )
    ui_serialization_referenced_fields = ma.fields.List(
        ma.fields.Str(),
        attribute="ui-serialization-referenced-fields",
        data_key="ui-serialization-referenced-fields",
        metadata={"doc": "List of field names resolved during ui serialization"},
    )


class RequestsComponent(DataTypeComponent):
    eligible_datatypes = [ModelDataType]
    depends_on = [DefaultsModelComponent, MarshmallowModelComponent]

    class ModelSchema(ma.Schema):
        requests = ma.fields.Nested(RequestsSchema)

    def process_requests_ext_resource(self, datatype, section, **kwargs):
        cfg = section.config
        cfg["ext-service-name"] = "service_requests"
        cfg["ext-resource-name"] = "resource_requests"

    def process_links(self, datatype, section: Section, **kwargs):
        url_prefix = url_prefix2link(datatype.definition["resource-config"]["base-url"])
        if datatype.root.profile == "record":
            section.config["links_item"] += [
                Link(
                    name="requests",
                    link_class="ConditionalLink",
                    link_args=[
                        "cond=is_published_record",
                        f'if_=RecordLink("{{+api}}{url_prefix}{{id}}/requests")',
                        f'else_=RecordLink("{{+api}}{url_prefix}{{id}}/draft/requests")',
                    ],
                    imports=[
                        Import("invenio_records_resources.services.ConditionalLink"),
                        Import("invenio_records_resources.services.RecordLink"),
                        Import("oarepo_runtime.records.is_published_record"),
                    ],
                ),
            ]

    def before_model_prepare(self, datatype, *, context, **kwargs):
        module = datatype.definition["module"]["qualified"]
        profile_module = context["profile_module"]

        requests = set_default(datatype, "requests", {})
        request_types = requests.setdefault("types", {})

        for request_name, request_type_data in request_types.items():
            request_module = f"{module}.{profile_module}.requests.{snake_case(request_name).replace('-', '_')}"
            request_type_module = request_type_data.setdefault(
                "module", f"{request_module}.types"
            )
            request_type_data.setdefault(
                "class",
                f"{request_type_module}.{camel_case(request_name)}RequestType",
            )
            request_type_data.setdefault("generate", True)
            request_type_data.setdefault(
                "base-classes", ["oarepo_requests.types.generic.OARepoRequestType"]
            )  # accept action
            request_type_data.setdefault(
                "id",
                f"{snake_case(datatype.definition['model-name']).replace('-', '_')}_{snake_case(request_name).replace('-', '_')}",
            )
            request_actions = request_type_data.setdefault("actions", {})
            for action_name, action_input_data in request_actions.items():
                request_action_module = action_input_data.setdefault(
                    "module", f"{request_module}.actions"
                )
                action_input_data.setdefault(
                    "class",
                    f"{request_action_module}.{camel_case(request_name)}RequestAcceptAction",
                )
                action_input_data.setdefault("generate", True)
                action_input_data.setdefault(
                    "base-classes", ["invenio_requests.customizations.AcceptAction"]
                )  # accept action
                action_input_data.setdefault("imports", [])

        requests_module = "requests"
        record_requests_config_cls = (
            "oarepo_requests.resources.draft.config.DraftRecordRequestsResourceConfig"
        )

        alias = datatype.definition["module"]["alias"]
        requests_alias = f"{alias}_requests"
        module = datatype.definition["module"]["qualified"]

        api = requests.setdefault("api-blueprint", {})
        api.setdefault("generate", True)
        api.setdefault("alias", requests_alias)
        # api.setdefault("extra_code", "")
        api_module = api.setdefault(
            "module",
            f"{module}.views.{requests_module}.api",
        )
        api.setdefault(
            "function",
            f"{api_module}.create_api_blueprint",
        )
        api.setdefault("imports", [])
        convert_config_to_qualified_name(api, name_field="function")

        app = requests.setdefault("app-blueprint", {})
        app.setdefault("generate", True)
        app.setdefault("alias", requests_alias)
        app.setdefault("extra_code", "")
        ui_module = app.setdefault(
            "module",
            f"{module}.views.{requests_module}.app",
        )
        app.setdefault(
            "function",
            f"{ui_module}.create_app_blueprint",
        )
        app.setdefault("imports", [])
        convert_config_to_qualified_name(app, name_field="function")

        module_container = datatype.definition["module"]
        resource = requests.setdefault("resource", {})
        resource.setdefault("generate", True)
        resource.setdefault(
            "config-key",
            f"{module_container['base-upper']}_{requests_module.upper()}_RESOURCE_CLASS",
        )
        resource.setdefault(
            "class",
            f"oarepo_requests.resources.draft.resource.DraftRecordRequestsResource",
        )

        resource.setdefault(
            "additional-args",
            [
                "record_requests_config={{" + record_requests_config_cls + "}}()",
            ],
        )
        resource.setdefault("skip", False)

        service = requests.setdefault("service", {})

        service.setdefault("generate", True)
        service.setdefault(
            "config-key",
            f"{module_container['base-upper']}_{requests_module.upper()}_SERVICE_CLASS",
        )
        service.setdefault(
            "class",
            f"oarepo_requests.services.draft.service.DraftRecordRequestsService",
        )
        service.setdefault(
            "additional-args",
            [
                f"record_service=self.service_records",
                "oarepo_requests_service={{oarepo_requests.proxies.current_oarepo_requests_service}}",
            ],
        )
        service.setdefault("skip", False)

        requests.setdefault(
            "additional-resolvers",
            [
                "{{oarepo_runtime.records.entity_resolvers.UserResolver}}()",
                "{{oarepo_runtime.records.entity_resolvers.GroupResolver}}()",
            ],
        )
        requests.setdefault(
            "additional-ui-resolvers",
            {
                '"user"': '{{oarepo_requests.resolvers.ui.UserEntityReferenceUIResolver}}("user")',
                '"fallback"': '{{oarepo_requests.resolvers.ui.FallbackEntityReferenceUIResolver}}("fallback")',
                '"group"': '{{oarepo_requests.resolvers.ui.GroupEntityReferenceUIResolver}}("group")',
            },
        )
        requests.setdefault(
            "ui-serialization-referenced-fields",
            ['"created_by"', '"receiver"', '"topic"'],
        )
