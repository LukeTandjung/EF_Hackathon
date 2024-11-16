from personalities import *

class OCEAN_Scores:
    """
    A class that contains the OCEAN scores of an agent.
    """
    def __init__(self, open, conscientious, extrovert, agree, neurotic):
        self.open = open
        self.conscientious = conscientious
        self.extrovert = extrovert
        self.agree = agree
        self.neurotic = neurotic
    
    def generate_prompt(self):
        """
        Generate a prompt for the agent's personality traits.
        """
        traits = [
            openness_trait(self.open),
            conscientiousness_trait(self.conscientious),
            extraversion_trait(self.extrovert),
            agreeableness_trait(self.agree),
            neuroticism_trait(self.neurotic)
        ]
        return "\n".join(trait for trait in traits if trait)

class CaseDetails:
    """
    A class that contains the details of a legal case.
    """
    def __init__(self, name, details, prosecution_argument, defendant_argument):
        self.name = name
        self.details = details
        self.prosecution_argument = prosecution_argument
        self.defendant_argument = defendant_argument
    
    def generate_prompt(self):
        """
        Generate a prompt for the case details.
        """
        return "\n".join([
            f"Case name: {self.name}",
            f"Case details: {self.details}",
            f"Prosecution argument: {self.prosecution_argument}",
            f"Defendant argument: {self.defendant_argument}"
        ])