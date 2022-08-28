# prepared-ai-app

The contents of this folder are based on my changes (see folder '10-example-ai-app') of <https://github.com/python-engineer/pytorch-chatbot> from Patrick Loeber released under the MIT License.

In addition to the allready made changes, i here combined all functions in one single file, the ``chmod.py``. This file now contains a minimal working example of the ai application (a chatbot) for being called from Django or directly from shell with parameters.

## Usage

1. Install Python and pipenv.
2. Install necessary packages by running ``pipenv install`` on the terminal in this folder.
3. Maybe add some topics, questions and answers to the ``intents.json`` file.
4. Then call the help on parameters wirh  ``pipenv run python -m chatbot --help`` and follow the given instructions.
5. Hint: Dont forget to train the Chatot bevor talking to it with ``pipenv run python -m chatbot -t`

## My changes and additions

- Refactored the code to collect all functions in one file.
- Put every line of logic in functions, so that it can be called from a ``main()``-function.
- Added **'argparse'** for parsing arguments given from console calls of the script.
- Upgraded the logging.

## License

MIT License: Copyright (c) 2022 Henning 'haenno' Beier, haenno@web.de, <https://github.com/haenno/ai-api>
