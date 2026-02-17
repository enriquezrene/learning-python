# Working with Python
We use virtual envs, so follow these instructions:

## Enabling the virtual environment
```shell
source venv/bin/activate
```

## De-active the virtual env
```shell
(venv) $ deactivate
```

## Add dependencies
Once you have enabled the environment
```shell
(venv) $ python -m pip install <package-name>
```

## DB Migrations
The project uses alembic to manage migrations, make sure you run the following command to have the db up-to-date
```shell
alembic upgrade head
```