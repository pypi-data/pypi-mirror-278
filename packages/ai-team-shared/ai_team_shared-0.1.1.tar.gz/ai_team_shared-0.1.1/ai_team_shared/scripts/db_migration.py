from logging.config import fileConfig

from alembic import command
from alembic.config import Config
from alembic.script import ScriptDirectory


def run_migration(_cmd: str = "up") -> None:
    alembic_cfg = _config_alembic()
    if _cmd == "up":
        _upgrade_to_head(alembic_cfg)
    elif _cmd == "down":
        _downgrade_to_previous(alembic_cfg)
    else:
        raise ValueError("Invalid command. Please use 'up' or 'down'.")


def _config_alembic() -> Config:
    # Configure logging using the alembic.ini file
    fileConfig('alembic.ini', disable_existing_loggers=False)

    # This is the only config file in the codebase
    alembic_cfg = Config("alembic.ini")

    # Get the script directory to access metadata
    script_directory = ScriptDirectory.from_config(alembic_cfg)

    current_revision = script_directory.get_current_head()
    print(f"Current revision before upgrade: {current_revision}")
    return alembic_cfg


def _upgrade_to_head(alembic_cfg: Config) -> None:
    command.upgrade(alembic_cfg, "head")
    print("Upgraded to the latest revision (head)")


def _downgrade_to_previous(alembic_cfg: Config) -> None:
    command.downgrade(alembic_cfg, "head-1")
    print("Downgraded to the previous revision (head-1)")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        run_migration(cmd)
    else:
        run_migration()
