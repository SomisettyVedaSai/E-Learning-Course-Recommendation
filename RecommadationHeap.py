"""
RecommadationHeap.py - Implements a min-heap for course recommendations based on student progress.
Uses array-based heap implementation for efficient priority-based operations.

Time Complexity:
- insert: O(log n)
- delete_root: O(log n)
- display: O(n)

Space Complexity: O(n) for storing n recommendations
"""

import random
import heapq

class RecommadationHeap:
    def __init__(self, maxSize=50):
        self.heap = []
        self.maxSize = maxSize
        self.course_popularity = {}  # Enhanced: Track course popularity

    def insert(self, course, priority):
        """Insert recommendation with priority - O(log n) time"""
        if len(self.heap) >= self.maxSize:
            # Remove lowest priority if heap is full
            heapq.heappop(self.heap)
        
        heapq.heappush(self.heap, (priority, course))
        
        # Track popularity
        self.course_popularity[course] = self.course_popularity.get(course, 0) + 1

    def delete_root(self):
        """Remove and return highest priority recommendation - O(log n) time"""
        if not self.heap:
            raise Exception("Heap is empty")
        priority, course = heapq.heappop(self.heap)
        return (course, priority)

    def get_highest_priority(self):
        """Get highest priority without removal - O(1) time"""
        if not self.heap:
            return None
        priority, course = self.heap[0]
        return (course, priority)

    def display(self):
        """Display all recommendations - O(n) time"""
        if not self.heap:
            print("Recommendation heap is empty")
            return []
        
        print(f"Recommendation Heap (size={len(self.heap)}):")
        sorted_recommendations = sorted([(priority, course) for priority, course in self.heap])
        for priority, course in sorted_recommendations:
            print(f"- {course} (priority: {priority})")
        
        return [(course, priority) for priority, course in sorted_recommendations]

    def insert_recommendation(self, course, progress, recommendation_threshold=3):
        """Enhanced: Insert recommendation based on progress - O(log n) time"""
        # Calculate priority based on progress and threshold
        if progress < recommendation_threshold:
            priority = progress  # Lower progress = higher priority
        else:
            priority = progress + random.randint(1, 5)  # Add some randomness
            
        self.insert(course, priority)

    def get_popular_courses(self, top_n=5):
        """Enhanced: Get most popular courses - O(n log n) time"""
        sorted_courses = sorted(self.course_popularity.items(), 
                              key=lambda x: x[1], reverse=True)
        return sorted_courses[:top_n]

    def clear(self):
        """Clear all recommendations - O(1) time"""
        self.heap = []
        print("Recommendation heap cleared.")

    def size(self):
        return len(self.heap)

    def is_empty(self):
        return len(self.heap) == 0

    def get_recommendations_for_progress(self, target_progress, max_recommendations=5):
        """Enhanced: Get recommendations matching target progress - O(n) time"""
        matching = []
        for priority, course in self.heap:
            if priority >= target_progress:
                matching.append((course, priority))
                
        matching.sort(key=lambda x: x[1])  # Sort by priority
        return matching[:max_recommendations]