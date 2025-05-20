import sqlite3

import click



@click.command()
def main(incident: str):
    # Initialize with ServiceNow credentials[14]
    assistant = IncidentAssistant(
        sn_instance="https://your-instance.service-now.com",
        sn_creds={
            "username": "api_user",
            "password": "secure_password",
            "client_id": "your_client_id",
            "client_secret": "your_client_secret",
        },
    )

    # Analyze an incident
    results = assistant.analyze_incident("INC0012345")

    # Print results
    for agent, analysis in results.items():
        print(f"=== {agent.upper()} ANALYSIS ===")
        print("Findings:", analysis.findings)
        print("Recommendations:", analysis.recommendations)

# ========== Example Usage ==========
if __name__ == "__main__":
    main()
