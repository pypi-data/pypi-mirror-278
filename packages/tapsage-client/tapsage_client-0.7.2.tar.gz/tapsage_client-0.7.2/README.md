# Tapsage Python Client

This Python client is designed to provide developers with a seamless integration into the Tapsage platform, enabling the efficient management and customization of generative AI-driven chatbots and image generation models.

## Features

- **API Integration**: Easy access to Tapsage's API endpoints for model selection, configuration, and management.
- **Model Customization**: Tools to customize and fine-tune large language models (LLMs) for text and image generation according to specific requirements.
- **Monitoring**: Capabilities to monitor the performance and quality of AI models, ensuring optimal functionality.
- **Simplified Deployment**: Streamlined processes for transitioning from model development to production.

## Installation

To install the Tapsage Python Client, run the following command:

```bash
pip install tapsage-client
```

## Usage

### Session
Here’s a quick example of how to use the client to interact with Tapsage:

```python
import tapsage

# Initialize the client
tapbot = tapsage.TapSageBot(api_key=TAPSAGE_API_KEY, bot_id=TAPSAGE_BOT_ID)

# Initialize a session
session = tapbot.create_session()
message = tapbot.send_message(session, "Suggest me a list of 5 gifts for a 30 years boy who is tech-fan.")
print(message.content)
message2 = tapbot.send_message(session, "What if he is a book lover?")
print(message2.content)

# Delete a session
tapbot.delete_session(session)
```

### Async
Here’s an example of async operation:

```python
import tapsage

# Initialize the client
tapbot = tapsage.TapSageBot(api_key=TAPSAGE_API_KEY, bot_id=TAPSAGE_BOT_ID)

prompt = "Suggest me a list of 5 gifts for a 30 years boy who is tech-fan."
session = tapbot.create_session()
task = tapbot.send_message_async(session, prompt)

while True:
    task_result = tapbot.retrieve_async_task(session, task)
    if task_result.status == "FINISHED":
        break
    time.sleep(1)
print(task_result.message.content)
print()
tapbot.delete_session(session)
```

### Stream
Here’s an example of stream usage:

```python
import tapsage

# Initialize the client
tapbot = tapsage.TapSageBot(api_key=TAPSAGE_API_KEY, bot_id=TAPSAGE_BOT_ID)

prompt = "Suggest me a list of 5 gifts for a 30 years boy who is tech-fan."
stream = tapbot.stream_messages(
    session, prompt, split_criteria={"line": True}
)
for message in stream:
    print(message.message.content)
tapbot.delete_session(session)
```


## Configuration
Before using the client, ensure you configure it with your API key:

```python
tapbot = tapsage.TapSageBot(api_key=TAPSAGE_API_KEY, bot_id=TAPSAGE_BOT_ID)
```

## Documentation
For more detailed information about the client's methods and additional functionalities, refer to the [Tapsage Documentation](https://docs.tapsage.com/).

## Support
If you encounter any issues or have questions, please contact hello@tapsage.com.

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/mahdikiani/tapsage-python/blob/main/LICENSE) file for details.