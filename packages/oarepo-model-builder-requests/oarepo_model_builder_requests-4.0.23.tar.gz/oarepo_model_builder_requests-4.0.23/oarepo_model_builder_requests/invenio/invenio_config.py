from oarepo_model_builder_requests.invenio.overriding_builder import OverridingBuilder


class InvenioConfigBuilder(OverridingBuilder):
    TYPE = "invenio_requests_config"
    section = "config"
    template = "config"
    overriden_sections = {
        "resource": "requests.resource",
        "service": "requests.service",
    }
