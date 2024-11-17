import json
from openai import OpenAI
import os
from Conversation import Conversation, User, System
from personalities import *
from Classes import OCEAN_Scores, CaseDetails
from pydantic import BaseModel
from typing import Literal

class DeliberationResponse(BaseModel):
    keep_silent: bool
    conversation_response: str
    verdict: float

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
OCEAN_SCORES = ["open", "conscientious", "extrovert", "agree", "neurotic"]

class Agent:
    """
    An agent that can be used to interact with the OpenAI API.
    In this app, an agent is a juror in the jury deliberation process.
    """
    def __init__(self, name, ocean_scores, case_details):
        """
        Initialize an Agent (juror) with their demographic and personality traits.
        
        Args:
            name (str): The agent's name
            ocean_score (dict): Dictionary containing OCEAN personality scores
                - open (float): Openness score (0 to 1)
                - conscientious (float): Conscientiousness score (0 to 1)
                - extrovert (float): Extroversion score (0 to 1)
                - agree (float): Agreeableness score (0 to 1)
                - neurotic (float): Neuroticism score (0 to 1)
            case_details (CaseDetails): CaseDetails object
        """
        self.name = name
        self.ocean_scores = ocean_scores
        self.case_details = case_details
        self.verdict_history = []

        assert isinstance(self.ocean_scores, OCEAN_Scores)
        assert isinstance(self.case_details, CaseDetails)

        self.system_prompt = self._generate_system_prompt()
    
    def generate_initial_verdict(self):
        """
        Generate the initial verdict for the agent based on the case details and personality traits.
        """
        # Generate the initial verdict prompt
        initial_verdict_prompt = self._generate_initial_verdict_prompt()
        
        # Create a conversation with only the system prompt
        initial_conversation = Conversation(model="gpt-4o-mini")
        initial_conversation.prepend_message(System(initial_verdict_prompt))
        initial_conversation.remove_empty_messages()
        
        # Interact with the OpenAI API
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=initial_conversation.to_openai(),
            temperature=0,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "initial_verdict",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "verdict": {
                                "type": "number",
                                "description": (
                                    "The juror's initial confidence level in the defendant's guilt, "
                                    "ranging from 0.0 (completely not guilty) to 1.0 (completely guilty). "
                                    "Please provide a number between 0.0 and 1.0."
                                )
                            }
                        },
                        "required": ["verdict"],
                        "additionalProperties": False
                    }
                }
            }
        )
        
        # Parse the response and store the initial verdict
        parsed_res = json.loads(res.choices[0].message.content)
        verdict_value = float(parsed_res["verdict"])
        verdict_value = max(0.0, min(1.0, verdict_value))  # Clamp between 0.0 and 1.0
        print(f"{self.name} initial verdict: {verdict_value}")
        self.verdict_history.append(verdict_value)
    
    def generate_speech(self, conversation: Conversation):
        """
        Generate a speech for the agent to say in the conversation.
        """
        this_conversation = conversation.deep_copy()
        this_conversation.prepend_message(System(self.system_prompt))
        this_conversation.remove_empty_messages()
        # print(this_conversation.to_openai())
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=this_conversation.to_openai(),
            temperature=0,
            response_format={
                "type": "json_schema",
                "json_schema": {
                "name": "verdict",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                    "keep_silent": {
                        "type": "boolean",
                        "description": "Flag indicating whether the juror chooses to remain silent in this round of conversation."
                    },
                    "conversation_response": {
                        "type": "string",
                        "description": "The response the juror would give. An empty string indicates silence."
                    },
                    },
                    "required": [
                    "keep_silent",
                    "conversation_response",
                    ],
                    "additionalProperties": False
                }
                }
            }
        )
        print(f"{self.name}:")
        parsed_res = json.loads(res.choices[0].message.content)

        print(parsed_res["conversation_response"])

        print("--------------------------------------------------------------")
        return User(content=parsed_res["conversation_response"], name=self.name)
    
    def update_verdict(self, conversation: Conversation):
        """
        Update the agent's verdict based on the conversation so far.
        """
        # Generate the update verdict prompt
        update_verdict_prompt = self._generate_update_verdict_prompt()
        
        # Prepare the conversation
        this_conversation = conversation.deep_copy()
        this_conversation.prepend_message(System(update_verdict_prompt))
        this_conversation.remove_empty_messages()
        
        # Interact with the OpenAI API
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=this_conversation.to_openai(),
            temperature=0,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "verdict_update",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "verdict": {
                                "type": "number",
                                "description": (
                                    "The juror's updated confidence level in the defendant's guilt, "
                                    "ranging from 0.0 (completely not guilty) to 1.0 (completely guilty). "
                                    "Please provide a number between 0.0 and 1.0."
                                )
                            }
                        },
                        "required": ["verdict"],
                        "additionalProperties": False
                    }
                }
            }
        )
        
        # Parse the response and store the updated verdict
        parsed_res = json.loads(res.choices[0].message.content)
        verdict_value = float(parsed_res["verdict"])
        verdict_value = max(0.0, min(1.0, verdict_value))  # Clamp between 0.0 and 1.0
        print(f"{self.name} updated verdict: {verdict_value}")
        self.verdict_history.append(verdict_value)

    
    def _generate_initial_verdict_prompt(self):
        """
        Generate the system prompt for initial verdict generation.
        """
        with open("./juror_initial_verdict_prompt.txt", "r") as f:
            prompt = f.read()
        prompt = prompt.replace("{{ juror_information_placeholder }}", f"Your name is {self.name}.")
        prompt = prompt.replace("{{ personality_traits_placeholder }}", self.ocean_scores.generate_prompt())
        prompt = prompt.replace("{{ case_details_placeholder }}", self.case_details.generate_prompt())
        return prompt

    def _generate_system_prompt(self):
        """
        Generate a system prompt for the agent.
        """
        with open("./juror_system_prompt.txt", "r") as f:
            prompt = f.read()
        # replace {{ juror_information_placeholder }} with the agent's demographic information
        prompt = prompt.replace("{{ juror_information_placeholder }}", f"Your name is {self.name}.")
        # replace {{ personality_traits_placeholder }} with the agent's personality traits
        prompt = prompt.replace("{{ personality_traits_placeholder }}", 
                                self.ocean_scores.generate_prompt())
        # replace {{ case_details_placeholder }} with the case details
        prompt = prompt.replace("{{ case_details_placeholder }}", 
                                self.case_details.generate_prompt())
        
        # Include the agent's current persuasion score
        if self.verdict_history:
            current_persuasion = self.verdict_history[-1]
        else:
            current_persuasion = 0.5  # Default value if no history exists
            
        prompt = prompt.replace("{{ current_persuasion_score }}", str(current_persuasion))
        return prompt
    
    def _generate_update_verdict_prompt(self):
        """
        Generate the system prompt for verdict updating.
        """
        with open("./juror_update_verdict_prompt.txt", "r") as f:
            prompt = f.read()
        prompt = prompt.replace("{{ juror_information_placeholder }}", f"Your name is {self.name}.")
        prompt = prompt.replace("{{ personality_traits_placeholder }}", self.ocean_scores.generate_prompt())
        prompt = prompt.replace("{{ case_details_placeholder }}", self.case_details.generate_prompt())
        return prompt


# test Agent class
# if __name__ == "__main__":
#     ocean_scores = OCEAN_Scores(0.8, 0.1, 0.5, 0.1, 0.8)
#     case_details = CaseDetails("Test Case", "Test Details", "Test Prosecution Argument", "Test Defendant Argument")
#     agent = Agent("John Doe", ocean_scores, case_details)
#     print(agent.system_prompt)

#     conversation = Conversation(model="gpt-4o-mini")
#     agent.generate_speech(conversation)
