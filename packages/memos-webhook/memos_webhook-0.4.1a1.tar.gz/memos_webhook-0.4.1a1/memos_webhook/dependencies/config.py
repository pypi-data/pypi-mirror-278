from pydantic import BaseModel

from memos_webhook.utils.config_decorators import (ArgsConfigProvider,
                                                   BaseArgsConfig,
                                                   BaseDotenvConfig,
                                                   BaseUnmarshalConfig,
                                                   default, from_env,
                                                   from_unmarshal, it_is)


class YouGetPluginConfig(BaseModel):
    name: str
    tag: str
    patterns: list[str]


class PluginConfig(BaseModel):
    you_get_plugins: list[YouGetPluginConfig]


arg_parser = ArgsConfigProvider()


class Config(BaseUnmarshalConfig, BaseDotenvConfig, BaseArgsConfig):
    @from_env()
    @arg_parser.from_flag(
        help="""Path to dotenv file.
If provided, will load dotenv file and merge with environment variables."""
    )
    def dotenv_path(self) -> str | None: ...

    @from_env()
    @arg_parser.from_flag(
        "-c",
        "--config",
        help="""Path to config file.
Will automatically use correct parser according to file extension.
Valid extensions: json, yaml, toml.
If not provided, will only load config from env and args.""",
    )
    def config_path(self) -> str | None: ...

    @from_env()
    @arg_parser.from_flag(
        choices=["trace", "debug", "info", "warning", "error"],
        help="Log level for fastAPI server and webhook service.",
    )
    @from_unmarshal()
    @default("info")
    def log_level(self) -> str: ...

    @from_env()
    @arg_parser.from_flag(help="Host to listen on.")
    @from_unmarshal("webhook", "host")
    @default("0.0.0.0")
    def webhook_host(self) -> str: ...

    @it_is(int)
    @from_env()
    @arg_parser.from_flag("--port", "-p", type=int, help="Port to listen on.")
    @from_unmarshal("webhook", "port")
    @default(8000)
    def webhook_port(self) -> int: ...

    @from_env()
    @arg_parser.from_flag(help="Host of memos service.")
    @from_unmarshal("memos", "host")
    @default("localhost")
    def memos_host(self) -> str: ...

    @it_is(int)
    @from_env()
    @arg_parser.from_flag(help="Port of memos service.")
    @from_unmarshal("memos", "port")
    @default("5230")
    def memos_port(self) -> str: ...

    @it_is(str, required=True)
    @from_env()
    @arg_parser.from_flag(help="Token for memos service.")
    @from_unmarshal("memos", "token")
    def memos_token(self) -> str: ...

    @it_is(PluginConfig)
    @from_unmarshal()
    def plugins(self) -> PluginConfig: ...


_config: Config


def new_config():
    global _config
    _config = Config()
    _config.load_args(arg_parser.parse_args())
    _config.load_dotenv(dotenv_path=_config.dotenv_path)
    _config.load_auto(_config.config_path)

    return _config


# Dependency for Config
def get_config() -> Config:
    assert _config, "config not initialized"
    return _config
