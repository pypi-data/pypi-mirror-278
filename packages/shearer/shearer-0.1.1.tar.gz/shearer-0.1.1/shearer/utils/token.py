import tiktoken

def get_token_num(content: str, model_name: str = "gpt-4") -> int:
    encoding = tiktoken.encoding_for_model(model_name)
    return len(encoding.encode(content))