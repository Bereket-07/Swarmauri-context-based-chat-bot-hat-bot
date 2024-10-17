import streamlit as st
import os
from dotenv import load_dotenv
from swarmauri.standard.llms.concrete.GroqModel import GroqModel
from swarmauri.standard.messages.concrete.SystemMessage import SystemMessage
from swarmauri.standard.agents.concrete.SimpleConversationAgent import SimpleConversationAgent
from swarmauri.standard.conversations.concrete.MaxSystemContextConversation import MaxSystemContextConversation

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv('GROQ_API')

# Initialize the GroqModel instance to retrieve allowed models
llm_models = GroqModel(api_key=GROQ_API_KEY)
allowed_models = llm_models.allowed_models

# Initialize the conversation instance
conversation = MaxSystemContextConversation()

# Function to assign the model based on input
def assign_model(model_name):
    try:
        return GroqModel(api_key=GROQ_API_KEY, name=model_name)
    except Exception as e:
        st.error(f"Error initializing model: {e}")
        return None

# Define the function to interact with the agent
def converse(user_text: str, system_context: str, model_name: str) -> str:
    try:
        # Initialize the model based on the user's selection
        llm = assign_model(model_name)
        if llm is None:
            return "Failed to initialize model."
        
        # Initialize the agent with the selected model and conversation context
        agent = SimpleConversationAgent(llm=llm, conversation=conversation)
        agent.conversation.system_context = SystemMessage(content=system_context)

        # Execute the conversation command
        response = agent.exec(user_text)
        return str(response)
    except Exception as e:
        return f"An error occurred during the conversation: {e}"

# Apply custom CSS for styling
st.markdown(
    """
    <style>
    .main {
        background-color: #f8f9fa;
        font-family: 'Arial', sans-serif;
    }
    .title {
        color: #4CAF50;
        text-align: center;
        font-size: 2.5em;
        font-weight: bold;
        margin-top: 20px;
    }
    .subheader {
        color: #555;
        text-align: center;
        margin-bottom: 20px;
        font-size: 1.2em;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        font-size: 1em;
        border-radius: 10px;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .input-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit app layout
st.markdown("<div class='title'>System Context Conversation with GroqModel</div>", unsafe_allow_html=True)
st.markdown("<div class='subheader'>Interact with the agent using the selected model and system context.</div>", unsafe_allow_html=True)

# Container for the response message
response_placeholder = st.empty()

# Input fields inside a container
with st.container():
    st.markdown("<div class='input-container'>", unsafe_allow_html=True)
    
    user_text = st.text_input("User Text", placeholder="Type your message here...")
    system_context = st.text_input("System Context", placeholder="Enter the system context here...")
    model_name = st.selectbox("Choose Model", options=allowed_models)
    
    # Button to start conversation
    if st.button("Start Conversation"):
        response = converse(user_text, system_context, model_name)
        response_placeholder.write(f"**Response:** {response}")
    
    st.markdown("</div>", unsafe_allow_html=True)
