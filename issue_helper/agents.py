from google import genai
from google.genai import types

from issue_helper.itsm import ServiceNOW
from issue_helper.models import AnalysisResult, ServiceNowIncident


class BaseAgent:
    def __init__(self, client: genai.Client):
        self.client = client
        self.name = "base_agent"

    def analyze(self, incident: ServiceNowIncident) -> AnalysisResult:
        raise NotImplementedError


class LinuxInfraAgent(BaseAgent):
    def __init__(self, client: genai.Client):
        super().__init__(client)
        self.name = "linux_agent"

    def analyze(self, incident: ServiceNowIncident) -> AnalysisResult:
        prompt = f"""
        Analyze Linux-related incident {incident.number}:
        Description: {incident.description}
        Related CIs: {incident.related_ci}

        Consider common Linux issues:
        - Disk space/partition issues
        - Service failures
        - Permission problems
        - Kernel panics
        - Package dependency issues
        """
        response = self.client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[self._linux_analysis_tool()]
            ),
        )
        return self._parse_response(response)


class WindowsInfraAgent(BaseAgent):
    def __init__(self, client: genai.Client):
        super().__init__(client)
        self.name = "windows_agent"

    def analyze(self, incident: ServiceNowIncident) -> AnalysisResult:
        # Placeholder for Windows-specific logic
        pass


class IncidentAssistant:
    def __init__(self, service_now: ServiceNOW):
        self.service_now = service_now
        self.llm_client = genai.Client()
        self.agents = {
            "linux": LinuxInfraAgent(self.llm_client),
            "windows": WindowsInfraAgent(self.llm_client),
        }

    def fetch_incident(self, incident_id: str) -> ServiceNowIncident:
        return self.service_now.get_incident(incident_id)

    def analyze_incident(self, incident_id: str) -> dict[str, AnalysisResult]:
        incident = self.fetch_incident(incident_id)
        results = {}
        for agent_name, agent in self.agents.items():
            if self._should_run_agent(agent, incident):
                results[agent_name] = agent.analyze(incident)
        return results

    def _should_run_agent(
        self, agent: BaseAgent, incident: ServiceNowIncident
    ) -> bool:
        # Implement logic based on CI types or other attributes
        return True
