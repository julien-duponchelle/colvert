# AI

Colvert support AI model to generate SQL queries. It's use [litellm](https://github.com/BerriAI/litellm) to wrap the call to the AI model.

[TOC]

## Settings

To use an AI model you need to configure the model and the API key using the following commands:

```console
$ colvert config set ai model <model>
$ colvert config set ai api_key <api_key>
```


You can also edit the colvert.toml file to set the model and the API key:

```toml
[ai]
model = "model"
api_key = "api_key"
```

## Test the connection

This command allow you to test the connection to the AI model:

```console
$ colvert ai test
```

## Common providers

### OpenAI

Create an API key for the OpenAI model in your [console](https://platform.openai.com/settings/organization/api-keys)

```console
$ colvert config set ai model openai/gpt-4o-mini
$ colvert config set ai api_key YOUR_KEY
```

For all supported models look at [LiteLLM documentation](https://docs.litellm.ai/docs/providers/openai#openai-chat-completion-models)

### Claude Anthropic

Create an API key for the Claude model in your [console](https://console.anthropic.com)

```console
$ colvert config set ai model anthropic/claude-3-5-sonnet-20240620
$ colvert config set ai api_key YOUR_KEY
```

For all supported models look at [LiteLLM documentation](https://docs.litellm.ai/docs/providers/anthropic#supported-models)

### Mistral 

Create an API key for the Mistral model in your [console](https://console.mistral.ai/api-keys/)


```console
$ colvert config set ai model mistral/mistral-large-latest
$ colvert config set ai api_key YOUR_KEY
```

For all supported models look at [LiteLLM documentation](https://docs.litellm.ai/docs/providers/mistral#supported-models)

### Other 

You can see the list of supported provider on LiteLLM [docs](https://litellm.com/docs/providers)