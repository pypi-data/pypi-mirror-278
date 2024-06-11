class DependencyResolver:
    def __init__(self):
        self.dependencies = {}
        self.visited = set()

    def add_dependency(self, component, dependency):
        self.dependencies.setdefault(component, []).append(dependency)

    def check_dependency_cycles(self, node):
        try:
            self.visited.clear()
            self.check_cycle(node, set())
            return False
        except ValueError:
            return True

    def check_cycle(self, node, visited):

        if node in visited:
            raise ValueError("Dependency cycle detected, Unable to continue.")

        visited.add(node)

        dependencies = self.dependencies.get(node, [])
        for neighbor in dependencies:
            self.check_cycle(neighbor, visited.copy())
