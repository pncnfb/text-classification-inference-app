from configparser import ConfigParser

from google.cloud import aiplatform
from vertexai.generative_models._generative_models import (
    HarmBlockThreshold,
    HarmCategory,
)
from llama_index.core import PromptTemplate
from llama_index.core.output_parsers import PydanticOutputParser
from llama_index.core.program import LLMTextCompletionProgram
from llama_index.llms.vertex import Vertex

from src.models import Notes

config = ConfigParser()

from google.oauth2 import service_account

class NotesAgent:
    def __init__(self, agent_config):
        credentials = service_account.Credentials.from_service_account_file(agent_config["GCP_JSON_CREDS_PATH"])
        aiplatform.init(project=agent_config["GCP_PROJECT_ID"], location=agent_config["GCP_REGION"],credentials=credentials)

        self.llm = self._get_llm
        print(agent_config)
        self.prompt_template = agent_config["PROMPT_TEMPLATE"]
        self.agent_config = agent_config

    def _get_llm(self):
        """
        The `_get_llm` function returns a `Vertex` object with specific model, project, and location
        configurations.
        :return: An instance of the Vertex class with the specified model, project, and location parameters.
        """
        return Vertex(
            model=self.agent_config["MODEL"],
            temperature=self.agent_config["TEMPERATURE"],
            max_retries=self.agent_config["MAX_RETRIES"],
            max_tokens=self.agent_config["MAX_TOKENS"],
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_UNSPECIFIED: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            },
        )

    def segment_and_classify_notes(self, clinical_text)->Notes:
        """ """
        try:
            llm = self._get_llm()
            parser = PydanticOutputParser(output_cls=Notes)

            prompt_template = PromptTemplate(
                template=self.prompt_template,
            )

            pydantic_llm_assistant = LLMTextCompletionProgram.from_defaults(
                output_cls=Notes,
                output_parser=parser,
                prompt=prompt_template,
                llm=llm,
                verbose=True,
            )

            output = pydantic_llm_assistant(
                query=self.prompt_template,
                clinical_text=clinical_text,
            )

            return output.notes


        except Exception as e:
            print(e)
            return None