from enum import Enum
import json
from therix.utils.rag import get_inference_model
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chains import (
    MapReduceDocumentsChain,
    ReduceDocumentsChain,
)
from langchain_core.output_parsers import JsonOutputParser
from langfuse.callback import CallbackHandler

       
class SummarizerTypeMaster(Enum): 
    EXTRACTIVE = 'EXTRACTIVE'
    ABSTRACTIVE = 'ABSTRACTIVE'
        
PROMPT_TEMPLATE = {
    "EXTRACTIVE" : """
        Summarize the provided context below:

        {context}

        ---

        Craft your response with conciseness and accuracy, including only the information provided in the context. 
        Use null values for any missing information.

        Please structure your response in the following JSON format:
        {response_schema_json}
        """,
    "ABSTRACTIVE": "Provide a concise summary for the following text using abstractive summarization:\n\n{context}."
}
        
async def async_summarizer(summarizer_config,inference_model_details,text, trace_details, system_prompt=None):
  
    chain_callbacks = []
    if trace_details is not None:
        langfuse_handler = CallbackHandler(
            secret_key=trace_details["secret_key"],
            public_key=trace_details["public_key"],
            host=trace_details["host"],
            trace_name=trace_details["identifier"],
        )
        chain_callbacks.append(langfuse_handler)
        
    pydantic_prompt = summarizer_config['pydantic_model']
    summarization_type = summarizer_config['summarization_type']
    inference_model_name = inference_model_details.name
    inference_model_config = inference_model_details.config
    llm = get_inference_model(inference_model_name, inference_model_config)

    if(summarization_type == 'ABSTRACTIVE'):
        map_template = PromptTemplate.from_template(
            """Read the following document and
            provide a detailed summary of the document.
            {pages}"""
        )
        reduce_template = """The following is set of summaries:
        {pages}
        Take these and distill it into a final, consolidated summary.
        Verify each and every detail and make sure that the final
        summary is accurate and complete."""
        
        map_chain = LLMChain(llm=llm, prompt=map_template)
        reduce_prompt = PromptTemplate.from_template(reduce_template)

        # Run chain
        reduce_chain = LLMChain(llm=llm, prompt=reduce_prompt)

        # Takes a list of documents, combines them into a single string, and passes this to an LLMChain
        combine_documents_chain = StuffDocumentsChain(
            llm_chain=reduce_chain, document_variable_name="pages"
        )

        # Combines and iteratively reduces the mapped documents
        reduce_documents_chain = ReduceDocumentsChain(
            # This is final chain that is called.
            combine_documents_chain=combine_documents_chain,
            # If documents exceed context for `StuffDocumentsChain`
            collapse_documents_chain=combine_documents_chain,
            # The maximum number of tokens to group documents into.
            token_max=4000,
        )

        # Combining documents by mapping a chain over them, then combining results
        map_reduce_chain = MapReduceDocumentsChain(
            # Map chain
            llm_chain=map_chain,
            # Reduce chain
            reduce_documents_chain=reduce_documents_chain,
            # The variable name in the llm_chain to put the documents in
            document_variable_name="pages",
            # Return the results of the map steps in the output
            return_intermediate_steps=False,
        )

        docs = Document(page_content=text, metadata={"source": "local"})

        text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=1000, chunk_overlap=0
        )
        split_docs = text_splitter.split_documents([docs])

        # Run the chain
        summary = map_reduce_chain.run(split_docs)
    
    else:
        summary = text
    
    parser = JsonOutputParser()

    if(system_prompt and summarization_type=="EXTRACTIVE"):
        prompt = PromptTemplate(
            template=system_prompt.get("system_prompt"),
            input_variables=["context"],
            partial_variables={"response_schema_json": pydantic_prompt},
    )
    else: 
        prompt = PromptTemplate(
            template=PROMPT_TEMPLATE[summarization_type],
            input_variables=["context"],
            partial_variables={"response_schema_json": pydantic_prompt},
        )


    
    if summarization_type == SummarizerTypeMaster.EXTRACTIVE.value:
        chain = prompt | llm | parser
        if(trace_details):
            return json.dumps(chain.invoke({"context": summary},config={"callbacks": [langfuse_handler]}))
        else:
            return json.dumps(chain.invoke({"context": summary}))

    else:
        chain = prompt | llm
        if(trace_details):
            return  chain.invoke({"context": summary}, config={"callbacks": [langfuse_handler]}).content
        else:
            return  chain.invoke({"context": summary}).content
        

