# SimplesAPI

**SimplesAPI** is a **Python-based application framework** designed to simplify the implementation of various functionalities such as database connections, structured logging, event dispatching, bucket access, and queue processing. By **reducing code repetition** and **enhancing code readability**, SimpleAPI allows developers to focus on solving business problems and rapidly create Proof of Concepts (POCs).

<p align="center">
  <img width="119" alt="image" src="https://github.com/oandersonmagalhaes/simplesapi/assets/83456692/7374e4f8-f9a8-4530-9e71-785e524e2b58">
</p>

## Features (WIP)
- Database Connections: Seamlessly connect to different types of databases with minimal configuration.
- Structured Logging: Implement structured and meaningful logs effortlessly.
- Event Dispatching: Send and handle events with ease.
- Bucket Access: Access and manage data stored in buckets.
- Queue Processing: Send messages to and retrieve messages from processing queues.
- Code Simplicity: Reduce boilerplate code to keep your codebase clean and maintainable.
- Rapid POC Development: Quickly develop and iterate on Proof of Concepts.

## Installation
To install SimplesAPI, simply run:

```bash
pip install simplesapi
```

# Getting Started

## Basic Setup
The main entry point of your application (main.py) should be set up as follows:

```python
from simplesapi.app import SimplesAPI
app = SimplesAPI(routes_path="routes")
```

## Folder Structure
SimpleAPI uses a folder structure to define routes. For example, to create a GET route for /users/{userId}, the folder structure should be:
```
routes/health-check__GET.py
routes/users/POST.py
routes/users/[userId]__GET.py
routes/users/DELETE.py
routes/users/PATCH.py
```

## Route Handler
Inside the route file ([userId]__GET.py), you should define an asynchronous handler function:
```python
async def handler(userId: str):
    return {"id": userId}
```

## Running
```
uvicorn main:app
```

## Contributing
We welcome contributions to SimpleAPI! Please read our contributing guidelines before submitting a pull request.

## License
SimpleAPI is licensed under the MIT License. See the LICENSE file for more details.

## Contact
For any questions or feedback, please contact in project Github.

By leveraging SimpleAPI, developers can streamline their application development process, focus on core business logic, and quickly bring their ideas to life.
