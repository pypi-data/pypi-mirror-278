from maitai_gen.config import Config, InferenceLocations

# TODO consider finding a source of truth where we don't need to deploy everytime a new model comes out
SERVER_PROVIDERS = ["groq", "openai"]
CLIENT_PROVIDERS = ["openai"]

MODELS = {
    "llama3-70b-8192": "groq",
    "llama3-8b-8192": "groq",
    "gpt-4o": "openai",
    "gpt-4o-2024-05-13": "openai",
    "gpt-4-turbo": "openai",
    "gpt-4-turbo-2024-04-09": "openai",
    "gpt-4-0125-preview": "openai",
    "gpt-4-turbo-preview": "openai",
    "gpt-4-1106-preview": "openai",
    "gpt-4-vision-preview": "openai",
    "gpt-4": "openai",
    "gpt-4-0314": "openai",
    "gpt-4-0613": "openai",
    "gpt-4-32k": "openai",
    "gpt-4-32k-0314": "openai",
    "gpt-4-32k-0613": "openai",
    "gpt-3.5-turbo": "openai",
    "gpt-3.5-turbo-16k": "openai",
    "gpt-3.5-turbo-0301": "openai",
    "gpt-3.5-turbo-0613": "openai",
    "gpt-3.5-turbo-1106": "openai",
    "gpt-3.5-turbo-0125": "openai",
    "gpt-3.5-turbo-16k-0613": "openai",
}


def get_default_config() -> Config:
    return Config(
        inference_location=InferenceLocations.SERVER,
        evaluation_enabled=True,
        apply_corrections=True,
        model='gpt-4o',
        temperature=0.4,
        streaming=False,
        response_format="text",
        stop=None,
        logprobs=False,
        max_tokens=None,
        n=1,
    )


def get_model_provider(model_name: str):
    return MODELS[model_name]


def get_models(providers):
    models = []
    for model_name, provider in MODELS.items():
        if provider in providers:
            models.append(model_name)
    return models


def get_available_models():
    return {"all_models": list(MODELS.keys()), "client_models": get_models(CLIENT_PROVIDERS), "server_models": get_models(SERVER_PROVIDERS)}
