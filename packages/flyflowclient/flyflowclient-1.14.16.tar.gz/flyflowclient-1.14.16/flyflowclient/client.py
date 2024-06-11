import os
import requests

class Flyflow:
    def __init__(self, api_key=None, base_url=None):
        self.api_key = api_key or os.getenv('FLYFLOW_API_KEY')
        self.base_url = base_url or 'https://api.flyflow.dev/v1'
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def create_call(self, from_number, to_number, context='', user_speaks_first=False):
        payload = {
            'from': from_number,
            'to': to_number,
            'context': context,
            'user_speaks_first': user_speaks_first,
        }
        response = requests.post(f'{self.base_url}/call', json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_call(self, call_id):
        response = requests.get(f'{self.base_url}/call', params={'id': call_id}, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def set_call_context(self, call_id, context):
        payload = {
            'id': call_id,
            'context': context
        }
        response = requests.post(f'{self.base_url}/call/context', json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def list_calls(self, cursor=None, limit=10, agent_id=None, client_number=None):
        params = {
            'cursor': cursor,
            'limit': limit,
            'agent_id': agent_id,
            'client_number': client_number
        }
        response = requests.get(f'{self.base_url}/calls', params=params, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def upsert_agent(self, name, system_prompt=None, initial_message=None, voice_id=None, llm_model=None, webhook=None, tools=None, filler_words=None, filler_words_whitelist=None, actions=None, voicemail_number=None, chunking=None, endpointing=None, voice_optimization=None, smart_endpointing_threshold=None):
        payload = {
            'name': name,
            'system_prompt': system_prompt,
            'initial_message': initial_message,
            'voice_id': voice_id,
            'llm_model': llm_model,
            'webhook': webhook,
            'tools': tools,
            'filler_words': filler_words,
            'filler_words_whitelist': filler_words_whitelist,
            'actions': actions,
            'voicemail_number': voicemail_number,
            'chunking': chunking,
            'endpointing': endpointing,
            'voice_optimization': voice_optimization,
            'smart_endpointing_threshold': smart_endpointing_threshold
        }
        response = requests.post(f'{self.base_url}/agent', json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_agent(self, agent_id):
        response = requests.get(f'{self.base_url}/agent', params={'id': agent_id}, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def delete_agent(self, agent_id):
        response = requests.delete(f'{self.base_url}/agent', params={'id': agent_id}, headers=self.headers)
        response.raise_for_status()

    def list_agents(self, cursor=None, limit=10):
        params = {
            'cursor': cursor,
            'limit': limit
        }
        response = requests.get(f'{self.base_url}/agents', params=params, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_filler_words(self, text):
        params = {'text': text}
        response = requests.get(f'{self.base_url}/filler-words', params=params, headers=self.headers)
        response.raise_for_status()
        return response.json()