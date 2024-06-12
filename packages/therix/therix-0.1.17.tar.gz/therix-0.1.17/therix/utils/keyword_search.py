from re import I
from langchain.prompts.chat import ChatPromptTemplate
from langchain_community.vectorstores.pgvector import PGVector
from therix.utils.rag import get_inference_model
from langfuse.callback import CallbackHandler
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List

DEFAULT_PROMPT = """
        You are a skilled professional who understands All kinds of documents. 
        You will be provided with Content and keywords.
        You have Analyze given data.
        {{content}}
        {{keywords}}
        Response should be in valid JSON format.

"""

BASIC_INSTRUCTIONS = """
If a question seems confusing, simply rephrase it using simpler words. Examples can help too.
When unsure of the user's intent, rephrase the question and ask for confirmation.
Only answer questions related to your knowledge base.
Avoid asking the user questions unrelated to their current request.
Strive for factual answers. If unsure, acknowledge it and offer to find more information.
Always be polite and inclusive in your communication.
Be open to improvement based on user interactions and feedback.
"""


def async_keyword_search(keyword_search_dict):
        chain_callbacks = []

        retriever = keyword_search_dict["retriever"]
        inference_model = keyword_search_dict["inference_model"]
         
        if keyword_search_dict.get("trace_details") is not None:
            langfuse_handler = CallbackHandler(
            secret_key=keyword_search_dict.get("trace_details")["secret_key"],
            public_key=keyword_search_dict.get("trace_details")["public_key"],
            host=keyword_search_dict.get("trace_details")["host"],
            trace_name=keyword_search_dict.get("trace_details")["identifier"],
        )

        content = ""  
        for keyword in keyword_search_dict["keywords"]:
            results = retriever.get_relevant_documents(keyword)
    
            for res in results:
                content += res.page_content + str(res.metadata) + "\n\n---\n\n"
        content = content.rstrip("\n\n---\n\n")

        prompt = keyword_search_dict["prompt"]

        if not prompt:
            prompt = DEFAULT_PROMPT.format(content, keyword_search_dict["keywords"])

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", prompt),
                ("human",
                 "{BASIC_INSTRUCTIONS} {content} {keywords}")
            ]
        )

        model = get_inference_model(inference_model.name, inference_model.config)
        
        chain = prompt | model | keyword_search_dict["output_parser"]
        if(keyword_search_dict.get("trace_details")):
            response_text = chain.invoke({"content": content, "keywords": keyword_search_dict["keywords"], "format_instructions": keyword_search_dict["output_parser"].get_format_instructions(), "BASIC_INSTRUCTIONS": BASIC_INSTRUCTIONS}, config={"callbacks": [langfuse_handler]})
        else: 
            response_text = chain.invoke({"content": content, "keywords": keyword_search_dict["keywords"], "format_instructions": keyword_search_dict["output_parser"].get_format_instructions(), "BASIC_INSTRUCTIONS": BASIC_INSTRUCTIONS})
        
        return response_text

def keyword_search(keyword_search_dict):
        chain_callbacks = []

        retriever = keyword_search_dict["retriever"]
        inference_model = keyword_search_dict["inference_model"]
         
        if keyword_search_dict.get("trace_details") is not None:
            langfuse_handler = CallbackHandler(
            secret_key=keyword_search_dict.get("trace_details")["secret_key"],
            public_key=keyword_search_dict.get("trace_details")["public_key"],
            host=keyword_search_dict.get("trace_details")["host"],
            trace_name=keyword_search_dict.get("trace_details")["identifier"],
        )

        content = ""  
        for keyword in keyword_search_dict["keywords"]:
            results = retriever.get_relevant_documents(keyword)
    
            for res in results:
                content += res.page_content + str(res.metadata) + "\n\n---\n\n"
        content = content.rstrip("\n\n---\n\n")

        prompt = keyword_search_dict["prompt"]

        if not prompt:
            prompt = DEFAULT_PROMPT.format(content, keyword_search_dict["keywords"])

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", prompt),
                ("human",
                 "{BASIC_INSTRUCTIONS} {content} {keywords}")
            ]
        )

        model = get_inference_model(inference_model.name, inference_model.config)
        
        chain = prompt | model | keyword_search_dict["output_parser"]
        if(keyword_search_dict.get("trace_details")):
            response_text = chain.invoke({"content": content, "keywords": keyword_search_dict["keywords"], "format_instructions": keyword_search_dict["output_parser"].get_format_instructions(), "BASIC_INSTRUCTIONS": BASIC_INSTRUCTIONS}, config={"callbacks": [langfuse_handler]})
        else: 
            response_text = chain.invoke({"content": content, "keywords": keyword_search_dict["keywords"], "format_instructions": keyword_search_dict["output_parser"].get_format_instructions(), "BASIC_INSTRUCTIONS": BASIC_INSTRUCTIONS})
        
        return response_text
    
    