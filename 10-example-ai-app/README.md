# example-ai-app

The contents of this folder are based on <https://github.com/python-engineer/pytorch-chatbot>, released under the MIT License: Copyright (c) 2020 Patrick Loeber.

Modifications made by me (as listed below), shall also be licensed under the MIT License: Copyright (c) 2022 Henning 'haenno' Beier, haenno@web.de, <https://github.com/haenno/ai-api>

## Usage

1. Install Python and pipenv.
2. Install necessary packages by running ``pipenv install`` on the terminal in this folder.
3. Maybe add some topics, questions and answers to the ``intents.json`` file.
4. Then train the AI model with ``pipenv run python train.py``.
5. Finally chat with the AI chatbot by running ``pipenv run python chat.py``.
6. End the conversation by typing ``ende`` in the chatbot input.

## My changes and additions

- Added a logging: Chats, inputs and answers are logged. Also not understood inputs.
- For each chat a universally unique identifier (UUID4) is being generated and used for logging.
- Collected settings in a ``config.py``-file for easy tinkering with parameters.
- Created a Pipenv ``Pipfile`` with all the necessary dependencies.
