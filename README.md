# Experiments with OpenAI, CamFort and Fortran source code

## Installation requirements

- `pip install -r requirements.txt`

## Docker alternative

- `./build.sh` generates image `openai:python3.10` locally from `Dockerfile.openai-python`
- `./run.sh [...]` runs command `[...]` within the Docker container.

## Getting an OpenAI API key

Sign up at <https://openai.com/api/>. You should automatically receive
US$18 in credit valid for 3 months (as of this writing), which should
be sufficient for testing. You can find your API key here:
<https://beta.openai.com/account/api-keys>.

The key is a long string beginning with `sk-`. Put the OpenAI API key
into the env var `OPENAPI_API_KEY` or provide it using the `--api-key`
option to scripts.

## Function / subroutine search

### Compiling a database of vectors

Script `get_vectors.py` can be used to form a (sqlite3) database
keeping information about functions and subroutines in Fortran files
for later look-up.

It expects JSON describing function/subroutine locations in a certain
format either on stdin or given in a file via option `-f`. Each line
in the file looks like this:

`{"name": "function_name", "path": "path/to/fortran/file.f90", "firstLine": 10, "lastLine": 25}`

#### Example runs

- `fortran-src --dump-funs-and-subs src/ | ./run.sh python get_vectors.py --api-key "sk-..."`
- `fortran-src --dump-funs-and-subs file.f90 | ./run.sh python get_vectors.py --database mydatabase.db --api-key "sk-..."`

### Searching the database

Script `search_vectors.py` can be used to query the (sqlite3) database
using a general free-text search query to find the functions or
subroutines that most closely match the description.

#### Example runs

- `./run.sh python search_vectors.py --api-key "sk-..." --database mydatabase.db calculate wet-bulb temperatures`
- `./run.sh python search_vectors.py -n 10 precipitation in clouds`

## OpenAI transcripts and finetuning

This section discusses the code and examples found in the
`openai-transcripts` subdirectory.

### Interactive OpenAI

OpenAI can be used interactively
<https://beta.openai.com/playground>. Typical settings include:

- model: text-davinci-003 (most powerful) or code-davinci-002 (programming oriented).
- temperature: 0, for the most deterministic output
- maximum length: adjust as needed for longer output sequences (256 is not a bad start)
- stop sequence: I often create one to stop the AI from going on and on. I use either `!=end` or `"""`, lately.

File `units-transcript1.txt` contains a sample transcript from a
session of teaching OpenAI about units. In between text explanations
are series of examples. Usually, the final example in each series is a
result of prompting the AI to fill in the 'output' automatically. Then
after having built up some knowledge, I move on to the next concept.

It is possible to provide a series of prompt/completion data entries
to 'finetune' the OpenAI model. Such finetuned models will appear in
the list of models in the playground, or can be invoked from the
programmatic API.

### Converting to JSONL

The input to finetuning requires the [JSONL](https://jsonlines.org/)
format, which is just a series of lines in a text file, each line
containing an independent JSON object. A sample script has been
provided to convert from a simple text format to JSONL.

`python3 txt-to-jsonl.py < finetune-examples.txt > finetune.jsonl`

The expected text input is a bit verbose and is adapted from the units transcript, it looks like this:

	Input: """
	<partially completed code>
	"""
	Output: """
	<fully completed code>
	"""
	###
	[...]

The output:

	{"prompt": "<partially completed code">, "completion": "<fully completed code>"}
	[...]

### Running the finetune process

Install the `openai` pip package and ensure your `OPENAI_API_KEY` env
var is set with your key, then you can invoke the functionality for
finetuning like so:

	openai api fine_tunes.create -t openai-transcripts/finetune.jsonl -m davinci

This will put you on the queue (and eventually charge your account
based on the number of tokens; it will tell you first before charging
so you can cancel if you like).


### Running the model

The generated finetune model will then be available in the playground
or on the command line (with `OPENAI_API_KEY` env var set):

	openai api completions.create -m davinci:ft-personal-xx-yy-zz -p '<partially completed code for the query>'

where `davinci:ft-personal-xx-yy-zz` is the name of the created model.
