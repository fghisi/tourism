import os
import importlib

from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool, MetaData

from alembic import context

from model import Base


config = context.config

fileConfig(config.config_file_name)


def combine_metadata(module_list):
    for module in module_list:
        m = MetaData()
        for t in load_class(module).metadata.tables.values():
            t.tometadata(m)
    return m


def load_class(module):
    return getattr(
        importlib.import_module(module), 
        'Base'
    )


def get_module_list():
    rootdir = os.getcwd()
    modules = []

    for dirname, subdirs, files in os.walk(rootdir):
        if (dirname.find('/model') >= 0 or dirname.find('\model') >= 0) \
                and (dirname.find('/__pycache__') < 0 or dirname.find('\__pycache__') < 0):

            for f in files:
                if not f.find('~') >= 0 and not f.find('__init__') >= 0 \
                        and not f.endswith('swp') and not f.endswith('pyc'):

                    modules = dirname.replace(os.getcwd(), '').split('/')
                    modules.pop(0)
                    module = '.'.join(modules)
                    module = "%s.%s" % (module, f.replace('.py', ''))

                    if module not in modules:
                        modules.append(module)
    return modules

module_list = get_module_list()
target_metadata = combine_metadata(module_list)


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


run_migrations_online()
