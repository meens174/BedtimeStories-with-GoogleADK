# Bedtime-story-app-with-Google-ADK
Bedtime story app that takes a topic and  creates a story and narrates it back to the user - using SequentialAgents from Google ADK

The inspiration for this project was my 3 year old who wishes to be narrated a bed time story each day :)

In this project, I have explored the Google ADK framework to build agents for my bedtime story application. 

The project implements a SequentialAgent for orchestrating the workflow and is composed of two sub-agents - the greeter who greets the user and the story creation agent that creates the story based on the topic to be used for the story telling.

Lastly, the created story is passed from this story creation agent to generate audio for narration purposes. The audio generation has been aided by the Elevenlabs Text-to-Speech API which is then streamed back to the user.

The  Bedtime-story-app-with-Google-ADK makes use of 

