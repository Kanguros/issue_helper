import click

from issue_helper.agents import IncidentAssistant
from issue_helper.itsm import ServiceNOW


@click.command()
@click.argument("incident")
def main(incident: str):
    url = "https://your-instance.service-now.com"
    username = ("username",)
    password = "password"  # noqa: S105

    service_now = ServiceNOW(url=url, username=username, password=password)
    assistant = IncidentAssistant(service_now)

    results = assistant.analyze_incident(incident)

    for agent, analysis in results.items():
        print(f"=== {agent.upper()} ANALYSIS ===")
        print("Findings:", analysis.findings)
        print("Recommendations:", analysis.recommendations)


if __name__ == "__main__":
    main()
