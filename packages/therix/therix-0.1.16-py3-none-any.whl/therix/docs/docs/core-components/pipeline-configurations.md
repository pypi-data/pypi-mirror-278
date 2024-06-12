---
slug: /components/pipeline-configurations
sidebar_position: 5
---

# Pipeline Configurations

Adding pipeline configurations is the most important part of working with therix. It decides the entire flow of the pipeline and determines the output. Based on the configuration added, therix itself identifies the type of pipeline you want to create.

Pipeline configurations which determine the pipeline type cannot be used with other clashing pipeline configurations. Therix wont let you add clashing configurations and will throw an exception if you try to do so. 

An example of which is an embedding model and a summarizer configuration cannot be added together as for the summarizer configuration we do not need embeddings as it accepts plain text.

```python
pipeline = Pipeline(name="My New Published Pipeline")
    (
        pipeline
        .add(EmbeddingModel(config={ // Embedding model config}))
        .add(SummarizerConfig(config={ // Summarizer config }))
    )

# throws an exception 
Exception : Cannot add SUMMARIZER.
```

As we have added embedding model first, therix determines the type as **RAG** and then when we add summarizer config it tries to overwrite the type by **SUMMARIZER** and hence throws an exception.

## Conflicting configurations

As of now therix only has one conflicting configuration.

- Embedding Model and Summarizer Configuration.
