import os
import tools
import asyncio
import logging
from dotenv import load_dotenv
from google.adk.agents import SequentialAgent,LlmAgent

from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
import google.genai as genai



load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')
genai.Client(api_key=api_key)

APP_NAME = "code_pipeline_app"
USER_ID = "dev_user_01"
SESSION_ID = "pipeline_session_02"


MODEL='gemini-2.0-flash-001'


greeter = LlmAgent(
    model=MODEL,
    name='greeter',
    description='You greet the user and collect the topic for story telling from the user',
    output_key='topic',
    instruction="""You need to do two things:-
     1)  Ask the user to suggest a topic  for the story 
     2) Store this in the session's state object {topic}
     2) Say something like - a story on {topic} will be narrated soon and then pass the topic to the story_telling_agent
     """,
    
    
)

story_telling_agent = LlmAgent(
    model=MODEL,
    name="story_telling_agent",
    instruction="""
Core Task:
Get the topic for story telling from the session state key of the greeter agent 'topic' and do the following:-
1. Create using imagination or re-tell a known story: Carefully include in your compilation only stories that can strictly be told to children.
2. Be mindful of the tone , language , narrative and message conveyed.
3. Add an element of wit and fun along the way to engage the child but keeping in mind point 2. above
4. Make it an interesting one with elements including what a 3 year old  would love to hear about

Output Requirements:


Focus Criteria: Each proposed area must meet the following criteria:
Time : Come up with a short story of 50 words
Catchy Title: Come up with a catchy title to engage the 3 year old child
Novelty in story line and elements: Let the story be interesting, something that sparks imagination, visualization and learning with interestign characters 
and storyline 
Wit:Let the story be conversational between the characters infused with fun and humor along the way.  Don't hesitate to include a bit of a song if that makes it more interesting
Tone and language: Tone and language to be a polite and to suit the kind of story telling that matches that of kids
Message: Lastly, include a moral message in the story.
   

""",
    output_key="story",

)


story_pipeline_agent = SequentialAgent(
    name="story_pipeline_agent",
    sub_agents=[greeter,story_telling_agent],
    description= 'you are a  helpful pipeline agent to help orchestrate the tasks between the 2 sub_agents ',

)


# --- Configure Logging ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
# --- Setup Runner and Session ---
session_service = InMemorySessionService()
initial_state = {"topic": ""}
session = asyncio.run(session_service.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state=initial_state # Pass initial state here
))
logger.info(f"Initial session state: {session.state}")




# --- Function to Interact with the Agent ---
def call_agent(user_input_topic: str):
    """
    Sends a new topic to the agent (overwriting the initial one if needed)
    and runs the workflow.
    """
    current_session = asyncio.run(session_service.get_session(app_name=APP_NAME, 
                                                  user_id=USER_ID, 
                                                  session_id=SESSION_ID))
    if not current_session:
        logger.error("Session not found!")
        return

    current_session.state["topic"] = user_input_topic
    logger.info(f"Updated session state topic to: {user_input_topic}")

    content = types.Content(role='user', parts=[types.Part(text=f"Generate a story about: {user_input_topic}")])
    events = runner.run(user_id=USER_ID, session_id=SESSION_ID, new_message=content)

    # final_response = "No final response captured."
    for event in events:
        
              
        if event.is_final_response() and event.content and event.content.parts:
            logger.info(f"Potential final response from [{event.author}]: {event.content.parts[0].text}")
            tools.generate_audio(event.content.parts[0].text) 


runner = Runner(
    agent=story_pipeline_agent, # Pass the custom orchestrator agent
    app_name=APP_NAME,
    session_service=session_service
)


# --- Run the Agent ---
# call_agent('dinosaurs')