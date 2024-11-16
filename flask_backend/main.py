from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
  return "Hello World!"

@app.route("/echo", methods=["POST"])
def echo():
  return request.json

@app.route("/deliberation", methods=["POST"])
def deliberation():
    return {
       "metadata": "this is an example deliberation",
        "conversation": [
            {
                "agent_name": "Alex",
                "transcript": "I think I'm actually the criminal."
            },
            {
                "agent_name": "Bob",
                "transcript": "Wait what?"
            },
            {
                "agent_name": "Charlie",
                "transcript": "I think I'm actually the criminal."
            }
        ],
        "vote": [
            {
                "agent_name": "Alex",
                "verdict": "guilty"
            },
            {
                "agent_name": "Bob",
                "verdict": "not_guilty"
            },
            {
                "agent_name": "Charlie",
                "verdict": "guilty"
            }
        ]
    }

if __name__ == "__main__":
  app.run(debug=True)
