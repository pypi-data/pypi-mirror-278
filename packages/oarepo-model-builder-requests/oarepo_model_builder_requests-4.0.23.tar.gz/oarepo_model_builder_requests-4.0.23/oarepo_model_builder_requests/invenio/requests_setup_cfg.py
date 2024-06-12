from oarepo_model_builder.builders import OutputBuilder
from oarepo_model_builder.outputs.cfg import CFGOutput
from oarepo_model_builder.utils.python_name import split_package_base_name


class RequestsSetupCfgBuilder(OutputBuilder):
    TYPE = "requests_setup_cfg"

    def finish(self):
        super().finish()

        output: CFGOutput = self.builder.get_output("cfg", "setup.cfg")

        output.add_dependency("oarepo-requests", ">=1.0.2")
        if (
            "requests" not in self.current_model.definition
            or not self.current_model.definition["requests"]
            or "types" not in self.current_model.definition["requests"]
        ):
            return
        requests = self.current_model.definition["requests"]["types"]
        if requests:
            for request_data in requests.values():
                class_ = request_data["class"]
                module, base = split_package_base_name(class_)
                output.add_entry_point(
                    "invenio_requests.types",
                    request_data["id"],
                    f"{module}:{base}",
                )
