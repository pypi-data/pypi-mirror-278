from iso_standards.errors import EntityNotFoundError


class EntityCollection:
    """A base class for ISO entity collections."""

    __slots__ = ("entities",)

    def __init__(self, entities=None):
        if entities is not None:
            self.entities = entities

    def __contains__(self, key):
        return self.entities.__contains__(key)

    def __getattr__(self, name):
        try:
            return self.__getattribute__(name)
        except AttributeError:
            try:
                return self.entities[name.replace("_", "-")]
            except KeyError:
                raise EntityNotFoundError

    def __iter__(self):
        yield from self.entities.values()

    def __len__(self):
        return len(self.entities)
