import heapq

class DynamicPriorityQueue:
    def __init__(self):
        self.heap = []
        self.vertex_height = {}  # Dictionary to track current heights
        self.invalid_entries = set()  # Set to track invalidated entries

    def add_vertex(self, vertex, height):
        self.vertex_height[vertex] = height
        heapq.heappush(self.heap, (height, vertex))

    def change_height(self, vertex, new_height):
        if vertex in self.vertex_height:
            old_height = self.vertex_height[vertex]
            self.invalid_entries.add((old_height, vertex))  # Mark old height as invalid
        self.vertex_height[vertex] = new_height
        heapq.heappush(self.heap, (new_height, vertex))

    def peek(self):
        while self.heap:
            height, vertex = self.heap[0]  # Look at the top element
            if (height, vertex) in self.invalid_entries:
                # Remove stale entry
                heapq.heappop(self.heap)
                self.invalid_entries.remove((height, vertex))
            else:
                # Valid entry
                return vertex, height
        raise KeyError("Priority queue is empty")

    def get_current_height(self, vertex):
        return self.vertex_height.get(vertex, None)

