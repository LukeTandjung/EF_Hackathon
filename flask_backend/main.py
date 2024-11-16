from flask import Flask, request

from Deliberation import Deliberation
from Classes import CaseDetails, OCEAN_Scores
from Agent import Agent

app = Flask(__name__)

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
            data["case"]["prosecution_argument"],
            data["case"]["defendant_argument"]
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
            agent_data["age"],
            agent_data["gender"],
            agent_data["race"],
            agent_data["political_view"],
            agent_data["education"],
            ocean_scores,
            case_details
        )
        agents.append(agent)
    
    # Create and run deliberation
    deliberation = Deliberation(data["simulation"]["num_conversations"], agents)
    conversation = deliberation.run()
    
    print(conversation.messages)

    # counting the votes
    last_conversations = conversation.messages[-len(agents):]
    vote = []
    for conv in last_conversations:
        vote.append({
            "agent_name": conv.name,
            "verdict": conv.vote
        })

    conversation_list = []
    for msg in conversation.messages:
        conversation_list.append({
            "agent_name": msg.name,
            "transcript": msg.content
        })
    
    return {
        "conversation": conversation_list,
        "votes": vote
    }

if __name__ == "__main__":
  app.run(debug=True)
