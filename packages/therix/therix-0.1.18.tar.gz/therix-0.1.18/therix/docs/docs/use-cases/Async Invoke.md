---
slug: /use-cases/asynchronous-methods
sidebar_position: 3
---

# Async Invoke

Therix also includes a feature for invoking the pipeline asynchronously. This means you can trigger multiple pipelines at the same time without any one of them slowing down the others.

# Syntax

Keeping it simple, just add `async_` before the `invoke` method, making it `async_invoke`.

# Example

We are using `asyncio` to make asynchronous calls, you can use any other desired library.

```python
import asyncio

pipeline = Pipeline(name="My New Published Pipeline")
    (
        pipeline
        .add(PipelineConfiguration(config={ // Add required metadata  })) // Add required configurations
        .save()
    )

    pipeline.publish()
    pipeline.preprocess_data()

     async def call_pipeline(text):
        ans = await pipeline.async_invoke(text)
        print(ans)
        return ans

    asyncio.run(call_pipeline("your question"))
```