# unofficial_ffm_openai_client
An unofficial Formosa Foundation Model client implementation based on OpenAI and LangChain

## Introduction

This is an unofficial Python client implementation for the Formosa Foundation Model public endpoint, compatible with the OpenAI Python client and LangChain. Currently, it only implements the [Conversation API](https://docs.twcc.ai/docs/user-guides/twcc/afs/afs-modelspace/api-and-parameters/conversation-api) and supports the public endpoint. Note that the synchronous API is not yet implemented.

## Usage

Install using pypi:

```shell
pip install unofficial-ffm-openai
```

You can use it similarly to the original OpenAIChat, with a few different parameters:

```python
from ffm.langchain.language_models.ffm import FfmChatOpenAI

chat_ffm = FfmChatOpenAI(
    ffm_endpoint="https://api-ams.twcc.ai/api",
    max_tokens=1000,
    temperature=0.5,
    top_k=50,
    top_p=1.0,
    frequency_penalty=1.0,
    ffm_api_key="your key",
    ffm_deployment="ffm-mistral-7b-32k-instruct",  # or other model name
    streaming=True,
    callbacks=callbacks
)
```

```python
from ffm.embeddings import FFMEmbeddings

embedding = FFMEmbeddings(
    base_url="",
    api_key="your key")
```

## Limitation

Currently, it has only been tested with the following dependencies:

```
langchain                         0.1.20
langchain-community               0.0.38
langchain-core                    0.1.52
langchain-openai                  0.1.7
langchain-text-splitters          0.0.2
langchainhub                      0.1.15
```

and the OpenAI client:

```
openai                            1.30.1
```

## TODO

* Full implementation for the synchronous API.
* Support for function calls.