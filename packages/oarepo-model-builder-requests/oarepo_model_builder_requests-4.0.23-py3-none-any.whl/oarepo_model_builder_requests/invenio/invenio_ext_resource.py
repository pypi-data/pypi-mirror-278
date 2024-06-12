from oarepo_model_builder_requests.invenio.overriding_builder import OverridingBuilder


class InvenioRequestsExtResourceBuilder(OverridingBuilder):
    TYPE = "invenio_requests_ext_resource"
    section = "ext"
    template = "requests-ext-resource"
    overriden_sections = {
        "resource": "requests.resource",
        "service": "requests.service",
    }

    def finish(self, **extra_kwargs):
        ext = self.current_model.section_requests_ext_resource.config
        super().finish(ext=ext, **extra_kwargs)
