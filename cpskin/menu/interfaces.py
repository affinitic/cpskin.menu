from zope.interface import Interface
from zope import schema


class ICpskinMenuLayer(Interface):
    """ Marker interface
    """


class IForthLevelNavigation(Interface):
    """ Marker interface
    """


class IMultiLevelNavigationView(Interface):
    """ Support for subtyping objects
    """

    can_enable_forth_level = schema.Bool(
        u'Can enable 4th level navigation',
        readonly=True
    )
    can_disable_forth_level = schema.Bool(
        u'Can disable 4th level navigation',
        readonly=True
    )

    def enable_forth_level():
        """ Enable 4th level navigation
        """

    def disable_forth_level():
        """ Disable 4th level navigation
        """
