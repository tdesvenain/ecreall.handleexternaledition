"""
Patches and code that makes version_on_unlock versioning policy work
"""

from webdav.Resource import Resource
from zope.event import notify
from zope.interface import implements
from zope.i18nmessageid import MessageFactory
from zope.component.hooks import getSite
from zope.component.interfaces import ObjectEvent, IObjectEvent

from Products.CMFEditions.utilities import maybeSaveVersion, isObjectChanged
from Products.CMFEditions.interfaces.IModifier import FileTooLargeToVersionError
from Products.CMFEditions.subscriber import _getVersionComment
from Products.CMFEditions import CMFEditionsMessageFactory as CEMF
from Products.Archetypes.interfaces.event import IWebDAVObjectEditedEvent

from collective.documentviewer.settings import GlobalSettings
from collective.documentviewer.utils import allowedDocumentType
from collective.documentviewer.async import queueJob

PMF = MessageFactory('plone')


class IWebdavUnlocked(IObjectEvent):
    """
    """

class WebdavUnlocked(ObjectEvent):
    """
    """
    implements(IWebdavUnlocked)


old_UNLOCK = Resource.UNLOCK
def UNLOCK_and_save_version(self, REQUEST, RESPONSE):
    """Unlock and then notify webdav unlocked event"""
    old_UNLOCK(self, REQUEST, RESPONSE)
    notify(WebdavUnlocked(self))


def handle_document_modified(obj, event, comment):
    obj = event.object

    changed = isObjectChanged(obj)

    if not changed:
        return

    handle_convert_document(obj, event)

    try:
        maybeSaveVersion(obj, policy='version_on_unlock', comment=comment, force=False)
    except FileTooLargeToVersionError:
        pass # There's no way to emit a warning here. Or is there?


def handle_unlock(obj, event):
    """Save a version when document is unlocked
    at the end of an external editing session
    """
    handle_document_modified(obj, event, comment=PMF('Edited'))


def handle_edited(obj, event):
    """Save a version when document is modified
    but not during an editing session
    """
    if IWebDAVObjectEditedEvent.providedBy(event):
        return

    comment = _getVersionComment(event.object) or PMF('Edited')
    return handle_document_modified(obj, event, comment=comment)


def handle_initialized(obj, event):
    """Save a version when document is initialized
    """
    comment = _getVersionComment(event.object) or CEMF('Initial revision')
    return handle_document_modified(obj, event, comment=comment)


def handle_convert_document(obj, event):
    """Convert document
    """
    site = getSite()
    gsettings = GlobalSettings(site)

    if not allowedDocumentType(obj, gsettings.auto_layout_file_types):
        return

    queueJob(obj)
