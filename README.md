# robusta-button-enricher

[Robusta](https://github.com/robusta-dev/robusta) is an amazing tool for enriching and enhancing your alerting system. This project is an [external action](https://docs.robusta.dev/master/playbook-reference/defining-playbooks/external-playbook-repositories.html#loading-external-actions) that allows you to enrich your alerts with buttons based on the alert context.

## Requirements

- Robusta v0.29+

## Usage

Example usage:

```yaml
customPlaybooks:
- triggers:
  - on_image_pull_backoff: {}
  actions:
  - image_pull_backoff_reporter: {}
  - button_enricher:
      button_text: "Navigate to ${namespace}"
      button_url: "https://example.com/namespace/${namespace}"
```

It supports templating, with the same set of substitutions as the [template_enricher](https://docs.robusta.dev/master/playbook-reference/actions/event-enrichment.html#template-enricher) action which was recommended as an alternative.

> [!NOTE]
> As per the current implementation, if the `button_url` is empty, the button will not be shown.
