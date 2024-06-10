# -*- coding: utf-8 -*-
"""Init and utils."""
import logging

from zope.i18nmessageid import MessageFactory

from . import patches

log = logging.getLogger("collective.flexmailhost")

_ = MessageFactory("collective.flexmailhost")

patches.apply_patches()
