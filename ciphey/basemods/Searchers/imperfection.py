from abc import abstractmethod
from typing import Set, Any, Union, List, Optional, Dict, Tuple

from loguru import logger

from .ausearch import Node, AuSearch
from ciphey.iface import (
    SearchLevel,
    Config,
    _registry,
    CrackResult,
    Searcher,
    ParamSpec,
    Decoder,
    DecoderComparer,
)

import bisect


class imperfection(AuSearch):
    """The default search module for Ciphey

    Called imperfection because ironically it is pretty perfect.

    """
    @staticmethod
    def getParams() -> Optional[Dict[str, ParamSpec]]:
        pass

    def findBestNode(self, nodes: Set[Node]) -> Node:
        return next(iter(nodes))

    def __init__(self, config: Config):
        super().__init__(config)


_registry.register(imperfection, Searcher)