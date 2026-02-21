"""
CourseGraph.py - Implements a directed graph for course dependencies and prerequisite management.
Supports topological sorting, path finding, and prerequisite validation.

Time Complexity:
- add_module: O(1)
- add_prerequisite: O(1)
- topological_sort: O(V + E) where V=vertices, E=edges
- find_all_prerequisites: O(V + E) - BFS traversal

Space Complexity: O(V + E) for storing graph structure
"""

from collections import deque

class CourseGraph:
    def __init__(self):
        # Stores the graph as an adjacency list, in-degrees for topological sorting, and content for each module
        self.graph = {}
        self.in_degrees = {}
        self.content = {} 
        self.sequences = {}  # Sequence tasks for each course
        self.course_descriptions = {}  # Enhanced: Store course descriptions

    def add_module(self, module, sequences=None, description=""):
        """Initialize course module - O(1) time"""
        if module not in self.graph:
            self.graph[module] = []
            self.in_degrees[module] = 0
            self.content[module] = []
            self.sequences[module] = sequences if sequences else []
            self.course_descriptions[module] = description

    def add_prerequisite(self, prerequisite, module):
        """Add prerequisite relationship - O(1) time"""
        if prerequisite not in self.graph:
            self.add_module(prerequisite)
        if module not in self.graph:
            self.add_module(module)
        
        # Avoid duplicate edges
        if module not in self.graph[prerequisite]:
            self.graph[prerequisite].append(module)
            self.in_degrees[module] += 1

    def topological_sort(self):
        """Topological sort using Kahn's algorithm - O(V + E) time"""
        in_degrees = self.in_degrees.copy()
        zero_in_degree = deque([node for node in self.graph if in_degrees[node] == 0])
        topo_order = []

        while zero_in_degree:
            module = zero_in_degree.popleft()
            topo_order.append(module)

            for neighbor in self.graph[module]:
                in_degrees[neighbor] -= 1
                if in_degrees[neighbor] == 0:
                    zero_in_degree.append(neighbor)

        if len(topo_order) == len(self.graph):
            return topo_order
        else:
            raise ValueError("Cycle detected in prerequisites, topological sort not possible.")

    def find_all_prerequisites(self, module):
        """Find all prerequisites using BFS - O(V + E) time"""
        if module not in self.graph:
            return set()
            
        prerequisites = set()
        queue = deque([module])
        visited = set([module])

        while queue:
            current = queue.popleft()
            for prereq in self.graph:
                if current in self.graph[prereq] and prereq not in visited:
                    prerequisites.add(prereq)
                    visited.add(prereq)
                    queue.append(prereq)

        return prerequisites

    def find_shortest_path(self, start, end):
        """Find shortest path using BFS - O(V + E) time"""
        if start not in self.graph or end not in self.graph:
            return None
            
        queue = deque([(start, [start])])
        visited = set([start])

        while queue:
            current, path = queue.popleft()
            if current == end:
                return path

            for neighbor in self.graph[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return None  # No path found

    def can_access_module(self, module, completed_modules):
        """Check if module can be accessed - O(1) average time"""
        prerequisites = self.find_all_prerequisites(module)
        return prerequisites.issubset(completed_modules)

    def get_prerequisites(self, module):
        """Get direct prerequisites - O(1) time"""
        if module not in self.graph:
            raise ValueError(f"Module {module} does not exist.")
        return [prereq for prereq in self.graph if module in self.graph[prereq]]

    def add_content(self, course_title, content):
        """Add content to course - O(1) time"""
        if course_title in self.graph:
            if content not in self.content[course_title]:  # Avoid duplicates
                self.content[course_title].append(content)
        else:
            raise ValueError(f"Course {course_title} does not exist.")

    def get_content(self, course_title):
        """Retrieve course content - O(1) time"""
        if course_title in self.content:
            return self.content[course_title]
        else:
            raise ValueError(f"Course {course_title} does not exist.")

    def get_courses_by_content(self, content_keyword):
        """Enhanced: Find courses containing specific content - O(V) time"""
        matching_courses = []
        for course, contents in self.content.items():
            for content in contents:
                if content_keyword.lower() in content.lower():
                    matching_courses.append(course)
                    break
        return matching_courses

    def get_course_description(self, course_title):
        """Enhanced: Get course description - O(1) time"""
        return self.course_descriptions.get(course_title, "No description available.")

    def set_course_description(self, course_title, description):
        """Enhanced: Set course description - O(1) time"""
        if course_title in self.graph:
            self.course_descriptions[course_title] = description
        else:
            raise ValueError(f"Course {course_title} does not exist.")

    def check_sequences_completion(self, module, completed_sequences):
        """Check if all sequences are completed - O(n) time"""
        required_sequences = set(self.sequences.get(module, []))
        return required_sequences.issubset(set(completed_sequences))

    def get_learning_path(self, target_course):
        """Enhanced: Get optimal learning path to target course - O(V + E) time"""
        try:
            topo_order = self.topological_sort()
            path = []
            for course in topo_order:
                if course == target_course:
                    path.append(course)
                    break
                path.append(course)
            return path
        except ValueError:
            return f"Cannot create learning path due to circular dependencies"