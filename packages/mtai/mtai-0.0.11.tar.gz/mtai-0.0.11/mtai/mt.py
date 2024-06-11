# The `MT` class is a subclass of `MTAIBase` that initializes the `mtai` library with secret key and
# provides access to tags, prompts, and bios functionalities.
"""Entry point defined here."""

from mtai.base import MTAIBase
from mtai.tags import Tag
from mtai.prompts import Prompt
from mtai.bios import Bio


class MT(MTAIBase):
    """MT Class used across defined."""

    def __init__(self, *args, **kwargs):
        """Initialize mtai with secret key."""
        MTAIBase.__init__(self, *args, **kwargs)

        self.tags = Tag
        self.prompts = Prompt
        self.bios = Bio
