from enum import Enum
import json
from therix.core.chat_history.base_chat_history import TherixChatMessageHistory
from therix.core.constants import InferenceModelMaster
from therix.db.session import SQLALCHEMY_DATABASE_URL
from therix.utils.rag import get_inference_model
from langchain.chains.llm import LLMChain
from langchain_core.prompts import PromptTemplate
from langfuse.callback import CallbackHandler
from langchain_core.runnables import RunnableParallel
from langchain_core.runnables import RunnablePassthrough
from langchain_core.messages import get_buffer_string
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages.chat import ChatMessage


def invoke_default_chat(inference_model_details, session_id, pipeline_id, question, trace_details=None):
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
    
    inference_model_name = inference_model_details.name
    inference_model_config = inference_model_details.config
    model = get_inference_model(inference_model_name, inference_model_config)

    # Define a default prompt template
    prompt_template = "You are a helpful chatbot, you can use your own brain to provide answer to questions by users. The question is: {question}"
    
    _template = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language.
                    Chat History:
                    {chat_history}
                    Follow Up Input: {question}
                    Standalone question:"""
    
    CONDENSE_QUESTION_PROMPT = PromptTemplate.from_template(_template)
    ANSWER_PROMPT = ChatPromptTemplate.from_template(prompt_template)
    _inputs = RunnableParallel(
        standalone_question=RunnablePassthrough.assign(
            chat_history=lambda x: get_buffer_string(x["chat_history"])
        )
        | CONDENSE_QUESTION_PROMPT
        | model
        | StrOutputParser(),
        )

    _context = {
        "context": itemgetter("standalone_question"),
        "question": lambda x: x["standalone_question"],
    }

    conversational_qa_chain = _inputs | _context | ANSWER_PROMPT | model
    
    # Run the chain with the input text and return the response
    # response = prompt_chain.run(context=text, config={"callbacks": chain_callbacks})

    if(trace_details is not None):
        result = conversational_qa_chain.invoke({"question": question, "chat_history": chat_history},config={"callbacks": [langfuse_handler]})
    else:
        result = conversational_qa_chain.invoke({"question": question, "chat_history": chat_history})

    if inference_model_details.name == InferenceModelMaster.BEDROCK_TEXT_EXPRES_V1 or inference_model_details.name == InferenceModelMaster.BEDROCK_TEXT_LITE_G1 : 
        response = f'{result}'
    else :
        response = json.loads(result.json())["content"]
    
    history.add_message("user",question,pipeline_id,session_id)
    history.add_message("system",response,pipeline_id,session_id)
    return response