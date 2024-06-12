from oarepo_model_builder_requests.invenio.overriding_builder import OverridingBuilder


class RequestsAPIViewsBuilder(OverridingBuilder):
    TYPE = "invenio_requests_api_views"
    section = "requests.api-blueprint"
    template = "api-views"
    overriden_sections = {"api-blueprint": "requests.api-blueprint"}

    def finish(self, **extra_kwargs):
        ext = self.current_model.section_requests_ext_resource.config
        super().finish(ext=ext, **extra_kwargs)
