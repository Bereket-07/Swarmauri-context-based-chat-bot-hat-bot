from flask import Flask , request , jsonify
from flask_cors import CORS  # Import CORS
from llm_model_setup import converse

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/',methods=['POST'])
def chat():
    data  = request.get_json()
    user_text = data.get('user_text')
    system_context = data.get('system_context')
    model_name = data.get('model_name')
    response = converse(user_text,system_context,model_name)
    return jsonify({"response":response})

if __name__ == "__main__":
    app.run()

    
