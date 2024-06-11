from abc import ABC, abstractmethod


class BaseMapping(ABC):
    URL = None
    RESOURCE_TYPE = None

    def __init__(self, session):
        self.session = session

    @abstractmethod
    def add(self):
        raise NotImplementedError

    @abstractmethod
    def edit(self):
        raise NotImplementedError

    @abstractmethod
    def get_all(self):
        raise NotImplementedError

    @abstractmethod
    def get(self):
        raise NotImplementedError

    @abstractmethod
    def delete(self):
        raise NotImplementedError

    @abstractmethod
    def download(self):
        raise NotImplementedError
