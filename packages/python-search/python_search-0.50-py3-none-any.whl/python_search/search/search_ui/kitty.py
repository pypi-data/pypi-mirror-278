import os

import logging
import sys
from python_search.host_system.system_paths import SystemPaths
from python_search.environment import is_mac


class KittySearch:
    """
    Renders the search ui using fzf + termite terminal
    """

    _DEFAULT_WINDOW_SIZE = (955, 230)

    _configuration = None

    def __init__(self, configuration=None):
        logger = logging.getLogger(name="search_ui")
        logger.addHandler(logging.StreamHandler(sys.stdout))
        logger.setLevel(logging.DEBUG)
        self._logger = logger

        if not configuration:
            from python_search.configuration.loader import ConfigurationLoader

            configuration = ConfigurationLoader().load_config()
        self._configuration = configuration
        custom_window_size = configuration.get_window_size()
        self._width = (
            custom_window_size[0]
            if custom_window_size
            else self._DEFAULT_WINDOW_SIZE[0]
        )
        self._height = (
            custom_window_size[1]
            if custom_window_size
            else self._DEFAULT_WINDOW_SIZE[1]
        )

        self._title = configuration.APPLICATION_TITLE

    def launch(self) -> None:
        """
        Entry point for the application to launch the search ui
        """
        from python_search.apps.terminal import Terminal
        from python_search.theme import get_current_theme

        theme = get_current_theme()

        terminal = Terminal()
        from python_search.host_system.system_paths import SystemPaths


        launch_cmd = f"""{get_kitty_cmd()} \
        --title {self._title} \
        --listen-on unix:/tmp/mykitty \
        -o allow_remote_control=yes \
        -o draw_minimal_borders=no \
        -o window_padding_width=0  \
        -o placement_strategy=center \
        -o window_border_width=0 \
        -o window_padding_width=0 \
        -o hide_window_decorations=titlebar-only \
        -o background_opacity=1 \
        -o active_tab_title_template=none \
        -o initial_window_width={self._width}  \
        -o initial_window_height={self._height} \
        -o background={theme.backgroud} \
        -o foreground={theme.text} \
        -o font_size="{theme.font_size}" \
        -o font_family="SF\ Pro" \
        {terminal.GLOBAL_TERMINAL_PARAMS} \
         {SystemPaths.BINARIES_PATH}/term_ui
        """
        result = os.system(launch_cmd)
        if result != 0:
            raise Exception("Failed: " + str(result), launch_cmd)

    @staticmethod
    def run() -> None:
        if not KittySearch.try_to_focus():
            KittySearch().launch()

    @staticmethod
    def try_to_focus():
        """
        Focuses the terminal if it is already open
        """
        if not os.path.exists("/tmp/mykitty"):
            return False

        result = os.system(KittySearch.focus_kitty_command())

        return result == 0

    @staticmethod
    def focus_or_open(configuration):
        if not KittySearch.try_to_focus():
            KittySearch(configuration).launch()

    @staticmethod
    def focus_kitty_command():
        return f"{get_kitty_cmd()} @ --to unix:/tmp/mykitty focus-window"


def get_kitty_cmd() -> str:
    if is_mac():
        return SystemPaths.KITTY_BINNARY
    return "kitty"


def main():
    import fire

    fire.Fire(KittySearch)


if __name__ == "__main__":
    main()
