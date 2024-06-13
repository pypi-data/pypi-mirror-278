from therix.core.data_sources import PDFDataSource
from therix.core.inference_models import BedrockLiteG1, BedrockTextExpressV1, GroqMixtral87bInferenceModel
from therix.core.embedding_models import BedrockTitanEmbedding
from therix.core.pii_filter_config import PIIFilterConfig
from therix.core.pipeline import Pipeline
import sys
from therix.core.trace import Trace



# TODO: Init therix with DB details, and license key


## Usage:
# python main.py ad11128d-d2ec-4f7c-8d87-15c1a5dfe1a9 "how does it help in reasoning?"

# if args has pipeline_id, then load the pipeline
## else create new pipeline
if len(sys.argv) > 1:
    pipeline = Pipeline.from_id(sys.argv[1])
    question = sys.argv[2]
    ans = pipeline.invoke(question)
    print(ans)
else:
    pipeline = Pipeline(name="My New Published Pipeline")
    (pipeline
    .add(PDFDataSource(config={'files': ['../../test-data/Essay-on-Lata-Mangeshkar-final.pdf']}))
    .add(BedrockTitanEmbedding(config={ "bedrock_aws_access_key_id":"",
                                        "bedrock_aws_secret_access_key" : "",
                                        "bedrock_aws_session_token" : "",
                                        "bedrock_region_name" : "us-east-1"
                                            }))
    .add(BedrockLiteG1(config={ "bedrock_aws_access_key_id":"",
                                "bedrock_aws_secret_access_key" : "",
                                "bedrock_aws_session_token" : "",
                                "bedrock_region_name" : "us-east-1"
                                            }))
    .add(PIIFilterConfig(config={
        'entities': ['PERSON','PHONE_NUMBER','EMAIL_ADDRESS']
    }))
    .add(Trace(config={
        'secret_key': 'sk-lf-6fd11f23-6506-428c-9328-6a03cce5574b',
        'public_key': 'pk-lf-d319ad68-34e1-45e5-b25c-c341e8f22462',
        'identifier': 'pii_filter_pipeline'
    }))
    .save())

    pipeline.publish()
    pipeline.preprocess_data()
    print(pipeline.id)
    ans = pipeline.invoke("Whom is the data about? And what are their personal details?")

    print(ans)