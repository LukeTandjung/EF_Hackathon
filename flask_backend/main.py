from flask import Flask, request
from flask_cors import CORS

from Deliberation import Deliberation
from Classes import CaseDetails, OCEAN_Scores
from Agent import Agent

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
  return "Hello World!"

@app.route("/echo", methods=["POST"])
def echo():
  return request.json

@app.route("/deliberation", methods=["POST"])
def deliberation():
    data = request.json
    
    # Create Agent instances
    agents = []
    for agent_data in data["agent"]:
        case_details = CaseDetails(
            data["case"]["name"],
            data["case"]["details"],
            data["case"]["argument"],
        )
        
        ocean_scores = OCEAN_Scores(
            agent_data["ocean_score"]["open"],
            agent_data["ocean_score"]["conscientious"],
            agent_data["ocean_score"]["extrovert"],
            agent_data["ocean_score"]["agree"],
            agent_data["ocean_score"]["neurotic"]
        )
        
        agent = Agent(
            agent_data["name"],
            ocean_scores,
            case_details
        )
        agents.append(agent)
    
    # Create and run deliberation
    deliberation = Deliberation(agents)
    conversation = deliberation.run()

    # Collecting the votes from agents
    votes = []
    convinced = 0
    highest_initial_buy_in = 0
    highest_initial_buy_in_agent = None
    lowest_initial_buy_in = 1
    lowest_initial_buy_in_agent = None
    for agent in agents:

        # Finds the current highest initial persuasion.
        if agent.verdict_history[0] > highest_initial_buy_in:
            highest_initial_buy_in = agent.verdict_history[0]
            highest_initial_buy_in_agent = agent.name

        # Finds the current highest initial persuasion.
        if agent.verdict_history[0] < lowest_initial_buy_in:
            lowest_initial_buy_in = agent.verdict_history[0]
            lowest_initial_buy_in_agent = agent.name

        # Finds the most persuasive jury. 
        # Initialize a dictionary to store the average persuasion changes for each agent
        average_persuasion_changes = {}

        # Total number of agents
        num_agents = len(agents)

        # For each agent, calculate the average change in persuasion they caused in others
        for agent in agents:
            agent_name = agent.name
            agent_index = agents.index(agent)
            speech_index = agent_index + 1  # Speeches start from index 1 in persuasion_history

            total_change = 0
            num_other_agents = num_agents - 1

            for other_agent in agents:
                if other_agent != agent:
                    # Compute the change in persuasion for other_agent after agent's speech
                    try:
                        # Ensure indices are within bounds
                        change = other_agent.verdict_history[speech_index] - other_agent.verdict_history[speech_index - 1]
                    except IndexError:
                        # Handle potential index errors if the histories are not properly populated
                        change = 0
                    total_change += change

            # Compute the average change caused by this agent's speech
            average_change = total_change / num_other_agents
            average_persuasion_changes[agent_name] = average_change

        # Identify the agent with the highest and lowest average persuasion change
        most_positive_agent = max(average_persuasion_changes, key=average_persuasion_changes.get)
        most_negative_agent = min(average_persuasion_changes, key=average_persuasion_changes.get)

        # The last element in agent.verdict_history is the most recent verdict
        # This function is calculating the proportion of the jury that was swayed by the argument!
        if agent.verdict_history[-1] > 0.5:
           convinced += 1

    percentage_sway = round((convinced / len(agents)) * 100)

    conversation_list = []
    for msg in conversation.messages:
        conversation_list.append({
            "agent_name": msg.name,
            "transcript": msg.content
        })
    
    response = {
        "conversation": conversation_list,
        "statistics": {
           "percentage_sway": f"{percentage_sway}%",
           "most_initial_persuaded": f"{highest_initial_buy_in_agent}",
           "least_initial_persuaded": f"{lowest_initial_buy_in_agent}",
            "most_positive_sway": f"{most_positive_agent}",
            "most_negative_sway": f"{most_negative_agent}"
        }
    }
    return response

if __name__ == "__main__":
  app.run(debug=True)
