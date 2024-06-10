# TASK-AI: CLI for describing Stonebranch task definitions

## Overview

Task AI is a powerful command-line tool designed to process Stonebranch Task JSON data, offering features like anonymization, parsing, and description generation. It's built with flexibility and ease of use in mind, making it ideal for various data analysis and manipulation tasks.

### Key Features:

* Anonymization: Securely anonymize sensitive data within your JSON files using configurable rules.
* Parsing: Process and structure your JSON data according to your specific needs.
* Description Generation: Generate clear and concise descriptions based on the processed JSON data.
* Configuration: Customize Task AI's behavior through a simple YAML configuration file.
* Logging: Track the tool's progress and debug issues with detailed logging capabilities.
* Command-Line Interface: Enjoy a user-friendly command-line interface for easy interaction.


### Getting Started:

`Installation`: Install Task AI using pip: 

```bash
pip install task-ai
```

`Configuration`: Create a configuration file (e.g., ~/.uac/task_ai.yml) to define your anonymization rules, parsing options, and other settings.
Usage: Run Task AI from your terminal, specifying the input JSON file and any desired options.

#### Sample Config
```yaml
template_path: task_ai/templates
prompt_example_path: task_ai/prompts/examples
llm:
  provider: "ollama"
  api_base: "http://localhost:11434"
  model: "llama3:latest"
  # For OpenAI use the following configuration
  # provider: "openai"
  # api_key: "sk-xxxxx
  # model: "gpt-4o"
  # temperature: 0.2
  # max_tokens: 1024
  # base_prompt: >
  # If there are notes just summarize the content of the notes. Do not include any notes in the output.
anonymization:
  fields:
    - agent
    - name
    - script
    - sysId
    - agentVar
    - command
    - parameters
    - summary
    - agent_cluster
    - broadcastCluster
    - credentials
    - runtimeDir
processing:
  exclude:
    - sysId
    - version
    - firstRun
    - lastRun
    - exportReleaseLevel
    - lastRunTimeDisplay
    - minRunTimeDisplay
    - maxRunTimeDisplay
    - avgRunTimeDisplay
    - notes
  include:
    - type

```
Example:
```bash
task-ai -i input.json -c config.yml -s
```

This command will process input.json using the settings in config.yml, anonymize the data, and display the anonymized JSON output and the description of the task.

You can use this tool combined with UAC-CLI tool like this.
```bash
uac task get task_name="Linux Sleep 10" | task-ai -s
```
Output
```
{
    "type": "taskUnix",
    "agent": "{agent}",
    "command": "{command}",
    "name": "{name}"
}
Unix task running on 'AGENT1' agent with name 'Linux Sleep 10' that will run a command as 'sleep 10'.
```

# Security

Your data will be anonymized using the provided rules. Sensitive data will not be sent to LLM API. Sensitive data is defined by the fields in the config file.

The sensitive data will be replaced with a string of {field_name}, for example: `Agent` will be replaced with `{agent}`. Once the description returned from LLM API, it will be replaced back to its original value.