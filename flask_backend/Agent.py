from openai import OpenAI
import os
from Conversation import Conversation, User, System
from personalities import *
from Classes import OCEAN_Scores, CaseDetails

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
OCEAN_SCORES = ["open", "conscientious", "extrovert", "agree", "neurotic"]

class Agent:
    """
    An agent that can be used to interact with the OpenAI API.
    In this app, an agent is a juror in the jury deliberation process.
    """
    def __init__(self, name, age, gender, race, political_view, education, ocean_scores, case_details):
        """
        Initialize an Agent (juror) with their demographic and personality traits.
        
        Args:
            name (str): The agent's name
            age (int): Age between 0 and 100
            gender (str): One of "Male", "Female", or "Others"
            race (str): Racial/ethnic background
            political_view (str): Political orientation
            education (str): Educational background
            ocean_score (dict): Dictionary containing OCEAN personality scores
                - open (float): Openness score (0 to 1)
                - conscientious (float): Conscientiousness score (0 to 1)
                - extrovert (float): Extroversion score (0 to 1)
                - agree (float): Agreeableness score (0 to 1)
                - neurotic (float): Neuroticism score (0 to 1)
            case_details (CaseDetails): CaseDetails object
        """
        self.name = name
        self.age = age
        self.gender = gender
        self.race = race
        self.political_view = political_view
        self.education = education
        self.ocean_scores = ocean_scores
        self.case_details = case_details

        assert isinstance(self.ocean_scores, OCEAN_Scores)
        assert isinstance(self.case_details, CaseDetails)

        self.system_prompt = self._generate_system_prompt()
    
    def generate_speech(self, conversation: Conversation):
        """
        Generate a speech for the agent to say in the conversation.
        """
        this_conversation = conversation.deep_copy()
        this_conversation.prepend_message(System(self.system_prompt))
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=this_conversation.to_openai(),
            temperature=0.5,
        )
        print(res.choices[0].message.content)
        return User(content=res.choices[0].message.content, name=self.name)

        

    def _generate_system_prompt(self):
        """
        Generate a system prompt for the agent.
        """
        with open("./juror_system_prompt.txt", "r") as f:
            prompt = f.read()
        # replace {{ juror_information_placeholder }} with the agent's demographic information
        prompt = prompt.replace("{{ juror_information_placeholder }}", 
                                self._generate_juror_information_prompt())
        # replace {{ personality_traits_placeholder }} with the agent's personality traits
        prompt = prompt.replace("{{ personality_traits_placeholder }}", 
                                self.ocean_scores.generate_prompt())
        # replace {{ case_details_placeholder }} with the case details
        prompt = prompt.replace("{{ case_details_placeholder }}", 
                                self.case_details.generate_prompt())
        return prompt

    def _generate_juror_information_prompt(self):
        """
        Generate a prompt for the agent's demographic information.
        """
        return f"Your name is {self.name}. You are a {self.age}-year-old {self.gender} {self.race} with a {self.political_view} political view and a {self.education} education level."

# test Agent class
if __name__ == "__main__":
    ocean_scores = OCEAN_Scores(0.8, 0.1, 0.5, 0.1, 0.8)
    case_details = CaseDetails("Test Case", "Test Details", "Test Prosecution Argument", "Test Defendant Argument")
    agent = Agent("John Doe", 30, "Male", "White", "Democrat", "B.S.", ocean_scores, case_details)
    print(agent.system_prompt)