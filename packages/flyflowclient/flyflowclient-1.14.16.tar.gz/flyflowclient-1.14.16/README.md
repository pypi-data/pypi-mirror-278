# Flyflow

Flyflow is a Python client library for interacting with the Flyflow API. It provides a simple and intuitive interface to manage agents, calls, and perform various operations related to the Flyflow platform.

## Installation

You can install the Flyflow package using pip:

```
pip install flyflowclient
```

## Usage

To use the Flyflow client library, you need to import the `Flyflow` class from the `flyflow.client` module:

```python
from flyflowclient import Flyflow

client = Flyflow()
```

By default, the client will load the API key from the `FLYFLOW_API_KEY` environment variable. If you want to provide the API key explicitly, you can pass it as a parameter when creating the client instance:

```python
client = Flyflow(api_key='your_api_key')
```

The default base URL for the Flyflow API is `https://api.flyflow.dev/v1`. If you need to use a different base URL, you can pass it as a parameter:

```python
client = Flyflow(base_url='https://custom-api-url.com')
```

### Agent Management

#### Upsert an Agent

```python
agent = client.upsert_agent(
   name='Agent Name',
   system_prompt='System prompt',
   initial_message='Initial message',
   llm_model='gpt-3.5-turbo',
   voice_id='voice_id',
   webhook='https://webhook-url.com',
   tools=[],
   filler_words=True,
   actions=[],
   voicemail_number='+1234567890',
   chunking=True,
   endpointing=200,
   voice_optimization=2
)
```

The `upsert_agent` method will create a new agent if one with the specified name doesn't exist, or update an existing agent if one with the same name already exists.

#### Get an Agent

```python
agent = client.get_agent(agent_id=agent['id'])
```

#### Delete an Agent

```python
client.delete_agent(agent_id=agent['id'])
```

#### List Agents

```python
agents = client.list_agents(limit=10)
```

### Call Management

#### Create a Call

```python
call = client.create_call(
    from_number='+1234567890',
    to_number='+9876543210',
    context='Call context'
)
```

#### Get a Call

```python
call = client.get_call(call_id=call['id'])
```

#### Set Call Context

```python
updated_call = client.set_call_context(
   call_id=call['id'],
   context='Updated call context'
)
```

#### List Calls

```python
calls = client.list_calls(limit=10, agent_id=agent['id'])
```

### Filler Words

#### Get Filler Words

```python
filler_words = client.get_filler_words(text='Your text here')
```

For more detailed information about the available methods and their parameters, please refer to the Flyflow API documentation.

## Publishing the Package

To publish the Flyflow package to PyPI, follow these steps:

1. Make sure you have the latest version of `setuptools` and `wheel` installed:
   ```
   pip install --upgrade setuptools wheel
   ```

2. Run the following command to build the package:
   ```
   python setup.py sdist bdist_wheel
   ```

3. Install `twine` if you haven't already:
   ```
   pip install twine
   ```

4. Upload the package to PyPI using `twine`:
   ```
   twine upload dist/*
   ```

   You will be prompted to enter your PyPI username and password.

5. Once the upload is successful, your package will be available on PyPI, and users can install it using `pip install flyflow`.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please open an issue or submit a pull request on the [GitHub repository](https://github.com/your-username/flyflow).
