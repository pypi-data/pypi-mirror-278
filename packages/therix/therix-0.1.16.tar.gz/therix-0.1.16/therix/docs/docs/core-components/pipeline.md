---
slug: /components/pipeline
sidebar_position: 1
---

# Pipeline

In therix, everything happens by creating pipelines of desired structure.

## What is a pipeline ?

A pipeline is a sequence of connected steps where a specific input undergoes various processes or transformations to achieve a desired outcome. Each step in the pipeline is dedicated to performing a specific task that contributes to the final result.

## How to create a pipeline ?

Import the Pipeline class and create an instance of a pipeline, name the pipeline with the desired name using its constructor.

```python
from therix.core.pipeline import Pipeline

# Initialize a new pipeline
pipeline = Pipeline(name="My New Published Pipeline")
```

Now you can add all the required configuration to your pipeline using the chaining method. Based on the components added the type of pipeline is determined implicitly.

## Add components to the pipeline

The newly created pipeline object acts as a starting point of adding the pipeline configurations. On this Instance you can add any required configuration component using the **.add()** method in a chain. So that the entire pipeline flow is decided.

```python
pipeline
        .add(PipelineConfiguration(config={ // Add required metadata  })) # Chaining add method to add configuration
```

## Save the pipeline

After you are done adding your desired configuration to your pipeline object its time to save our pipeline into the database. You can save your pipeline by chaining the **.save()** method at the end of the configuration chain.

```python
(pipeline
        .add(PipelineConfiguration(config={ // Add required metadata  }))
        .save() # Save method chained at the end for saving
        )
```

**Note : Once you save your pipeline, its configurations cannot be altered.**

## Publish your pipeline

Publishing the pipeline makes your pipeline ready to be used. You can simply publish your pipeline by calling the **.publish()** method on your pipeline object.

```python
pipeline.publish() # Call the publish method
```

## Preprocess the pipeline Data

Preprocessing the pipeline data is an optional step. If your pipeline configuration consists of an embedding model or has embedding creation requirements then only you need to preprocess the data. Otherwise you can skip it.
Preprocessing is done using the **.preprocess_data()** method on your pipeline object.

```python
pipeline.preprocess_data() # Add preprocessing method
```

## Invoke pipeline

The final step is invoking the pipeline for executing the pipeline according to the flow that we have configured with the help of pipeline configurations and its metadata added previously. This returns us the llm response into a dictionary with keys **answer** for the response and the **session_id** for the session.

Invocation is done using the **.invoke()** method on the pipeline object.

```python
answer = pipeline.invoke(// Your question) # Invoke the pipeline

#answer:
{'answer': // LLM response , 'session_id': // Uuid session id}
```

## Example

```python
pipeline = Pipeline(name="My New Published Pipeline")
    (
        pipeline
        .add(PipelineConfiguration(config={ // Add required metadata  })) // Add required configurations
        .save()
    )

    pipeline.publish()
    pipeline.preprocess_data()
    answer = pipeline.invoke(// Question to the llm)
```
In this way we have sucessfully created the pipeline, configured it and invoked it based on our requirements.