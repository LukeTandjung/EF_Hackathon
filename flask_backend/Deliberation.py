"""
This module contains the functions for the deliberation process.
It supervises the conversation between the agents and the system.
"""

import json
from Agent import Agent
from Conversation import Conversation, User
from Classes import CaseDetails, OCEAN_Scores

class Deliberation:
    """
    A class that contains the functions for the deliberation process.
    """
    def __init__(self, n_rounds: int, agents: [Agent]):
        self.n_rounds = n_rounds
        self.agents = agents
        self.conversation = Conversation(model="gpt-4o-mini")

    def run(self):
        """
        Run the deliberation process.
        """
        for round in range(self.n_rounds):
            print(f"Round {round + 1}:")
            for agent in self.agents:
                answer = agent.generate_speech(self.conversation)
                self.conversation.add_message(answer)
        return self.conversation


if __name__ == "__main__":
    with open("./test_simulation.json", "r") as f:
        data = json.load(f)
    agents = []
    for agent_data in data["agent"]:
        this_case = CaseDetails(data["case"]["name"], data["case"]["details"], data["case"]["prosecution_argument"], data["case"]["defendant_argument"])
        this_ocean_scores = OCEAN_Scores(agent_data["ocean_score"]["open"], agent_data["ocean_score"]["conscientious"], agent_data["ocean_score"]["extrovert"], agent_data["ocean_score"]["agree"], agent_data["ocean_score"]["neurotic"])
        this_agent = Agent(agent_data["name"], agent_data["age"], agent_data["gender"], agent_data["race"], agent_data["political_view"], agent_data["education"], this_ocean_scores, this_case)
        agents.append(this_agent)
    deliberation = Deliberation(data["simulation"]["num_conversations"], agents)
    deliberation.run()