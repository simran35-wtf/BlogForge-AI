from services import groq_client, gemini_client
from concurrent.futures import ThreadPoolExecutor

PROVIDERS = {
    "groq":   groq_client,
    "gemini": gemini_client,
}

def generate_content(provider: str, prompt: str, system_msg: str, model: str = None):
    if provider not in PROVIDERS:
        raise ValueError(f"Unknown provider: {provider}")

    module = PROVIDERS[provider]

    if model:
        return module.generate(prompt, system_msg, model)
    return module.generate(prompt, system_msg)


def generate_compare(prompt: str, system_msg: str):
    """Calls Groq and Gemini in parallel, returns both results."""
    results = {}

    def call_provider(name, module):
        try:
            post = module.generate(prompt, system_msg)
            results[name] = {"success": True, "data": post.dict()}
        except Exception as e:
            results[name] = {"success": False, "error": str(e)}

    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [
            executor.submit(call_provider, "groq", groq_client),
            executor.submit(call_provider, "gemini", gemini_client),
        ]
        for f in futures:
            f.result()

    return results