def summarizer(summarizer_config,inference_model_details,text, trace_details, system_prompt=None):
  
    chain_callbacks = []
    if trace_details is not None:
        langfuse_handler = CallbackHandler(
            secret_key=trace_details["secret_key"],
            public_key=trace_details["public_key"],
            host=trace_details["host"],
            trace_name=trace_details["identifier"],
        )
        chain_callbacks.append(langfuse_handler)
        
    pydantic_prompt = summarizer_config['pydantic_model']
    summarization_type = summarizer_config['summarization_type']
    inference_model_name = inference_model_details.name
    inference_model_config = inference_model_details.config
    llm = get_inference_model(inference_model_name, inference_model_config)

    if(summarization_type == 'ABSTRACTIVE'):
        map_template = PromptTemplate.from_template(
            """Read the following document and
            provide a detailed summary of the document.
            {pages}"""
        )
        reduce_template = """The following is set of summaries:
        {pages}
        Take these and distill it into a final, consolidated summary.
        Verify each and every detail and make sure that the final
        summary is accurate and complete."""
        
        map_chain = LLMChain(llm=llm, prompt=map_template)
        reduce_prompt = PromptTemplate.from_template(reduce_template)

        # Run chain
        reduce_chain = LLMChain(llm=llm, prompt=reduce_prompt)

        # Takes a list of documents, combines them into a single string, and passes this to an LLMChain
        combine_documents_chain = StuffDocumentsChain(
            llm_chain=reduce_chain, document_variable_name="pages"
        )

        # Combines and iteratively reduces the mapped documents
        reduce_documents_chain = ReduceDocumentsChain(
            # This is final chain that is called.
            combine_documents_chain=combine_documents_chain,
            # If documents exceed context for `StuffDocumentsChain`
            collapse_documents_chain=combine_documents_chain,
            # The maximum number of tokens to group documents into.
            token_max=4000,
        )

        # Combining documents by mapping a chain over them, then combining results
        map_reduce_chain = MapReduceDocumentsChain(
            # Map chain
            llm_chain=map_chain,
            # Reduce chain
            reduce_documents_chain=reduce_documents_chain,
            # The variable name in the llm_chain to put the documents in
            document_variable_name="pages",
            # Return the results of the map steps in the output
            return_intermediate_steps=False,
        )

        docs = Document(page_content=text, metadata={"source": "local"})

        text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=1000, chunk_overlap=0
        )
        split_docs = text_splitter.split_documents([docs])

        # Run the chain
        summary = map_reduce_chain.run(split_docs)
    
    else:
        summary = text
    
    parser = JsonOutputParser()

    if(system_prompt and summarization_type=="EXTRACTIVE"):
        prompt = PromptTemplate(
            template=system_prompt.get("system_prompt"),
            input_variables=["context"],
            partial_variables={"response_schema_json": pydantic_prompt},
    )
    else: 
        prompt = PromptTemplate(
            template=PROMPT_TEMPLATE[summarization_type],
            input_variables=["context"],
            partial_variables={"response_schema_json": pydantic_prompt},
        )


    
    if summarization_type == SummarizerTypeMaster.EXTRACTIVE.value:
        chain = prompt | llm | parser
        if(trace_details):
            return json.dumps(chain.invoke({"context": summary},config={"callbacks": [langfuse_handler]}))
        else:
            return json.dumps(chain.invoke({"context": summary}))

    else:
        chain = prompt | llm
        if(trace_details):
            return  chain.invoke({"context": summary}, config={"callbacks": [langfuse_handler]}).content
        else:
            return  chain.invoke({"context": summary}).content