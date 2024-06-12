import json, uuid
from operator import itemgetter
from pathlib import Path
from urllib import response
from langchain.docstore.document import Document
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_community.vectorstores.pgvector import PGVector
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_openai import AzureChatOpenAI
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders.youtube import YoutubeLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureOpenAIEmbeddings
from therix.core.JSONLoader import JSONLoader
from langchain_community.embeddings.bedrock import BedrockEmbeddings
import boto3
from langchain_community.llms import Bedrock
from therix.core.chat_history.base_chat_history import TherixChatMessageHistory
from therix.core.constants import (
    DataSourceMaster,
    EmbeddingModelMaster,
    InferenceModelMaster,
)
from therix.db.session import SQLALCHEMY_DATABASE_URL
from langfuse.callback import CallbackHandler
from langchain_core.prompts import PromptTemplate
from langchain_community.vectorstores.pgvector import PGVector
from langchain.prompts import PromptTemplate
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import get_buffer_string
from langchain_core.prompts import format_document
from langchain_core.runnables import RunnableParallel
from langchain_text_splitters import  RecursiveCharacterTextSplitter
from operator import itemgetter
from langchain_experimental.data_anonymizer import PresidioReversibleAnonymizer
from langchain_core.messages.chat import ChatMessage

def sanitize_text(text):
    # Remove null characters (0x00) from the text
    sanitized_text = text.replace("\x00", "")
    return sanitized_text


def get_loader(file_type, file_path, config):
    if file_type == DataSourceMaster.TEXT:
        return TextLoader(file_path)
    elif file_type == DataSourceMaster.PDF:
        return PyPDFLoader(file_path)
    elif file_type == DataSourceMaster.YOUTUBE:
        return YoutubeLoader.from_youtube_url(
            file_path,
            add_video_info=True,
            language=[config["language"], "id"],
            translation="en",
        )
        return PyPDFLoader(file_path)
    elif file_type == DataSourceMaster.WEBSITE:
        return JSONLoader(file_path)
    else:
        raise ValueError(f"Unknown data source type: {file_type}")


def get_embedding_model(embedding_model_name, config):
    if (
        embedding_model_name == EmbeddingModelMaster.OPENAI_TEXT_ADA
        or embedding_model_name == EmbeddingModelMaster.OPENAI_TEXT_EMBEDDING_3_SMALL
        or embedding_model_name == EmbeddingModelMaster.OPENAI_TEXT_EMBEDDING_3_LARGE
    ) and ("api_key" in config):
        return OpenAIEmbeddings(
            openai_api_key=config["api_key"], model=embedding_model_name
        )
    elif (
        embedding_model_name == EmbeddingModelMaster.AZURE_TEXT_ADA
        or embedding_model_name == EmbeddingModelMaster.AZURE_TEXT_EMBEDDING_3_LARGE
        or embedding_model_name == EmbeddingModelMaster.AZURE_TEXT_EMBEDDING_3_SMALL
    ) and ("azure_api_key" in config):
        return AzureOpenAIEmbeddings(
            api_key=config["azure_api_key"],
            model=embedding_model_name,
            azure_endpoint=config["azure_endpoint"],
            openai_api_version=config["openai_api_version"],
            azure_deployment=config["azure_deployment"],
        )

    elif (
        embedding_model_name == EmbeddingModelMaster.BEDROCK_TITAN_EMBEDDING
        or embedding_model_name
        == EmbeddingModelMaster.BEDROCK_TITAN_MULTIMODAL_EMBEDDING
    ) and ("bedrock_aws_session_token" in config):
        bedrock_client = boto3.client(
            service_name="bedrock-runtime",
            aws_access_key_id=config["bedrock_aws_access_key_id"],
            aws_secret_access_key=config["bedrock_aws_secret_access_key"],
            aws_session_token=config["bedrock_aws_session_token"],
            region_name=config["bedrock_region_name"],
        )

        return BedrockEmbeddings(
            credentials_profile_name="bedrock-admin",
            client=bedrock_client,
            model_id=embedding_model_name,
            region_name=config["bedrock_region_name"],
        )
        
    elif(
        embedding_model_name == EmbeddingModelMaster.GEMINI_EMBEDDING
    ) and ("google_api_key" in config):
        return GoogleGenerativeAIEmbeddings(
            model=EmbeddingModelMaster.GEMINI_EMBEDDING,
            google_api_key=config["google_api_key"],
        )
    else:
        raise ValueError(f"Unknown embedding model: {embedding_model_name}")
    
    

