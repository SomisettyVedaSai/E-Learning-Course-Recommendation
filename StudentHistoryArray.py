"""
StudentHistoryArray.py - Implements a dynamic array for storing student activity history.
Uses Python list with efficient append operations.

Time Complexity:
- append_activity: O(1) amortized
- iterate_activities: O(n) for n activities

Space Complexity: O(n) where n is number of activities
"""

from datetime import datetime

class Activity:
    def __init__(self, activity_type, timestamp, score=None, metadata=None):
        self.activity_type = activity_type
        self.timestamp = timestamp
        self.score = score
        self.metadata = metadata or {}

    def __repr__(self):
        return (f"Activity(type={self.activity_type}, timestamp={self.timestamp}, "
                f"score={self.score}, metadata={self.metadata})")

    def to_dict(self):
        """Convert activity to dictionary for easy serialization"""
        return {
            'type': self.activity_type,
            'timestamp': self.timestamp.isoformat(),
            'score': self.score,
            'metadata': self.metadata
        }

class StudentHistoryArray:
    def __init__(self, initial_size=10):
        self.activities = []
        self.size = 0

    def append_activity(self, activity_type, timestamp, score=None, metadata=None):
        """Append activity - O(1) amortized time"""
        activity = Activity(activity_type, timestamp, score, metadata)
        self.activities.append(activity)
        self.size += 1

    def iterate_activities(self):
        """Iterate through activities - O(n) time for n activities"""
        for activity in self.activities:
            yield activity

    def get_recent_activities(self, count=5):
        """Enhanced: Get most recent activities - O(1) time"""
        return self.activities[-count:] if self.activities else []

    def get_activities_by_type(self, activity_type):
        """Enhanced: Filter activities by type - O(n) time"""
        return [activity for activity in self.activities 
                if activity.activity_type == activity_type]

    def get_activities_in_range(self, start_date, end_date):
        """Enhanced: Get activities within date range - O(n) time"""
        return [activity for activity in self.activities 
                if start_date <= activity.timestamp <= end_date]

    def clear_old_activities(self, cutoff_date):
        """Enhanced: Remove activities before cutoff date - O(n) time"""
        self.activities = [activity for activity in self.activities 
                          if activity.timestamp >= cutoff_date]
        self.size = len(self.activities)

    def __len__(self):
        return self.size

    def __iter__(self):
        return iter(self.activities)