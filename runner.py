from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from config import APP_NAME

session_service = InMemorySessionService()

def create_runner(agent):
    return Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=session_service
    )