def get_inference_model(inference_model_name, config):
    if (
        inference_model_name == InferenceModelMaster.OPENAI_GPT_3_5_TURBO
        or inference_model_name == InferenceModelMaster.OPENAI_GPT_3_5_TURBO_INSTRUCT
        or inference_model_name == InferenceModelMaster.OPENAI_GPT_4
        or inference_model_name == InferenceModelMaster.OPENAI_GPT_4_TURBO_PREVIEW
    ) and ("api_key" in config):
        return ChatOpenAI(openai_api_key=config["api_key"], model=inference_model_name)
    elif (
        inference_model_name == InferenceModelMaster.OPENAI_GPT_3_5_TURBO
        or inference_model_name == InferenceModelMaster.OPENAI_GPT_3_5_TURBO_INSTRUCT
        or inference_model_name == InferenceModelMaster.OPENAI_GPT_4
        or inference_model_name == InferenceModelMaster.OPENAI_GPT_4_TURBO_PREVIEW
    ) and ("azure_api_key" in config):
        return AzureChatOpenAI(
            api_key=config["azure_api_key"],
            model=inference_model_name,
            deployment_name=config["azure_deployment"],
            azure_endpoint=config["azure_endpoint"],
            api_version=config["openai_api_version"],
            temperature=config["temperature"],
        )
    elif (
        inference_model_name == InferenceModelMaster.GROQ_LLM_MIXTRAL_8_7_B
        or inference_model_name == InferenceModelMaster.GROQ_LLM_LLAMA3_70B
        or inference_model_name == InferenceModelMaster.GROQ_LLM_GEMMA7B
    ) and ("groq_api_key" in config):
         return ChatGroq(groq_api_key=config["groq_api_key"], model=inference_model_name, temperature=config["temperature"])

    elif (
        inference_model_name == InferenceModelMaster.BEDROCK_TEXT_EXPRES_V1
        or inference_model_name == InferenceModelMaster.BEDROCK_TEXT_LITE_G1
    ) and ("bedrock_aws_session_token" in config):
        bedrock_client = boto3.client(
            service_name="bedrock-runtime",
            aws_access_key_id=config["bedrock_aws_access_key_id"],
            aws_secret_access_key=config["bedrock_aws_secret_access_key"],
            aws_session_token=config["bedrock_aws_session_token"],
            region_name=config["bedrock_region_name"]
        )
        return Bedrock(
            credentials_profile_name="bedrock-admin",
            model_id=inference_model_name,
            client=bedrock_client,
            region_name=config["bedrock_region_name"]
        )
    
    elif(
        inference_model_name == InferenceModelMaster.GOOGLE_GEMINI_PRO
        or inference_model_name == InferenceModelMaster.GOOGLE_GEMINI_1_5_PRO
    ) and ("google_api_key" in config):
        return ChatGoogleGenerativeAI(
            model=inference_model_name,
            google_api_key=config["google_api_key"],
            temperature=config["temperature"], 
            top_p=0.85,
            metadata= {'language': 'en'}
          

        )
    else:
        raise ValueError(f"Unknown inference model: {inference_model_name}")


def create_embeddings(data_sources, embedding_model, collection_name):

    store = get_vectorstore(embedding_model, collection_name)
    
    config_id = []
    for data_source in data_sources:
        config_id.append(uuid.uuid4())
        # data_source = {'name': 'PDF', 'config': {'files': ['path/to/file', 'path/to/file']}}
        for file_path in data_source.config["files"]:
            loader = get_loader(data_source.name, file_path, data_source.config)
            extra_metadata = [
                ("configId", str(config_id)),
            ]
            pages = loader.load_and_split()
            for page_content in pages:
                for key, value in extra_metadata:
                    page_content.metadata[key] = value
            
            # document.text = mask_data(document.text)
            result=RecursiveCharacterTextSplitter(
                 chunk_size=1000,
                 chunk_overlap=200,
                ).split_documents(pages)
            store.add_documents(result)
    # config_id is a list, due to possibility of multiple data_source.
    return {"message" : "embedding created" , "config_id" : config_id}


def get_vectorstore(embedding_model, collection_name):
    embeddings = get_embedding_model(embedding_model.name, embedding_model.config)
    store = PGVector(
        collection_name=collection_name,
        connection_string=SQLALCHEMY_DATABASE_URL,
        embedding_function=embeddings,
    )
    return store


