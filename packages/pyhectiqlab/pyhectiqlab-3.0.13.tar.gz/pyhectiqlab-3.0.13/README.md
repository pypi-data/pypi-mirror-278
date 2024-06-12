# pyhectiqlab

- [Documentation](https://docs.hectiq.ai)

- [Web app](http://lab.hectiq.ai)

## Installation

```bash
pip install pyhectiqlab
```

## List of environment variables

- `HECTIQLAB_PROJECT`: Name of the current Hectiq Lab project.
- `HECTIQLAB_CONFIGS`: Path to the `configs.toml` file. By default, this is in `~/.hectiq-lab`.
- `HECTIQLAB_CREDENTIALS`: Path to the `credentials.toml` file. By default, this is in `~/.hectiq-lab`.
- `HECTIQLAB_ALLOW_DIRTY`: Whether to allow for a dirty state of the repo's project.
- `HECTIQLAB_API_KEY`: API key, this should be set via the CLI function `authenticate`.
- `HECTIQLAB_API_URL`: URL of the API `https://api.lab.hectiq.ai`, this should not be modified.
- `HECTIQLAB_REPOS`: List of repo versions to monitor.
- `HECTIQLAB_MODELS_DOWNLOAD`: Default path where to download models.
- `HECTIQLAB_DATASETS_DOWNLOAD`: Default path where to download datasets.
