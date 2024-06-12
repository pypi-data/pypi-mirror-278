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

import json
import logging

from bedrock_util.bedrock_genai_util.BedrockUtil import BedrockUtil

logger = logging.getLogger(__name__)


class AwsTitanBedrockUtil(BedrockUtil):
    def text_completion(
        self,
        bedrock_client,
        model,
        prompt,
        guardrail_identifier=None,
        guardrail_version=None,
        **model_kwargs,
    ):
        prompt_request = {}
        prompt_response = {}

        if prompt:
            prompt_request["inputText"] = prompt

            text_config = {
                "temperature": model_kwargs.get("temperature"),
                "topP": model_kwargs.get("top_p"),
                "maxTokenCount": model_kwargs.get("max_token"),
            }
            stop_sequences = model_kwargs.get("stop_sequences")

            if stop_sequences:
                text_config["stopSequences"] = [
                    seq.strip() for seq in stop_sequences.split(",") if seq.strip()
                ]

            text_config = {k: v for k, v in text_config.items() if v}

            if text_config:
                prompt_request["textGenerationConfig"] = text_config

            body = json.dumps(prompt_request)
            accept = "application/json"
            content_type = "application/json"

            try:
                if guardrail_identifier is None and guardrail_version is None:
                    response = bedrock_client.invoke_model(
                        body=body,
                        modelId=model,
                        accept=accept,
                        contentType=content_type,
                    )
                else:
                    response = bedrock_client.invoke_model(
                        body=body,
                        modelId=model,
                        accept=accept,
                        contentType=content_type,
                        guardrailIdentifier=guardrail_identifier,
                        guardrailVersion=guardrail_version,
                    )
                response_body = json.loads(response.get("body").read())
                prompt_response["output"] = response_body["results"][0]["outputText"]
            except Exception as e:
                logger.exception(
                    f"Error in text_completion for model {model}: {str(e)}"
                )
                raise

        return prompt_response
