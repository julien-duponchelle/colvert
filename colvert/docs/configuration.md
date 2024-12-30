# Configuration

[TOC]

The settings are stored in the `colvert.toml` file. This file is located in the user standard config directory (example on Linux `~/.config/colvert/colvert.toml`)

## Manipulate settings via the CLI

The command line interface is also available to modify the settings.

### Set a setting

```console
$ colvert config set <section> <key> <value>
```

!!!warning
    You need to restart all running colvert instances to apply the changes.

### Get the path to the settings file

```console
$ colvert config path
```

## Available configuration

### Section: ai

|Key|Value|
|---|---|
| model | The model to use for the AI (see [AI](/docs/ai.md)) |
| api_key | The API key to use for the AI |