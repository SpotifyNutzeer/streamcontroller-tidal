import os
from src.backend.PluginManager.ActionBase import ActionBase


ASSETS = os.path.join(os.path.dirname(__file__), "..", "..", "assets")


class ShuffleAction(ActionBase):
    """Schaltet die Zufallswiedergabe an/aus."""

    def on_ready(self):
        self._update_ui(self.plugin_base.backend.state)
        self.plugin_base.backend.add_callback(self._on_state_change)

    def on_remove(self):
        self.plugin_base.backend.remove_callback(self._on_state_change)

    def on_key_down(self):
        new_state = not self.plugin_base.backend.state.shuffle
        self.plugin_base.backend.set_shuffle(new_state)

    def _on_state_change(self, state):
        self._update_ui(state)

    def _update_ui(self, state):
        if state.shuffle:
            self.set_media(media_path=os.path.join(ASSETS, "shuffle_on.svg"), size=0.75)
        else:
            self.set_media(media_path=os.path.join(ASSETS, "shuffle_off.svg"), size=0.75)
        self.set_label("")
