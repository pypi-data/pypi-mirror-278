from oarepo_model_builder_requests.invenio.overriding_builder import OverridingBuilder


class RequestsAPPViewsBuilder(OverridingBuilder):
    TYPE = "invenio_requests_app_views"
    section = "requests.app-blueprint"
    template = "app-views"
    overriden_sections = {"app-blueprint": "requests.app-blueprint"}

    def finish(self, **extra_kwargs):
        ext = self.current_model.section_requests_ext_resource.config
        super().finish(ext=ext, **extra_kwargs)
