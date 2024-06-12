# Copyright (c) 2024 Biprajeet Kar

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import logging
from bedrock_util import yaml
from bedrock_util.bedrock_genai_util.TextCompletionUtil import generate_text_completion
from bedrock_util.bedrock_genai_util.model_map import model_map

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def __read_prompt_config(file_path):
    try:
        with open(file_path, "r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        logger.error(f"The file {file_path} does not exist.")
    except Exception as e:
        logger.exception(f"Error decoding YAML in file {file_path}: {e}")
    return None


def __validate_model(service_id, model):
    if service_map.get("PromptServices", {}).get(service_id):
        service = service_map["PromptServices"][service_id]
        allowed_providers = service.get("allowedFoundationModelProviders")
        if allowed_providers and model_map.get(model) in allowed_providers:
            return True
    logger.warning(f"Model ID {model} not allowed for service {service_id}")
    return False


def __validate_prompt_inputs(service_id, prompt_inputs):
    if service_map.get("PromptServices", {}).get(service_id):
        service = service_map["PromptServices"][service_id]
        input_variables = service.get("inputVariables")
        if (not input_variables and not prompt_inputs) or (
            input_variables
            and prompt_inputs
            and sorted(input_variables) == sorted(prompt_inputs.keys())
        ):
            return True
    logger.warning(f"Invalid inputs provided for service ID {service_id}")
    return False


def run_service(
    bedrock_client, service_id, model_id, prompt_input_variables=None, **model_kwargs
):
    if __validate_model(service_id, model_id) and __validate_prompt_inputs(
        service_id, prompt_input_variables
    ):
        prompt = service_map["PromptServices"][service_id]["prompt"]
        guardrail_identifier = service_map["PromptServices"][service_id].get(
            "guardrailIdentifier"
        )
        guardrail_version = service_map["PromptServices"][service_id].get(
            "guardrailVersion"
        )
        formatted_prompt = prompt.format(**(prompt_input_variables or {}))
        return generate_text_completion(
            bedrock_client,
            model_id,
            formatted_prompt,
            guardrail_identifier,
            guardrail_version,
            **model_kwargs,
        )


service_map = __read_prompt_config("prompt_store.yaml")