async def async_chat(
    question,
    retriever,
    inference_model,
    embed_model,
    session_id,
    pipeline_id,
    trace_details=None,
    pii_filter_config = None,
    system_prompt=None,
    output_parser = None,
):
    chain_callbacks = []
    if trace_details is not None:
        langfuse_handler = CallbackHandler(
            secret_key=trace_details["secret_key"],
            public_key=trace_details["public_key"],
            host=trace_details["host"],
            trace_name=trace_details["identifier"],
        )
        chain_callbacks.append(langfuse_handler)

    history = TherixChatMessageHistory(
        str(session_id),
        str(pipeline_id),
        SQLALCHEMY_DATABASE_URL,
        table_name="chat_history",
    )
    message_history = history.get_message_history(str(session_id))
    chat_history=[]
    for message in message_history:
        chat_history.append(
            ChatMessage(role=message["message_role"], content=message["message"])
        )

    if(system_prompt):
        template = system_prompt.get("system_prompt")
    else :
        if(output_parser is not None): 
            template = """
            Answer the question based only on the following context:

            {context}

            Answer the question based on the above context: {question}
            The response should be a valid JSON format with the output_parser structure.
            """
        else:
            template = """
            Answer the question based only on the following context:

            {context}

            Answer the question based on the above context: {question}
            """

    ANSWER_PROMPT = ChatPromptTemplate.from_template(template)
    _template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language.
                    Chat History:
                    {chat_history}
                    Follow Up Input: {question}
                    Standalone question:"""

    CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)
    DEFAULT_DOCUMENT_PROMPT = PromptTemplate.from_template(template="{page_content} {source} {page}")
    
    model = get_inference_model(inference_model.name, inference_model.config)
    
    if pii_filter_config:
        pii_filter_config = pii_filter_config.config
        entities = pii_filter_config['entities']
        anonymizer = PresidioReversibleAnonymizer(
        analyzed_fields=entities,
        faker_seed=42)

        def _combine_documents(
            docs, document_prompt=DEFAULT_DOCUMENT_PROMPT, document_separator="\n\n"
        ):
            doc_strings = [format_document(doc, document_prompt) for doc in docs]
            return anonymizer.anonymize(document_separator.join(doc_strings))
        
        _inputs = RunnableParallel(
        standalone_question=RunnablePassthrough.assign(
            chat_history=lambda x: anonymizer.anonymize(get_buffer_string(x["chat_history"]))
        )
        | CONDENSE_QUESTION_PROMPT
        | model
        | StrOutputParser(),
        )
    else :
        def _combine_documents(
            docs, document_prompt=DEFAULT_DOCUMENT_PROMPT, document_separator="\n\n"
        ):
            doc_strings = [format_document(doc, document_prompt) for doc in docs]
            return document_separator.join(doc_strings)
            
        _inputs = RunnableParallel(
        standalone_question=RunnablePassthrough.assign(
            chat_history=lambda x: get_buffer_string(x["chat_history"])
        )
        | CONDENSE_QUESTION_PROMPT
        | model
        | StrOutputParser(),
        )
    
    _context = {
        "context": itemgetter("standalone_question") | retriever | _combine_documents,
        "question": lambda x: x["standalone_question"],
    }
        
    conversational_qa_chain = _inputs | _context | ANSWER_PROMPT | model
    
    if(trace_details and output_parser):
        result = conversational_qa_chain.invoke({"question": question, "chat_history": chat_history , "format_instructions" : output_parser.get_format_instructions()},config={"callbacks": [langfuse_handler]})
    elif(trace_details and not output_parser):
        result = conversational_qa_chain.invoke({"question": question, "chat_history": chat_history},config={"callbacks": [langfuse_handler]})
    elif(output_parser and not trace_details):
        result = conversational_qa_chain.invoke({"question": question, "chat_history": chat_history , "format_instructions" : output_parser.get_format_instructions()},config={"callbacks": [langfuse_handler]})
    else:   
        result = conversational_qa_chain.invoke(
            {"question": question, "chat_history": chat_history}
        )
    
    if inference_model.name == InferenceModelMaster.BEDROCK_TEXT_EXPRES_V1 or inference_model.name == InferenceModelMaster.BEDROCK_TEXT_LITE_G1 : 
        response = f'{result}'
    else :
        response = json.loads(result.json())["content"]

    if pii_filter_config:
        response = anonymizer.deanonymize(response)

    history.add_message("user",question,pipeline_id,session_id)
    history.add_message("system",response,pipeline_id,session_id)
    return response

def chat(
    question,
    retriever,
    inference_model,
    embed_model,
    session_id,
    pipeline_id,
    trace_details=None,
    pii_filter_config = None,
    system_prompt=None,
    output_parser = None
):
    
    chain_callbacks = []
    if trace_details is not None:
        langfuse_handler = CallbackHandler(
            secret_key=trace_details["secret_key"],
            public_key=trace_details["public_key"],
            host=trace_details["host"],
            trace_name=trace_details["identifier"],
        )
        chain_callbacks.append(langfuse_handler)

    history = TherixChatMessageHistory(
        str(session_id),
        str(pipeline_id),
        SQLALCHEMY_DATABASE_URL,
        table_name="chat_history",
    )
    message_history = history.get_message_history(str(session_id))
    chat_history=[]
    for message in message_history:
        chat_history.append(
            ChatMessage(role=message["message_role"], content=message["message"])
        )

    if(system_prompt):
        template = system_prompt.get("system_prompt")
    else :
        if(output_parser is not None): 
            template = """
            Answer the question based only on the following context:

            {context}

            Answer the question based on the above context: {question}
            The response should be a valid JSON format with the output_parser structure.
            """
        else:
            template = """
            Answer the question based only on the following context:

            {context}

            Answer the question based on the above context: {question}
            """

    ANSWER_PROMPT = ChatPromptTemplate.from_template(template)
    _template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language.
                    Chat History:
                    {chat_history}
                    Follow Up Input: {question}
                    Standalone question:"""

    CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)
    DEFAULT_DOCUMENT_PROMPT = PromptTemplate.from_template(template="{page_content} {source} {page}")
    
    model = get_inference_model(inference_model.name, inference_model.config)
    
    if pii_filter_config:
        pii_filter_config = pii_filter_config.config
        entities = pii_filter_config['entities']
        anonymizer = PresidioReversibleAnonymizer(
        analyzed_fields=entities,
        faker_seed=42)

        def _combine_documents(
            docs, document_prompt=DEFAULT_DOCUMENT_PROMPT, document_separator="\n\n"
        ):
            doc_strings = [format_document(doc, document_prompt) for doc in docs]
            return anonymizer.anonymize(document_separator.join(doc_strings))
        
        _inputs = RunnableParallel(
        standalone_question=RunnablePassthrough.assign(
            chat_history=lambda x: anonymizer.anonymize(get_buffer_string(x["chat_history"]))
        )
        | CONDENSE_QUESTION_PROMPT
        | model
        | StrOutputParser(),
        )
    else :
        def _combine_documents(
            docs, document_prompt=DEFAULT_DOCUMENT_PROMPT, document_separator="\n\n"
        ):
            doc_strings = [format_document(doc, document_prompt) for doc in docs]
            return document_separator.join(doc_strings)
            
        _inputs = RunnableParallel(
        standalone_question=RunnablePassthrough.assign(
            chat_history=lambda x: get_buffer_string(x["chat_history"])
        )
        | CONDENSE_QUESTION_PROMPT
        | model
        | StrOutputParser(),
        )
    
    _context = {
        "context": itemgetter("standalone_question") | retriever | _combine_documents,
        "question": lambda x: x["standalone_question"],
    }
        
    conversational_qa_chain = _inputs | _context | ANSWER_PROMPT | model
    
    if(trace_details and output_parser):
        result = conversational_qa_chain.invoke({"question": question, "chat_history": chat_history , "format_instructions" : output_parser.get_format_instructions()},config={"callbacks": [langfuse_handler]})
    elif(trace_details and not output_parser):
        result = conversational_qa_chain.invoke({"question": question, "chat_history": chat_history},config={"callbacks": [langfuse_handler]})
    elif(output_parser and not trace_details):
        result = conversational_qa_chain.invoke({"question": question, "chat_history": chat_history , "format_instructions" : output_parser.get_format_instructions()},config={"callbacks": [langfuse_handler]})
    else:   
        result = conversational_qa_chain.invoke(
            {"question": question, "chat_history": chat_history}
        )
    
    if inference_model.name == InferenceModelMaster.BEDROCK_TEXT_EXPRES_V1 or inference_model.name == InferenceModelMaster.BEDROCK_TEXT_LITE_G1 : 
        response = f'{result}'
    else :
        response = json.loads(result.json())["content"]

    if pii_filter_config:
        response = anonymizer.deanonymize(response)

    history.add_message("user",question,pipeline_id,session_id)
    history.add_message("system",response,pipeline_id,session_id)
    return response

