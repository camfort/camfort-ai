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
