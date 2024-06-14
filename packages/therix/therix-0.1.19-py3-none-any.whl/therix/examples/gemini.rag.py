from therix.core.data_sources import PDFDataSource
from therix.core.embedding_models import (
    GeminiAIEmbeddings,
)
from therix.core.inference_models import (
    GeminiPro,
)

from therix.core.pipeline import Pipeline
import sys

from therix.core.trace import Trace

if len(sys.argv) > 1:
    pipeline = Pipeline.from_id(sys.argv[1])
    question = sys.argv[2]
    session_id = None

    if len(sys.argv) < 4:
        pass
    else:
        session_id = sys.argv[3]

    ans = pipeline.invoke(question, session_id)
    print(ans)
else:
    pipeline = Pipeline(name="My New Published Pipeline")
    (
        pipeline.add(PDFDataSource(config={"files": ["../../test-data/doc.pdf"]}))
        .add(GeminiAIEmbeddings(config={"google_api_key": ""}))
        .add(GeminiPro(config={"google_api_key": ""}))
        .add(
            Trace(
                config={
                    "secret_key": "sk-lf-e62aa7ce-c4c8-4c77-ad7d-9d76dfd96db1",
                    "public_key": "pk-lf-282ad728-c1d6-4247-b6cd-8022198591a9",
                    "identifier": "my own pipeline",
                }
            )
        )
        .save()
    )

    pipeline.publish()
    pipeline.preprocess_data()
    print(pipeline.id)
    ans = pipeline.invoke("what this document is about?")

    print(ans)
