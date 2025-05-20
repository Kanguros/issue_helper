from typing import Optional

import requests

from issue_helper.models import ServiceNowIncident


class ServiceNOW:
    def __init__(
        self,
        url: str,
        username: str,
        password: str,
        verify: Optional[bool] = None,
    ):
        self.url = url.rstrip("/")
        self.session = requests.Session()
        self.session.auth = (username, password)
        self.verify = verify

    def get_table(self, table: str, params: dict):
        full_url = f"{self.url}/api/now/table/{table}"
        response = self.session.get(full_url, params=params, verify=self.verify)
        response.raise_for_status()
        return response.json()

    def get_incident(self, incident_id: str) -> ServiceNowIncident:
        result = self.get_table(
            table="incident", params={"sys_id": incident_id}
        )
        records = result.get("result", [])
        if not records:
            raise ValueError(f"Incident with sys_id {incident_id} not found")
        return ServiceNowIncident(**records[0])

    def get_configuration_item(self, incident_id: str) -> Optional[str]:
        incident = self.get_incident(incident_id)
        return incident.configuration_item

    def get_application(self, configuration_item: str) -> Optional[str]:
        response = self.get_table(
            table="cmdb_ci", params={"sys_id": configuration_item}
        )
        records = response.get("result", [])
        if not records:
            return None
        # Assuming 'application' field exists in cmdb_ci table
        return records[0].get("application")

    def find_history_incidents_of_configuration_item(
        self, configuration_item: str
    ) -> list[ServiceNowIncident]:
        response = self.get_table(
            table="incident", params={"configuration_item": configuration_item}
        )
        records = response.get("result", [])
        return (
            [ServiceNowIncident(**record) for record in records]
            if records
            else []
        )
