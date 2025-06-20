## Here's my first experiment with Google ADK !

As a part of this project, I have set up  a Bedtime storytelling app using Google's ADK.

The primary libraries required would be 
  *  google-adk
  *  Eleven-labs
  *  dotenv (depending on how you'd like the API keys to be retrieved)
  *  ffmpeg

For the purpose of this project, I have broken down my task of my storytelling into 3 sub-tasks that I have assigned to 3 of the sub-agents viz. the Greeter (primarily for greeting the user and accepting a topic for the storytelling from a user), the Story Creation Agent which creates the story and finally the story narration agent that narrates the story back to the user.

## Sub-Agents

### Greeter Agent : —
This agent is an LLMAgent equipped to have meaningful conversations and reason. The primary purpose of this agent is to greet the user and get a topic for story telling from the user. The agent has a model passed to it which in my case was ‘gemini-2.0-flash-001’. You could also pass a short description of the agent and provide some instructions on the tasks you would like it to carry out. Lastly, the output_key here is the parameter ‘topic’ which it collects from the user and passes onto the next agent in the sequence. The parameters passed are retrieved from the active session’s state object behind the scenes.

### Story Creation Agent:-

The story creation agent is an LLMAgent that gets the topic from the Greeter agent and follows the guidelines I have given to build out a story. Further the story it builds around the topic is passed to the next agent in the sequence which is the Story Narration Agent.
### Story Narration Agent:-

The story naration agent is an LLMAgent which picks up the ‘story’ from the story_creation_agent and converts the story text to audio by invoking the generate_audio funtion specified in the ADK’s function tool argument here. ‘generate_audio’ is a custom function I built which resides in my tools.py file that accepts a text input and converts to audio via an API call to the third-party platform ‘Elevenlabs’ .

### Story Pipeline Agent 

This agent which is a Sequential Agent is a workflow agent and acts as a task orchestrator for the sub-agents. Being a sequential agent, it executes the sub-agents in a sequence passing the session's state variables (or parameters of interest, put simply) from one sub-agent to another.
