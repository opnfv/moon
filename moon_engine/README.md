# moon_engine

## Installation

If you want a stable version:

```bash
sudo python -m pip install moon_engine
```

If you want a development version:

```bash
ARTIFACTORY=https://artifactory-iva.si.francetelecom.fr/artifactory/api/pypi/python-virt-orange-product-devops/simple
sudo python -m pip install --pre moon_engine -i $ARTIFACTORY
```
Use it at your own risk, this is an unstable version.

If you want to be in development mode, and get the code:

```bash
git clone git@gitlab.forge.orange-labs.fr:moon/moon_utilities.git
cd moon_utilities
sudo pip install -e .
cd ..
git clone git@gitlab.forge.orange-labs.fr:moon/moon_cache.git
cd moon_cache
sudo pip install -e .
cd ..
git clone git@gitlab.forge.orange-labs.fr:moon/moon_engine.git
cd moon_engine
sudo pip install -e .
```

## Configuration

You need to create 3 configuration files.

### config.cfg::

    # configuration for Gunicorn
    bind = "127.0.0.1:8081"
    workers = 2
    
    # configuration for moon_engine
    moon = "moon.yaml"


### moon.yaml (feel free to update the configuration file to your need...)::


    type: "pipeline"
    uuid:
    manager_url: ""
    incremental_updates: false
    api_token:
    data: policy.json
    debug: true
    
    management:
      password: admin
      url: http://127.0.0.1:8000
      user: admin
      token_file: moon_engine_users.json
    
    orchestration:
      driver: moon_engine.plugins.pyorchestrator
      connection: local
      port: 20000...20100
      config_dir: /tmp
    
    authorization:
      driver: moon_engine.plugins.authz
    
    plugins:
      directory: /tmp
    
    logging:
      version: 1
    
      formatters:
        brief:
          format: "%(levelname)s %(name)s %(message)-30s"
        custom:
          format: "%(asctime)-15s %(levelname)s %(name)s %(message)s"
    
      handlers:
        console:
          class : logging.StreamHandler
          formatter: custom
          level   : INFO
          stream  : ext://sys.stdout
        file:
          class : logging.handlers.RotatingFileHandler
          formatter: custom
          level   : DEBUG
          filename: /tmp/moon_engine.log
          maxBytes: 1048576
          backupCount: 3
    
      loggers:
        moon:
          level: DEBUG
          handlers: [console, file]
          propagate: no
    
      root:
        level: ERROR
        handlers: [console]

### policy.json

This file contains all data that will be imported in the Engine. As we cannot update the cache after the creation of the Engine, all data must be in this file.
Example files lie in the conf directory.

## Web server execution

Execution when library is installed:

For a development server:

```bash
hug -m moon_engine.server config.cfg
```

For a production server:

```bash
gunicorn moon_engine.server:__hug_wsgi__ -c config.cfg
```

or

```bash
moon_engine start config.cfg
```

If library is not installed:

```bash
gunicorn moon_engine/server:__hug_wsgi__ -c config.cfg
```

This will install an autonomous engine server.
If you need to connect to a Manager, you must update the `moon.yaml` accordingly.

