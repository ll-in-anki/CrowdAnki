from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Callable

from .anki_repo import AnkiRepo
from .archiver import Archiver
from ..anki_adapters.anki_deck import AnkiDeck
from ..export.deck_exporter import DeckExporter


@dataclass
class AnkiDeckArchiver(Archiver):
    deck_exporter: DeckExporter
    repo_provider: Callable[[Path], AnkiRepo]
    deck: AnkiDeck
    output_directory: Path

    def archive(self, decks: Iterable = tuple(), reason=None):
        deck_path = self.deck_exporter.export_to_directory(self.deck, self.output_directory)

        repo = self.repo_provider(deck_path)
        repo.init()
        repo.stage_all()
        repo.commit(reason)