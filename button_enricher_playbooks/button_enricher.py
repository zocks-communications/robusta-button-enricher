from typing import Dict, Any
from collections import defaultdict
from robusta.api import action, ActionParams, PrometheusKubernetesAlert, KubernetesResourceEvent, Link
from string import Template


class TemplatedButtonParams(ActionParams):
    """
    :var button_text: The templated text of the button
    :var button_url: The templated URL of the button
    """
    button_text: str
    button_url: str


def _get_labels(event: KubernetesResourceEvent, default_value: str = "<missing>") -> Dict[str, Any]:
    labels: Dict[str, Any] = defaultdict(lambda: default_value)
    if isinstance(event, PrometheusKubernetesAlert):
        labels.update(event.alert.labels)
        labels.update(event.alert.annotations)
        labels.update(vars(event.get_alert_subject()))
        labels["kind"] = labels["subject_type"].value
    elif isinstance(event, KubernetesResourceEvent):
        labels.update(vars(event.get_subject()))
        labels["kind"] = labels["subject_type"].value

    return labels


@action
def button_enricher(event: KubernetesResourceEvent, params: TemplatedButtonParams):
    """
    Create a button with a templated text and URL.
    You can inject the k8s subject info and additionally on Prometheus alerts, any of the alert's Prometheus labels.

    Common variables to use are ${name}, ${kind}, ${namespace}, and ${node}

    A variable like ${foo} will be replaced by the value of info/label foo.
    If it isn't present, then the text will be skipped.

    If the button_url is empty, then the button will not be added.

    Check example for adding a template link.

    """
    labels = _get_labels(event, default_value="")
    button_text = Template(params.button_text).safe_substitute(labels)
    button_url = Template(params.button_url).safe_substitute(labels)
    if button_url.strip() != "":
        event.add_link(Link(url=button_url, name=button_text))
