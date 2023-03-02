from rest_framework import viewsets

from .mixins import *


class BetterReadWriteViewSet(BetterCreateModelMixin,
                             BetterListModelMixin,
                             viewsets.GenericViewSet):
    """POST+GET(Batch)-

    """
    pass


class BetterReadWriteDeleteViewSet(BetterCreateModelMixin,
                                   BetterListModelMixin,
                                   BetterDestroyMixin,
                                   viewsets.GenericViewSet):
    """POST+GET(Batch)+DELETE(soft)

    """
    pass
