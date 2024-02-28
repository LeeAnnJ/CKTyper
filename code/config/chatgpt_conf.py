PROXY_URL = "http://127.0.0.1:7890" # or None
# for ModelAccesser_V2
# api key & base url for openai
# better have more than one account to avoid the rate limit
ACCOUNTS = [
    {
        "api_key": "sk-xxx",
        "base_url": "https://xxx.xxx/com" # your gpt proxy url
    },
    {
        "api_key": "sk-xxx",
        "base_url": None

    }
]

# for ModelAccesser_V1
# cookie: __Secure-next-auth.session-token available from https://chat.openai.com/
# better have more than one account to avoid the rate limit
SESSION_TOKEN = ["xxx","xxx"]