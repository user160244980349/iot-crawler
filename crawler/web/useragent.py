

_id = -1
_user_agents = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3112.50 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3112.50 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3112.50 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3112.50 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3112.50 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3112.50 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3112.50 Safari/537.36",
    "Mozilla/5.0 (Wayland; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36",
    "Mozilla/5.0 (Wayland; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3112.50 Safari/537.36",
    "Mozilla/5.0 (Wayland; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3112.50 Safari/537.36",
    "Mozilla/5.0 (Wayland; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3112.50 Safari/537.36",
    "Mozilla/5.0 (Wayland; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3112.50 Safari/537.36",
    "Mozilla/5.0 (Wayland; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3112.50 Safari/537.36",
    "Mozilla/5.0 (Wayland; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3112.50 Safari/537.36",
    "Mozilla/5.0 (Wayland; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3112.50 Safari/537.36",
    "Mozilla/5.0 (Windows 10 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36",
    "Mozilla/5.0 (Windows 10 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3112.50 Safari/537.36",
    "Mozilla/5.0 (Windows 10 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3112.50 Safari/537.36",
    "Mozilla/5.0 (Windows 10 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3112.50 Safari/537.36",
    "Mozilla/5.0 (Windows 10 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3112.50 Safari/537.36",
    "Mozilla/5.0 (Windows 10 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3112.50 Safari/537.36",
    "Mozilla/5.0 (Windows 10 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3112.50 Safari/537.36",
    "Mozilla/5.0 (Windows 10 x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3112.50 Safari/537.36",
]


def get_user_agent():
    global _id
    global _user_agents
    _id += 1
    if _id >= len(_user_agents):
        _id = 0
    return _user_agents[_id]
