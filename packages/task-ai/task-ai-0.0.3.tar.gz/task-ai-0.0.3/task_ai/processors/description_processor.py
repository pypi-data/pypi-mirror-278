import pkg_resources
import yaml
import os

class DescriptionProcessor():
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger
        self.example_path = config.get("prompt_example_path", None)
        self.description_config = self.config.get("description", {})

    def process(self, json_data):
        json_type = json_data.get('type')
        if not json_type:
            raise ValueError("The 'type' field is missing in the actual JSON.")
    
        self.examples = self.load_template(f"{json_type}.yaml")
        self.logger.debug("Loaded template for type %s", json_type)
        self.logger.debug("Template content:\n%s", self.examples)

        description = self.ask_ai(json_data=json_data)
        self.logger.debug("AI response: %s", description)
        if self.description_config.get("multi_line", False):
            return self.format_description(description)
        else:
            return description

    def update_values(self, description, removed_values):
        for key, value in removed_values.items():
            description = description.replace(f"{{{key}}}", f"'{value}'")
        return description
    
    def format_description(self, description):
        description = description.replace(". ", ".\n")
        desc_lines = description.split("\n")
        new_desc = []
        new_desc.append(desc_lines.pop(0))
        new_desc = new_desc + sorted(desc_lines)
        return "\n".join(new_desc)

    def load_template(self, template_name):
        if self.example_path is None:
            self.example_path = pkg_resources.resource_filename(__name__, "prompts/examples")

        template_file = os.path.join(self.example_path, template_name)
        
        with open(template_file, 'r') as file:
            return yaml.safe_load(file)
        
    def generate_prompt(self, json_data):
        base_prompt = self.config.get("llm", {}).get("base_prompt", "")
        messages = []
        for example in self.examples.get("examples", []):
            input = example.get("input")
            output = example.get("output")
            messages.append({"role": "user", "content": f'''Convert the following JSON input into a detailed, human-readable description:
                {input}
                '''})
            messages.append({"role": "assistant", "content": f''' {output} '''})
        messages.append({'role': 'user', 'content': f"""Convert the following JSON input into a detailed, human-readable description:
        {base_prompt}

        {json_data}
                """})
        return messages
    
    def ask_ai(self, json_data):
        provider = self.config.get("llm", {}).get("provider", "ollama")
        prompt = self.generate_prompt(json_data)
        self.logger.debug("Prompt: %s", prompt)

        if provider == "ollama":
            response = self.ask_ollama(prompt)
        elif provider == "openai":
            response = self.ask_openai(prompt)

        return response
    
    def ask_ollama(self, prompt):
        from ollama import Client
        api_base = self.config.get("llm", {}).get("api_base", "http://localhost:11434")
        model = self.config.get("llm", {}).get("model", "llama3:latest")

        client = Client(host=api_base)
        response = client.chat(model=model, messages=prompt)
        human_readable_text = response['message']['content'].strip()
        return human_readable_text

    def ask_openai(self, prompt):
        from openai import OpenAI

        api_key = self.config.get("llm", {}).get("api_key", None)
        model = self.config.get("llm", {}).get("model", "gpt-4o")
        temperature = self.config.get("llm", {}).get("temperature", 0.2)
        max_tokens = self.config.get("llm", {}).get("max_tokens", 1024)

        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=prompt,
            max_tokens=max_tokens, 
            temperature=temperature
            )
        human_readable_text = response.choices[0].message.content.strip()
        return human_readable_text