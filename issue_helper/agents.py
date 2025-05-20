
from typing import Dict

from google import genai
from google.genai import types


# ========== Base Agent Class ==========
class AnalysisAgent:
    def __init__(self, client: genai.Client):
        self.client = client
        self.name = "base_agent"

    def analyze(self, incident: ServiceNowIncident) -> AnalysisResult:
        """To be implemented by specialized agents"""
        raise NotImplementedError

# ========== Specialized Agents ==========
class LinuxInfraAgent(AnalysisAgent):
    def __init__(self, client: genai.Client):
        super().__init__(client)
        self.name = "linux_agent"

    def analyze(self, incident: ServiceNowIncident) -> AnalysisResult:
        prompt = f'''
        Analyze Linux-related incident {incident.number}:
        Description: {incident.description}
        Related CIs: {incident.related_ci}

        Consider common Linux issues:
        - Disk space/partition issues
        - Service failures
        - Permission problems
        - Kernel panics
        - Package dependency issues
        '''

        response = self.client.models.generate_content(
            model='gemini-2.0-flash-001',
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[self._linux_analysis_tool()]
            )
        )
        return self._parse_response(response)

class WindowsInfraAgent(AnalysisAgent):
    def __init__(self, client: genai.Client):
        super().__init__(client)
        self.name = "windows_agent"

    def analyze(self, incident: ServiceNowIncident) -> AnalysisResult:
        # Similar structure to Linux agent with Windows-specific logic
        pass

# ========== Core Workflow Engine ==========
class IncidentAssistant:
    def __init__(self, sn_instance: str, sn_creds: dict):
        self.sn_client = servicenow_api.Api(
            url=sn_instance,
            **sn_creds
        )
        self.llm_client = genai.Client()
        self.agents = {
            'linux': LinuxInfraAgent(self.llm_client),
            'windows': WindowsInfraAgent(self.llm_client)
        }

    def fetch_incident(self, incident_id: str) -> ServiceNowIncident:
        """Retrieve incident from ServiceNow[12]"""
        response = self.sn_client.get_table(
            table='incident',
            params={'sys_id': incident_id}
        )
        return ServiceNowIncident(**response.value)

    def analyze_incident(self, incident_id: str) -> Dict[str, AnalysisResult]:
        incident = self.fetch_incident(incident_id)

        results = {}
        for agent_name, agent in self.agents.items():
            if self._should_run_agent(agent, incident):
                results[agent_name] = agent.analyze(incident)

        return results
  # noqa: W293
    def _should_run_agent(self, agent: AnalysisAgent, incident: ServiceNowIncident) -> bool:
        """Determine if agent is relevant for this incident"""
        # Implement logic based on CI types or other attributes
        return True
