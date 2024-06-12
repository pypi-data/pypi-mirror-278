from pathlib import Path

from oarepo_model_builder.utils.python_name import module_to_path

from .invenio_requests_builder_base import InvenioRequestsBuilder


class InvenioRequestsActionsBuilder(InvenioRequestsBuilder):
    TYPE = "invenio_requests_actions"
    section = "requests"
    template = "requests-actions"
    skip_if_not_generating = False

    def finish(self, **extra_kwargs):
        vars = self.get_vars_or_none_if_no_requests()
        if not vars:
            return

        for request in vars["requests"]["types"].values():
            for action in request["actions"].values():
                if not action["generate"]:
                    continue
                module = action["module"]
                python_path = Path(module_to_path(module) + ".py")

                self.process_template(
                    python_path,
                    self.template,
                    current_module=module,
                    vars=vars,
                    action=action,
                    **extra_kwargs,
                )
