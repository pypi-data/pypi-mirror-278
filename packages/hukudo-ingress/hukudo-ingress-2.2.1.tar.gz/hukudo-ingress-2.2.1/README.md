# Ingress
Configure Caddy as an ingress for your Docker containers.

See https://gitlab.com/hukudo/ingress for example usage.

## Usage
```
pip install hukudo-ingress==2.2.1
ingress --help
```

## Development
Initial
```
make dev-setup
ingress --help
```

[Completion](https://click.palletsprojects.com/en/8.1.x/shell-completion/)
```
eval "$(_INGRESS_COMPLETE=bash_source ingress)"
```


## Debugging
```
LOGLEVEL=info ingress render
LOGLEVEL=info ingress reconfigure
```
