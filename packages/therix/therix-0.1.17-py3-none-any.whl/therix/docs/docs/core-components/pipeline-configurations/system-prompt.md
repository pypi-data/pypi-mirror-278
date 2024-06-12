---
slug: /components/pipeline-config/system-prompt
sidebar_position: 1
---

# System Prompt
System prompt is a way of adding custom prompt to your language models that override the existing prompt provided by Therix.


## Why Custom System-Prompt
A personalized system prompt allows you to direct your language model's behavior. This means you can tailor the model to suit your preferences, whether you need it to act like a teacher, a doctor, or anything else.

## Example of System-Prompt
Keep in mind to use the same placeholders for `{context}` and `{question}`

    ```Python
    sys_prompt =  
        """
        You are an AI chatbot who behaves as a doctor.
        Answer the question based only on the following context.
        Always prescribe according to the context provided
        Do not reply if you are not sure.
        Context: 
        {context}

        Question: {question}
        """
    ```

## Add System-Prompt to your pipeline
You can add system-prompt to your pipeline by doing a `.add` to your existing configurations.
```python
.add(SystemPromptConfig(config={"system_prompt" : sys_prompt}))
```

# Example
```python
from therix.core.system_prompt_config import SystemPromptConfig

pipeline = Pipeline(name="Summarizer Pipeline")
    (pipeline
    .add(SystemPromptConfig(config={"system_prompt" : sys_prompt}))
    .add(// Any other configuration you want to add)
    .save())

    pipeline.publish()
    answer = pipeline.invoke(text)
```



## How to pass dynamic system prompt


You can also pass a dynamic system prompt while invoking already created pipeline, by just adding a parameter to pipeline.invoke method


**Example**

```python

#just define a dynamic system prompt if you don't want to use already added system prompt or don.t want to add a system prompt to your pipeline


dynamic_system_prompt = """
        You are a an eXpert in summarizing documents
        Summarize the provided context below as an expert:
        {context}

        ---

        Craft your response with conciseness and accuracy, including only the information provided in the context. 
        Use null values for any missing information.

        Please structure your response in the following JSON format:
        {response_schema_json}
        """


#And instead of adding this system prompt to the pipeline configuration we can directly pass it to our invoke method 


pipeline = Pipeline(name="Summarizer Pipeline")
    (pipeline
    .add(SummarizerConfig(SummarizerTypeMaster.EXTRACTIVE,TopicModel))
    .add(// Any other configuration you want to add)
    .save())

    pipeline.publish()
    ans = pipeline.invoke(question = text, dynamic_system_prompt=dynamic_system_prompt )
    print(ans)