import os
from src.backend.PluginManager.ActionBase import ActionBase


ASSETS = os.path.join(os.path.dirname(__file__), "..", "..", "assets")


class VolumeDownAction(ActionBase):
    """Verringert die Lautstärke um 5%."""

    def on_ready(self):
        self.set_media(media_path=os.path.join(ASSETS, "volume_down.svg"), size=0.75)
        self._update_label(self.plugin_base.backend.state)
        self.plugin_base.backend.add_callback(self._on_state_change)

    def on_remove(self):
        self.plugin_base.backend.remove_callback(self._on_state_change)

    def on_key_down(self):
        state = self.plugin_base.backend.state
        self.plugin_base.backend.volume_down()

    def _on_state_change(self, state):
        self._update_label(state)

    def _update_label(self, state):
        self.set_label(f"{state.volume}%", font_size=12)
