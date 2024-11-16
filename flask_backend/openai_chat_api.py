from openai import OpenAI
import random
from pathlib import Path

# Initialize OpenAI client
client = OpenAI(api_key='sk-kkkkkkkkkkkkkkkkk')  # Put API key here

# Simplified personality traits
PERSONALITY_TRAITS = [
    "empathetic", "analytical", "decisive", "open-minded",
    "assertive", "patient", "curious", "diligent"
]

def get_system_prompt():
    """Read and prepare the system prompt with random personality traits."""
    # Read the system prompt from file
    prompt_path = Path('juror_system_prompt.txt')
    system_prompt = prompt_path.read_text()
    
    # Select random traits and insert them into the prompt
    traits = ", ".join(random.sample(PERSONALITY_TRAITS, 3))
    return system_prompt.replace('{{ personality_traits_placeholder }}', traits)

def get_verdict(case_details):
    """Get a verdict for the given case details."""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": get_system_prompt()},
                {"role": "user", "content": case_details}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error getting verdict: {str(e)}"

if __name__ == "__main__":
    case_details = input("Enter your case details: ")
    verdict = get_verdict(case_details)
    print("\nVerdict:", verdict)