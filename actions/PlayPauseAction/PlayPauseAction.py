import os
import threading
from loguru import logger
from src.backend.PluginManager.ActionBase import ActionBase


ASSETS = os.path.join(os.path.dirname(__file__), "..", "..", "assets")


class PlayPauseAction(ActionBase):
    """Play/Pause-Taste – zeigt beim Spielen Cover-Art und Songtitel an."""

    def on_ready(self):
        self._last_cover_url = None
        self._update_ui(self.plugin_base.backend.state)
        self.plugin_base.backend.add_callback(self._on_state_change)

    def on_remove(self):
        self.plugin_base.backend.remove_callback(self._on_state_change)

    def on_key_down(self):
        self.plugin_base.backend.toggle()

    def _on_state_change(self, state):
        self._update_ui(state)

    def _update_ui(self, state):
        if not state.connected:
            self.set_media(media_path=os.path.join(ASSETS, "disconnected.svg"), size=0.75)
            self.set_label("Getrennt", font_size=12)
            return

        if state.is_playing and state.track_title:
            # Cover-Art im Hintergrund laden
            if state.cover_url != self._last_cover_url:
                self._last_cover_url = state.cover_url
                threading.Thread(
                    target=self._load_cover,
                    args=(state.track_title, state.track_artist),
                    daemon=True,
                ).start()
            else:
                self._set_track_label(state)
        else:
            # Pausiert oder kein Track: Play-Icon anzeigen
            self._last_cover_url = None
            self.set_media(media_path=os.path.join(ASSETS, "play.svg"), size=0.75)
            label = state.track_title or ""
            if state.track_artist and label:
                label = f"{state.track_artist}\n{label}"
            self.set_label(label, font_size=10)

    def _load_cover(self, title, artist):
        cover_path = self.plugin_base.backend.get_cover_art_path()
        if cover_path:
            try:
                self.set_media(media_path=cover_path, size=1.0)
            except Exception as exc:
                logger.warning(f"PlayPauseAction: Cover konnte nicht gesetzt werden – {exc}")
                self.set_media(media_path=os.path.join(ASSETS, "pause.svg"), size=0.75)
        else:
            self.set_media(media_path=os.path.join(ASSETS, "pause.svg"), size=0.75)

        label = title or ""
        if artist and label:
            label = f"{artist}\n{label}"
        try:
            self.set_label(label, font_size=10)
        except Exception:
            pass

    def _set_track_label(self, state):
        label = state.track_title or ""
        if state.track_artist and label:
            label = f"{state.track_artist}\n{label}"
        self.set_label(label, font_size=10)
