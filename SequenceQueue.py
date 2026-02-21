"""
SequenceQueue.py - Implements a circular queue for scheduling course sequences with priorities.
Supports efficient enqueue/dequeue operations for course scheduling.

Time Complexity:
- enqueue: O(1)
- dequeue: O(1)
- update_priority: O(n) worst case

Space Complexity: O(n) for storing n sequences
"""

from datetime import timedelta
from collections import deque

class SequenceQueue:
    def __init__(self, size=50):
        self.tasks = deque(maxlen=size)  # Use deque for efficient operations
        self.size = size
        self.course_durations = {}  # Enhanced: Store course durations

    def enqueue(self, task):
        """Enqueue task - O(1) time"""
        if len(self.tasks) >= self.size:
            # Remove oldest task if queue is full (circular behavior)
            self.tasks.popleft()
        self.tasks.append(task)

    def dequeue(self):
        """Dequeue task - O(1) time"""
        if self.is_empty():
            raise Exception("Queue is empty")
        return self.tasks.popleft()

    def is_empty(self):
        return len(self.tasks) == 0

    def display(self):
        """Display all tasks - O(n) time"""
        if self.is_empty():
            print("Queue is empty")
            return
        
        print("Current tasks in the queue:")
        for i, task in enumerate(self.tasks):
            print(f"{i+1}. {task}")

    def schedule_course(self, course_name, duration, priority):
        """Schedule a course - O(1) time"""
        task = (course_name, priority, duration)
        self.enqueue(task)
        self.course_durations[course_name] = duration
        print(f"Scheduled: {course_name} (priority: {priority}, duration: {duration})")

    def update_priority(self, course_name, new_priority):
        """Update course priority - O(n) time"""
        updated = False
        new_tasks = deque(maxlen=self.size)
        
        for task in self.tasks:
            if task[0] == course_name:
                new_tasks.append((course_name, new_priority, task[2]))
                updated = True
            else:
                new_tasks.append(task)
        
        if not updated:
            # Course not found, add as new task
            default_duration = self.course_durations.get(course_name, timedelta(days=1))
            new_tasks.append((course_name, new_priority, default_duration))
            print(f"Added new course: {course_name}")
        
        self.tasks = new_tasks
        print(f"Updated priority for {course_name} to {new_priority}")

    def get_next_sequence(self):
        """Enhanced: Get next sequence without removing - O(1) time"""
        if self.is_empty():
            return None
        return self.tasks[0]

    def get_queue_size(self):
        return len(self.tasks)

    def clear_completed_courses(self, completed_courses):
        """Enhanced: Remove completed courses - O(n) time"""
        self.tasks = deque([task for task in self.tasks 
                          if task[0] not in completed_courses], 
                         maxlen=self.size)
        print(f"Cleared completed courses. Remaining: {len(self.tasks)} tasks")

    def estimate_completion_time(self):
        """Enhanced: Estimate total completion time - O(n) time"""
        total_duration = timedelta()
        for task in self.tasks:
            total_duration += task[2]  # duration is at index 2
        return total_duration

    def get_courses_by_priority(self, priority_level):
        """Enhanced: Get courses by priority level - O(n) time"""
        return [task for task in self.tasks if task[1] == priority_level]