import os
from google.adk.agents import SequentialAgent,LlmAgent
import google.genai as genai
import tools
from dotenv import load_dotenv




load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')
genai.Client(api_key=api_key)

# APP_NAME = "code_pipeline_app"
# USER_ID = "dev_user_01"
# SESSION_ID = "pipeline_session_02"


MODEL='gemini-2.0-flash-001'



greeter = LlmAgent(
    model=MODEL,
    name='greeter',
    description='You greet the user and collect the topic for story telling from the user',
    output_key='topic',
    instruction="""You need to do the following things:-
     1)  First of all, you are a calm , patient and friendly agent 
      2) Greet the user first and ask for a name.  If name has already been provided , skip asking for a name and simply greet using the name provided.
     3) Ask the user to suggest a topic  for the story . Wait for the user to provide a topic.
     4) Only once you have a topic from the user, Say out loud something like -"a story on {'topic'} will be narrated soon"
     """
    #  Store the name provided in session's state object {'name'}
    # Store this in the session's state object {'topic'}
    # and then pass the session state object 'topic' to the story_telling_agent
)
# 5. Lastly, store the story in the session state object {'story'}

story_creation_agent = LlmAgent(
    model=MODEL,
    name="story_creation_agent",
    instruction="""
Core Task:
Get the topic for story telling from the session state key of the greeter agent {'topic'} and do the following:-
1. Create using imagination or re-tell a known story: Carefully include in your compilation only stories that can strictly be told to children.
2. Be mindful of the tone , language , narrative and message conveyed.
3. Add an element of wit and fun along the way to engage the child but keeping in mind point 2. above
4. Make it an interesting one with elements including what a 3 year old  would love to hear about


Output Requirements:


Focus Criteria: Each proposed area must meet the following criteria:
Time : Come up with a short story of 100 words
Catchy Title: Come up with a catchy title to engage the 3 year old child
Novelty in story line and elements: Let the story be interesting, something that sparks imagination, visualization and learning with interestign characters 
and storyline 
Wit:Let the story be conversational between the characters infused with fun and humor along the way.  Don't hesitate to include a bit of a song if that makes it more interesting
Tone and language: Tone and language to be a polite and to suit the kind of story telling that matches that of kids
Message: Lastly, include a moral message in the story.
   

""",
    output_key="story"
)
story_narration_agent = LlmAgent(
    model=MODEL,
    name="story_telling_agent",
    instruction="""
    Core Task:
    1. Retrieve the story from the story_creation_agent i.e. from its session's state object {'story'}
    2. Narrate it back to the user  
      
        """
    ,
 tools=[tools.generate_audio],
    )

story_pipeline_agent = SequentialAgent(
    name="story_pipeline_agent",
    sub_agents=[greeter,story_creation_agent, story_narration_agent],
    description= 'you are a  helpful pipeline agent to help orchestrate the tasks between the 3 sub_agents ',

)
root_agent=story_pipeline_agent


