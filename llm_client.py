# llm_client.py
# Stateless LLM wrapper: Ollama primary, Groq fallback.
# Usage: generate(prompt, system_prompt='', max_tokens=512) -> str

import os
import requests
from dotenv import load_dotenv

load_dotenv()  # loads GROQ_API_KEY from .env

OLLAMA_URL   = 'http://localhost:11434/api/generate'
OLLAMA_MODEL = 'llama3.1:8b'
GROQ_MODEL   = 'llama3-8b-8192'
GROQ_API_URL = 'https://api.groq.com/openai/v1/chat/completions'


def _call_ollama(prompt: str, system_prompt: str, max_tokens: int) -> str:
    """Call Ollama REST API with a full prompt string. Returns generated text."""
    full_prompt = f'{system_prompt}\n\n{prompt}'.strip() if system_prompt else prompt
    payload = {
        'model':   OLLAMA_MODEL,
        'prompt':  full_prompt,
        'stream':  False,
        'options': {'num_predict': max_tokens}
    }
    resp = requests.post(OLLAMA_URL, json=payload, timeout=120)
    resp.raise_for_status()
    return resp.json()['response'].strip()


def _call_groq(prompt: str, system_prompt: str, max_tokens: int) -> str:
    """Call Groq OpenAI-compatible API. Returns generated text."""
    api_key = os.environ.get('GROQ_API_KEY', '')
    if not api_key:
        raise EnvironmentError(
            'GROQ_API_KEY not set. Add it to .env or export GROQ_FALLBACK=0 to use Ollama.'
        )
    messages = []
    if system_prompt:
        messages.append({'role': 'system', 'content': system_prompt})
    messages.append({'role': 'user', 'content': prompt})
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type':  'application/json'
    }
    payload = {
        'model':      GROQ_MODEL,
        'messages':   messages,
        'max_tokens': max_tokens
    }
    resp = requests.post(GROQ_API_URL, json=payload, headers=headers, timeout=60)
    resp.raise_for_status()
    return resp.json()['choices'][0]['message']['content'].strip()


def generate(prompt: str, system_prompt: str = '', max_tokens: int = 512) -> str:
    """
    Main entry point. Calls Groq if GROQ_FALLBACK=1, else calls Ollama.
    Args:
        prompt:        The user/assembled prompt string.
        system_prompt: Optional system instruction (empty string = no system prompt).
        max_tokens:    Maximum tokens to generate.
    Returns:
        Generated text string.
    """
    use_groq = os.environ.get('GROQ_FALLBACK', '0') == '1'
    if use_groq:
        print('[llm_client] Using Groq fallback')
        return _call_groq(prompt, system_prompt, max_tokens)
    else:
        print('[llm_client] Using Ollama (local)')
        return _call_ollama(prompt, system_prompt, max_tokens)


if __name__ == '__main__':
    # Quick smoke test
    response = generate('Respond with exactly: LLM_CLIENT_OK')
    print(f'Response: {response}')
