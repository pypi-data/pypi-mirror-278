from src.plugins.base_plugin import PluginExecutor, PluginProtocol
from src.plugins.you_get_plugin import YouGetPlugin

from .config import Config, PluginConfig, YouGetPluginConfig
from .memos_cli import MemosCli

_plugin_executor: PluginExecutor = None


_DEFAULT_PLUGIN_CFG = PluginConfig(
    you_get_plugins=[
        YouGetPluginConfig(
            name="you-get",
            tag="hook/download",
            patterns=[
                "https://twitter.com/\\w+/status/\\d+",
                "https://x.com/\\w+/status/\\d+",
            ],
        ),
    ]
)


def new_plugin_executor(cfg: Config, memos_cli: MemosCli) -> PluginExecutor:
    global _plugin_executor
    plugins_cfg = cfg.plugins
    if plugins_cfg is None:
        plugins_cfg = _DEFAULT_PLUGIN_CFG  # temp fake cfg

    plugins: list[PluginProtocol] = []
    for you_get_plugin_cfg in plugins_cfg.you_get_plugins:
        plugins.append(YouGetPlugin(you_get_plugin_cfg))

    _plugin_executor = PluginExecutor(memos_cli, plugins)
    return _plugin_executor


def get_plugin_executor() -> PluginExecutor:
    assert _plugin_executor is not None, "plugin_executor not initialized"
    return _plugin_executor
