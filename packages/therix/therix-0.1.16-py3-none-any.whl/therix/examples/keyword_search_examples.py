from therix.core.data_sources import PDFDataSource
from typing import List
from therix.core.embedding_models import AzureOpenAIEmbedding3LargeEmbeddingModel
from therix.core.inference_models import AzureOpenAIGPT4InferenceModel
from therix.core.output_parser import OutputParserWrapper
from therix.core.pipeline import Pipeline
import sys
from therix.core.trace import Trace
from pydantic import BaseModel, Field

if len(sys.argv) > 1:

    pipeline_group = Pipeline.merge([
        "pipeline_id1",
        "pipeline_id2",
    ])

    pipeline_group.set_primary("pipeline_id1")
    
    # question = sys.argv[2]

    pipeline_group.invoke("What is the summary of the data?")

    # pipeline = Pipeline.from_id(sys.argv[1])
    session_id = None

    # if len(sys.argv) < 4:
    #     pass
    # else:
    #     session_id = sys.argv[3]

    # ans = pipeline.invoke(question, session_id)
    # print(ans)
else:
    pipeline = Pipeline(name="My New Published Pipeline")
    (pipeline
    .add(PDFDataSource(config={'files': ['../../test-data/rat.pdf']}))
    .add(AzureOpenAIEmbedding3LargeEmbeddingModel(config={"azure_deployment" : "", "azure_api_key" : "" , "azure_endpoint" : "" , "openai_api_version" :  ""}))
    .add(AzureOpenAIGPT4InferenceModel(config={"azure_api_key" : "" , "openai_api_version" :  "", "azure_endpoint" : "" , "azure_deployment" : "" }))
    .add(Trace(config={
                    'secret_key': 'sk-lf-e62aa7ce-c4c8-4c77-ad7d-9d76dfd96db1',
                    'public_key': 'pk-lf-282ad728-c1d6-4247-b6cd-8022198591a9',
                    'identifier': 'keyword_search_pipeline'
         }))
        .save()
        )

    pipeline.publish()
    pipeline.preprocess_data()
    print(pipeline.id)

    class TestDetails(BaseModel):
        name: str = Field(description="Name of the Topic")
        description: str = Field(description="Short description of the Topic")
        citations: str = Field(description="add source of every topic, from where it is generated")
        page: str = Field(description="page number of the topic")


    class OutputParserJSON(BaseModel):
        tests: List[TestDetails] = Field(description="Topic")

    # mergerPipeline = Pipeline.merge(['ddd8c1a9-83b6-483d-ac68-cb6f98ccd987', '4d11a249-671f-45a2-bc0d-20922cbf4f4b'])

    # mergerPipeline.set_primary('ddd8c1a9-83b6-483d-ac68-cb6f98ccd987')

    # mergerPipeline.set_primary(pipeline.id)

    keyword_search_dict = {
        "prompt" : "Analyze the provided report content for all the documents provided and include only the sentences that matches {keywords} that is being provided separately and also add the keywords whose records are not found and add description as not found. Response should be a list of JSON  format.{format_instructions} Example: {{tests: [{{name: 'name of test', description: 'short description of Test'}}]}}",
        "keywords" : ["RAT" , "Gender"],
        "output_parser" : OutputParserWrapper.parse_output(pydantic_object=OutputParserJSON)
    }
    
    # ans = mergerPipeline.invoke("what is the meaning of RAT and gender in both the documents?")
    # ans = pipeline.invoke("what is the meaning of RAT and gender in both the documents?")
    ans = pipeline.invoke(keyword_search_params=keyword_search_dict)

    print(ans)

    
# ASYNCHRONOUS CALL - EXAMPLE
    # async def call_pipeline(keyword_search_dict):
    #     ans = await pipeline.async_invoke(keyword_search_params=keyword_search_dict)
    #     print(ans)
    #     return ans
    
    # asyncio.run(call_pipeline(keyword_search_dict))
    # print(ans)
