from config import user_agents


def get_user_agent():
    agent = user_agents.pop(0)
    user_agents.append(agent)
    return agent
