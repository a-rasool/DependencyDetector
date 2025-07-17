from abc import ABC, abstractmethod

class BaseDependencyDetector(ABC):
    def __init__(self, data):
        self.data = data
        
        @abstractmethod
        def compute_dependencies(self):
            pass
        
        @abstractmethod
        def visualize(self, out_path: str):
            pass