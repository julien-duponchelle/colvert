# AI

Colvert support AI model to generate SQL queries. It's use [litellm](https://github.com/BerriAI/litellm) to wrap the call to the AI model.

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

### Mistral 

Create an API key for the Mistral model in your [console](https://console.mistral.ai/api-keys/)


```console
$ colvert config set ai model mistral/codestral-latest
$ colvert config set ai api_key YOUR_KEY
```

### Other 

You can see the list of supported provider on LiteLLM [docs](https://litellm.com/docs/providers)