from therix.utils.summarizer import async_summarizer, summarizer
from therix.utils.default_chat import invoke_default_chat
from ..db.session import SessionLocal
from ..entities.models import ConfigType, Pipeline, PipelineConfiguration
import json
import os
import urllib
from therix.services.web_crawling import crawl_website
from therix.utils.pii_filter import pii_filter
from ..db.session import SessionLocal
from therix.utils.rag import (
    chat,
    create_embeddings,
    get_embedding_model,
    get_vectorstore,
    get_loader,
    async_chat,
)
from langchain_openai import AzureOpenAIEmbeddings
from therix.utils.keyword_search import async_keyword_search, keyword_search
from langchain.retrievers.merger_retriever import MergerRetriever


class PipelineService:
    def __init__(self):
        self.db_session = SessionLocal()

    def create_pipeline_with_configurations(self, pipeline_data, configurations_data):
        new_pipeline = Pipeline(**pipeline_data)
        self.db_session.add(new_pipeline)
        self.db_session.flush()  # Flush to assign an ID to the new_pipeline

        for config_data in configurations_data:
            config_data["pipeline_id"] = new_pipeline.id
            new_config = PipelineConfiguration(**config_data)
            if new_config.config_type == "INFERENCE_MODEL":
                if "temperature" not in new_config.config:
                    new_config.config["temperature"] = 0.5
            self.db_session.add(new_config)

        self.db_session.commit()
        return new_pipeline

    def publish_pipeline(self, pipeline_data):
        pipeline = (
            self.db_session.query(Pipeline).filter_by(id=pipeline_data.id).first()
        )
        pipeline.status = "PUBLISHED"
        self.db_session.commit()
        return pipeline

    def get_pipeline(self, pipeline_id):
        return self.db_session.query(Pipeline).filter_by(id=pipeline_id).first()

    def get_pipeline_configuration(self, pipeline_id: str):
        return (
            self.db_session.query(PipelineConfiguration)
            .filter_by(pipeline_id=pipeline_id)
            .all()
        )

    def get_pipeline_configuraitons_by_type(self, pipeline_id, config_type):
        return (
            self.db_session.query(PipelineConfiguration)
            .filter_by(pipeline_id=pipeline_id, config_type=config_type)
            .all()
        )

    def preprocess_data(self, pipeline_id):
        data_sources = self.get_pipeline_configuraitons_by_type(
            pipeline_id, "INPUT_SOURCE"
        )
        output_file = None
        if "website" in data_sources[0].config:
            website_url = data_sources[0].config["website"]
            web_content = crawl_website(website_url)
            domain_name = urllib.parse.urlparse(website_url).netloc
            output_file = f"{domain_name}_data.json"
            with open(output_file, "w") as f:
                json.dump(web_content, f, indent=4)
            data_sources[0].config["files"] = [output_file]
        if "website" in data_sources[0].config:
            os.remove(output_file)
        embedding_model = self.get_pipeline_configuraitons_by_type(
            pipeline_id, "EMBEDDING_MODEL"
        )
        return create_embeddings(data_sources, embedding_model[0], str(pipeline_id))

    async def async_invoke_pipeline(
        self,
        pipeline_id,
        question,
        session_id,
        trace_details=None,
        system_prompt=None,
        pipeline_ids=None,
        output_parser=None,
    ):
        embedding_model = self.get_pipeline_configuraitons_by_type(
            pipeline_id, "EMBEDDING_MODEL"
        )

        if pipeline_ids:
            combined_retrievers = []
            for individual_pipeline_id in pipeline_ids:
                embedding_model = self.get_pipeline_configuraitons_by_type(
                    individual_pipeline_id, "EMBEDDING_MODEL"
                )
                store = get_vectorstore(embedding_model[0], str(individual_pipeline_id))
                combined_retrievers.append(store.as_retriever())
            retreiver = MergerRetriever(retrievers=combined_retrievers)

        else:
            store = get_vectorstore(embedding_model[0], str(pipeline_id))
            retreiver = store.as_retriever()

        inference_model = self.get_pipeline_configuraitons_by_type(
            pipeline_id, "INFERENCE_MODEL"
        )

        pii_filter_config = self.get_pipeline_configuraitons_by_type(
            pipeline_id, ConfigType.PII_FILTER
        )
        if len(pii_filter_config) != 0:
            pii_filter_config = pii_filter_config[0]
        else:
            pii_filter_config = None

        result = await async_chat(
            question,
            retreiver,
            inference_model[0],
            embedding_model,
            session_id,
            pipeline_id,
            trace_details,
            pii_filter_config,
            system_prompt,
            output_parser,
        )

        if pii_filter_config:
            pii_filter_config = pii_filter_config.config
            entities = pii_filter_config["entities"]
            return pii_filter(result, entities)
        else:
            return result

    def invoke_pipeline(
        self,
        pipeline_id,
        question,
        session_id,
        trace_details=None,
        system_prompt=None,
        pipeline_ids=None,
        output_parser=None,
    ):
        embedding_model = self.get_pipeline_configuraitons_by_type(
            pipeline_id, "EMBEDDING_MODEL"
        )

        if pipeline_ids:
            combined_retrievers = []
            for individual_pipeline_id in pipeline_ids:
                embedding_model = self.get_pipeline_configuraitons_by_type(
                    individual_pipeline_id, "EMBEDDING_MODEL"
                )
                store = get_vectorstore(embedding_model[0], str(individual_pipeline_id))
                combined_retrievers.append(store.as_retriever())
            retreiver = MergerRetriever(retrievers=combined_retrievers)

        else:
            store = get_vectorstore(embedding_model[0], str(pipeline_id))
            retreiver = store.as_retriever()

        inference_model = self.get_pipeline_configuraitons_by_type(
            pipeline_id, "INFERENCE_MODEL"
        )

        pii_filter_config = self.get_pipeline_configuraitons_by_type(
            pipeline_id, ConfigType.PII_FILTER
        )
        if len(pii_filter_config) != 0:
            pii_filter_config = pii_filter_config[0]
        else:
            pii_filter_config = None

        result = chat(
            question,
            retreiver,
            inference_model[0],
            embedding_model,
            session_id,
            pipeline_id,
            trace_details,
            pii_filter_config,
            system_prompt,
            output_parser,
        )

        if pii_filter_config:
            pii_filter_config = pii_filter_config.config
            entities = pii_filter_config["entities"]
            return pii_filter(result, entities)
        else:
            return result

    async def async_invoke_summarizer_pipeline(
        self, pipeline_id, text, trace_details=None, system_prompt=None
    ):
        inference_model = self.get_pipeline_configuraitons_by_type(
            pipeline_id, ConfigType.INFERENCE_MODEL
        )
        summarizer_config = self.get_pipeline_configuraitons_by_type(
            pipeline_id, ConfigType.SUMMARIZER
        )[0].config
        return await async_summarizer(
            summarizer_config, inference_model[0], text, trace_details, system_prompt
        )

    def invoke_summarizer_pipeline(
        self, pipeline_id, text, trace_details=None, system_prompt=None
    ):
        inference_model = self.get_pipeline_configuraitons_by_type(
            pipeline_id, ConfigType.INFERENCE_MODEL
        )
        summarizer_config = self.get_pipeline_configuraitons_by_type(
            pipeline_id, ConfigType.SUMMARIZER
        )[0].config
        return summarizer(
            summarizer_config, inference_model[0], text, trace_details, system_prompt
        )

    def invoke_default_pipeline(
        self, pipeline_id, session_id, question, trace_details=None
    ):
        inference_model = self.get_pipeline_configuraitons_by_type(
            pipeline_id, ConfigType.INFERENCE_MODEL
        )
        return invoke_default_chat(
            inference_model[0], session_id, pipeline_id, question, trace_details
        )

    def async_search_keywords(self, keyword_search_params):
        if (
            not keyword_search_params.get("prompt")
            or not keyword_search_params.get("keywords")
            or not keyword_search_params.get("output_parser")
        ):
            return "Request is missing required parameters, please provide all the parameters, i.e. pipeline_id, config_id, prompt, keywords, output_parser"

        if "pipeline_ids" in keyword_search_params and len(
            keyword_search_params.get("pipeline_ids")
        ):
            combined_retrievers = []
            inference_model = self.get_pipeline_configuraitons_by_type(
                keyword_search_params.get("pipeline_ids")[
                    len(keyword_search_params.get("pipeline_ids")) - 1
                ],
                ConfigType.INFERENCE_MODEL,
            )
            for pipeline_id in keyword_search_params.get("pipeline_ids"):
                embedding_model = self.get_pipeline_configuraitons_by_type(
                    pipeline_id, ConfigType.EMBEDDING_MODEL
                )
                store = get_vectorstore(embedding_model[0], str(pipeline_id))
                combined_retrievers.append(store.as_retriever())
            retriever = MergerRetriever(retrievers=combined_retrievers)
        else:
            inference_model = self.get_pipeline_configuraitons_by_type(
                keyword_search_params.get("pipeline_id"), ConfigType.INFERENCE_MODEL
            )
            embedding_model = self.get_pipeline_configuraitons_by_type(
                keyword_search_params.get("pipeline_id"), ConfigType.EMBEDDING_MODEL
            )
            store = get_vectorstore(
                embedding_model[0], str(keyword_search_params.get("pipeline_id"))
            )
            retriever = store.as_retriever()

        keyword_search_dict = {
            "retriever": retriever,
            "keywords": keyword_search_params.get("keywords"),
            "output_parser": keyword_search_params.get("output_parser"),
            "prompt": keyword_search_params.get("prompt"),
            "trace_details": keyword_search_params.get("trace_details"),
            "inference_model": inference_model[0],
        }
        return async_keyword_search(keyword_search_dict)

    def search_keywords(self, keyword_search_params):
        if (
            not keyword_search_params.get("prompt")
            or not keyword_search_params.get("keywords")
            or not keyword_search_params.get("output_parser")
        ):
            return "Request is missing required parameters, please provide all the parameters, i.e. pipeline_id, config_id, prompt, keywords, output_parser"

        if "pipeline_ids" in keyword_search_params and len(
            keyword_search_params.get("pipeline_ids")
        ):
            combined_retrievers = []
            inference_model = self.get_pipeline_configuraitons_by_type(
                keyword_search_params.get("pipeline_ids")[
                    len(keyword_search_params.get("pipeline_ids")) - 1
                ],
                ConfigType.INFERENCE_MODEL,
            )
            for pipeline_id in keyword_search_params.get("pipeline_ids"):
                embedding_model = self.get_pipeline_configuraitons_by_type(
                    pipeline_id, ConfigType.EMBEDDING_MODEL
                )
                store = get_vectorstore(embedding_model[0], str(pipeline_id))
                combined_retrievers.append(store.as_retriever())
            retriever = MergerRetriever(retrievers=combined_retrievers)
        else:
            inference_model = self.get_pipeline_configuraitons_by_type(
                keyword_search_params.get("pipeline_id"), ConfigType.INFERENCE_MODEL
            )
            embedding_model = self.get_pipeline_configuraitons_by_type(
                keyword_search_params.get("pipeline_id"), ConfigType.EMBEDDING_MODEL
            )
            store = get_vectorstore(
                embedding_model[0], str(keyword_search_params.get("pipeline_id"))
            )
            retriever = store.as_retriever()

        keyword_search_dict = {
            "retriever": retriever,
            "keywords": keyword_search_params.get("keywords"),
            "output_parser": keyword_search_params.get("output_parser"),
            "prompt": keyword_search_params.get("prompt"),
            "trace_details": keyword_search_params.get("trace_details"),
            "inference_model": inference_model[0],
        }
        return keyword_search(keyword_search_dict)

    def __del__(self):
        self.db_session.close()
