---
slug: /introduction/installation
sidebar_position: 10
---

# Installation & Setup

Therix is available to install via [pypi.org](https://pypi.org/) for use in any python project. 
If you need a custom solution get in touch at [enterprise@therix.ai](mailto:enterprise@therix.ai)


## Installation
To install Therix, you'll need to use a tool called `pip`, which helps manage software packages in Python. Open your command prompt or terminal, and type the following command exactly as shown:
`pip install therix` 


## Setup 
After installing, you can begin using `therix` by importing it into your Python scripts. Here’s how you can start with the `Pipeline` class:

```python
from therix.core.pipeline import Pipeline

# Initialize a new pipeline
pipeline = Pipeline(name="My New Published Pipeline")
(pipeline
    .add(// Add configurations you want to add)
    .save())

    pipeline.publish()
    answer = pipeline.invoke(text)
```

Use the `Pipeline` object to manage and execute various tasks within your project. For further details, follow the documentation precisely.

### Python Versions Supported

- **3.12**

### ENV Variables with meaning
- `THERIX_DB_HOST`: This variable specifies the host address where your Therix database is located.
- `THERIX_DB_PORT`: This variable defines the port number used to connect to your Therix database.
- `THERIX_DB_USERNAME`: This variable holds the username used to authenticate and access your Therix database. 
- `THERIX_DB_PASSWORD`: This variable stores the password required to authenticate and access your Therix database.
- `THERIX_DB_NAME`: This variable specifies the name of the Therix database you want to connect to.
- `THERIX_DB_TYPE`: This variable indicates the type of database system you're using


<!-- ### Optional ENV VARS

Cache, etc -->