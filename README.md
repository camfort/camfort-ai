# Experiments with OpenAI, CamFort and Fortran source code

## Installation requirements

- `pip install -r requirements.txt`

## Docker

- `./build.sh` generates image `openai:python3.10` locally from `Dockerfile.openai-python`
- `./run.sh [...]` runs command `[...]` within the Docker container.

## Function / subroutine search

### Compiling a database of vectors

Script `get_vectors.py` can be used to form a (sqlite3) database
keeping information about functions and subroutines in Fortran files
for later look-up.

It expects JSON describing function/subroutine locations in a certain
format either on stdin or given in a file via option `-f`. Each line
in the file looks like this:

`{"name": "function_name", "path": "path/to/fortran/file.f90", "firstLine": 10, "lastLine": 25}`

Put your OpenAPI key into the env var `OPENAPI_API_KEY` or provide it using the `--api-key` option.

#### Example runs

- `fortran-src --dump-funs-and-subs src/ | ./run.sh python get_vectors.py --api-key "sk-..."`
- `fortran-src --dump-funs-and-subs file.f90 | ./run.sh python get_vectors.py --database mydatabase.db --api-key "sk-..."`
