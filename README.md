# workflows
workflow definitions via argo-workflow


## TODO TBD
unsure where to keep the manifests, but for ease of local development it probably makes sense to keep them here in some form

for now this repo is a python project, but if additional workflow languages are ever required, more thought will need to be put into the structure of this project

going to use typer for CLI
single entrypoint for now
strutcture TBD. multi app is possible but need to setup


## setup
uv for project management

creat venv `uv venv`. creates folder `.venv`
activate venv `source .venv/bin/activate` and setup IDE to use this venv
run `uv sync` to install

now you can run a command
```
uvx run twitch-to-slack
```
or
```
uvx run other-workflow
```


### dev setup
additional steps for dev setup

install pre-commit as uv tool
```
uv tool install pre-commit
```

init pre-commit hook
```
uvx pre-commit install
```


then you can run pre-commit manually with
```
uvx pre-commit
```

### commands

helm dry run
```
helm install --dry-run workflows charts/workflow-templates/
```
