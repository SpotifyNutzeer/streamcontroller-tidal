import os
from src.backend.PluginManager.ActionBase import ActionBase


ASSETS = os.path.join(os.path.dirname(__file__), "..", "..", "assets")

# Icons je Wiederhol-Modus
REPEAT_ICONS = {
    0: "loop_off.svg",
    1: "loop_all.svg",
    2: "loop_one.svg",
}

REPEAT_LABELS = {
    0: "Aus",
    1: "Alles",
    2: "Eines",
}


class LoopAction(ActionBase):
    """Schaltet durch die Wiederhol-Modi: Aus → Alles → Eines → Aus …"""

    def on_ready(self):
        self._update_ui(self.plugin_base.backend.state)
        self.plugin_base.backend.add_callback(self._on_state_change)

    def on_remove(self):
        self.plugin_base.backend.remove_callback(self._on_state_change)

    def on_key_down(self):
        current = self.plugin_base.backend.state.repeat
        next_mode = (current + 1) % 3
        self.plugin_base.backend.set_repeat(next_mode)

    def _on_state_change(self, state):
        self._update_ui(state)

    def _update_ui(self, state):
        mode = state.repeat
        icon = REPEAT_ICONS.get(mode, "loop_off.svg")
        self.set_media(media_path=os.path.join(ASSETS, icon), size=0.75)
        self.set_label("")
