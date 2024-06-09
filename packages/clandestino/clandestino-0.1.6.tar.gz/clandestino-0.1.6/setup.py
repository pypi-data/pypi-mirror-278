# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['clandestino', 'clandestino.src']

package_data = \
{'': ['*']}

install_requires = \
['clandestino-interfaces>=0.1.1,<0.2.0', 'python-decouple>=3.8,<4.0']

extras_require = \
{'elasticsearch': ['clandestino_elasticsearch>=0.1.1,<0.2.0'],
 'mongo': ['clandestino_mongo>=0.1.1,<0.2.0'],
 'postgres': ['clandestino_postgres>=0.1.1,<0.2.0'],
 'sqlite': ['clandestino_sqlite>=0.1.1,<0.2.0']}

entry_points = \
{'console_scripts': ['cdt = clandestino.clandestino:main']}

setup_kwargs = {
    'name': 'clandestino',
    'version': '0.1.6',
    'description': 'Simple migration tool for your python project',
    'long_description': '# Clandestino\n\n![banner](docs/banner.jpeg)\n\n```\nBy: CenturyBoys\n```\n\nThis package provides a migration tool. It includes a command-line interface (CLI) for easy execution and a single asynchronous function that can be imported and used in your code.\n\n## Install\n\nThe main package does not have any database implementation and uses only the interfaces and abstractions from the `clandestino_interfaces` package. In other words, you are free to create your own implementations. We will explain the details later.\n\n| Database Type | Install using extra | description                            | Environment parameter                       |\n|---------------|---------------------|----------------------------------------|---------------------------------------------|\n| PostgreSQL    | postgres            | [here](extras/postgres/README.md)      | CLANDESTINO_POSTGRES_CONNECTION_STRING      |\n| Elasticsearch | elasticsearch       | [here](extras/elasticsearch/README.md) | CLANDESTINO_ELASTICSEARCH_CONNECTION_STRING |\n| MongoDB       | mongo               | [here](extras/mongo/README.md)         | CLANDESTINO_MONGO_CONNECTION_STRING         |\n| SQLite        | sqlite              | [here](extras/sqlite/README.md)        | CLANDESTINO_SQLITE_DB_PATH                  |\n\nHow to install extra packages?\n\n```shell\npoetry add clandestino -E postgres\nOR\npip install \'clandestino[postgres]\'\n```\n\n## Config\n\nClandestino has some configurations that you can set as environment variables or in a `.env` file.\n\n- `CLANDESTINO_MIGRATION_REPO` If you are using any of the extra packages, you must set them with their respective values: `POSTGRES`, `ELASTICSEARCH`, `MONGO`, `SQLITE`\n\n## CLI\n\n### [-h] Help command\n\n```bash\n$cdt -h         \n Clandestino is a database migration tool\n Migration repository mode is: ELASTICSEARCH\n  cldest [-h|-m|-lm|-rm|-cm] [params]\n\n    -h: Display help\n    -m: Migrate database\n    -lm: List migrations\n    -rm: Rollback last migration\n    -cm: Create database migration - params [name type]\n```\n\n### [-m] Migrate database\n\nMigrate databases using the files within the `./migrations` folder. Each migration checks if it\'s already run. If not, the migration is applied, the information is saved, and the async def up(self) -> None method is called. No migration will be executed twice.\n\nThe system will display the migration status:\n- OK = ✅\n- ERROR = ⚠️\n- SKIPPED = ⏭️\n\n### [-lm] List migrations\n\nList all migration within the `./migrations` folder\n\n### [-rm] Rollback migration\n\nRollback the last database migration using the latest file in the `./migrations` folder. The `async def down(self) -> None` method within the file will be called.\n\nThe system will display the rollback status:\n- OK = ✅\n- ERROR = ⚠️\n- SKIPPED = ⏭️\n\n### [-cm] Create migration\n\nCreate a migration within the `./migrations` folder, if the folder not exists create it to. \n\nThis command receive two parameters:\n\n- Migration name \n- Migration type, if not filled will use default migration template.\n\nThe migration file will be like this `migration_{datetime_reference}_{migration_name}.py`\n\n## Migration file\n\nThe migration file inherit the abstract class `AbstractMigration` and need declare two fundtions:\n\n- `async def up(self) -> None`. This method will be called on migration command\n- `async def down(self) -> None`. This method will be called on rollback command\n\nSee bellow an empty template file\n\n```python\nfrom clandestino_interfaces import AbstractMigration\n\nclass Migration(AbstractMigration):\n\n    infra = None\n\n    async def up(self) -> None:\n        """Do modifications in database"""\n        pass\n\n    async def down(self) -> None:\n        """Undo modifications in database"""\n        pass\n```\n\n## Self Implementation\n\nTo create your own Clandestino implementation, simply create a file named `repository.py` inside the `./migrations` folder. This file should contain a class named `MigrateRepository` that inherits from `clandestino_interfaces.IMigrateRepository`.\n\nObservation: Your migrations need to handler the database connections by your self.\n\nSee bellow the interface:\n\n```python\nfrom abc import ABC, abstractmethod\n\nclass IMigrateRepository(ABC):\n    @classmethod\n    @abstractmethod\n    async def create_control_table(cls) -> None:\n        pass\n\n    @classmethod\n    @abstractmethod\n    async def control_table_exists(cls) -> bool:\n        pass\n\n    @classmethod\n    @abstractmethod\n    async def register_migration_execution(cls, migration_name: str) -> None:\n        pass\n\n    @classmethod\n    @abstractmethod\n    async def migration_already_executed(cls, migration_name: str) -> bool:\n        pass\n\n    @classmethod\n    @abstractmethod\n    async def remove_migration_execution(cls, migration_name: str) -> None:\n        pass\n```',
    'author': 'XimitGaia',
    'author_email': 'im.ximit@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
