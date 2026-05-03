import os
from src.backend.PluginManager.ActionBase import ActionBase


ASSETS = os.path.join(os.path.dirname(__file__), "..", "..", "assets")


class NextAction(ActionBase):
    """Taste zum Überspringen zum nächsten Track."""

    def on_ready(self):
        self.set_media(media_path=os.path.join(ASSETS, "next.svg"), size=0.75)
        self.set_label("")

    def on_key_down(self):
        self.plugin_base.backend.next_track()
