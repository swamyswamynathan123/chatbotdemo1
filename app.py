import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from langchain_anthropic import ChatAnthropic
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts.prompt import PromptTemplate
from langchain.globals import set_llm_cache
from langchain_community.cache import InMemoryCache
from langchain_groq import ChatGroq
import markdown


# Load environment variables
load_dotenv()

prompt_template = """
# Conversation Template

You are a concise and helpful book recommendation chatbot. Your role is to provide brief, 
relevant information and resources on data science, machine learning, AI, data engineering, 
and analytics.

Current conversation:
{history}
Human: {input}
AI Assistant:
 """


# Create PromptTemplate object
prompt = PromptTemplate(input_variables=["history", "input"], template=prompt_template)

# Set up caching
set_llm_cache(InMemoryCache())

llm = ChatGroq(
     model="mixtral-8x7b-32768",
     temperature=0.0,
     max_retries=2,
     api_key=os.getenv("GROQ_API_KEY")
)

# Initialize conversation chain
conversation = ConversationChain(
    prompt=prompt,
    llm=llm,
    verbose=True,
    memory=ConversationBufferMemory(ai_prefix="AI Assistant"),
)

# Initialize Flask app
app = Flask(__name__)

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')


# Route for handling chat requests
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    
    # Get response from LangChain conversation
    response = conversation.predict(input=user_message)
    
    # Convert markdown to HTML
    html_response = markdown.markdown(response)
    
    return jsonify({'response': html_response})




# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)