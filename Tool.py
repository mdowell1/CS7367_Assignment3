from abc import abstractmethod, ABC


class Tool(ABC):
    @staticmethod
    @abstractmethod
    def onClick():
        print("default")


class Rectangle(Tool):
    @staticmethod
    def onClick():
        print("Rectangle onClick")


class Translate(Tool):
    @staticmethod
    def onClick():
        print("Translate onClick")


class Rigid(Tool):
    @staticmethod
    def onClick():
        print("Rigid onClick")


class Similarity(Tool):
    @staticmethod
    def onClick():
        print("Similarity onClick")


class Affine(Tool):
    @staticmethod
    def onClick():
        print("Affine onClick")


class Projective(Tool):
    @staticmethod
    def onClick():
        print("Projective onClick")
