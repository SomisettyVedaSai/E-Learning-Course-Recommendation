"""
StudentHashMap.py - Implements a hash map for storing student data with efficient retrieval.
Uses dictionary for O(1) average case operations.

Time Complexity:
- insert_student: O(1) average
- retrieve_student_data: O(1) average
- update_student_progress: O(1) average

Space Complexity: O(n) where n is number of students
"""

from StudentHistoryArray import StudentHistoryArray
from datetime import datetime

class Student:
    def __init__(self, student_id, name, age, gender):
        self.student_id = student_id
        self.name = name
        self.age = age
        self.gender = gender
        self.current_course = None
        self.completed_courses = set()  # Track completed courses
        self.completed_sequences = set()  # Track completed sequences
        self.progress = 0
        self.quiz_scores = {}  # Enhanced: Store quiz scores per course
        self.history = StudentHistoryArray()
        self.learning_style = "Visual"  # Enhanced: Default learning style

    def update_progress(self, course, sequence, score=None):
        """Update student progress - O(1) time"""
        sequence_key = f"{course}_{sequence}"
        
        if sequence_key not in self.completed_sequences:
            self.completed_sequences.add(sequence_key)
            self.progress += 1
            
            # Store quiz score if provided
            if score is not None:
                if course not in self.quiz_scores:
                    self.quiz_scores[course] = []
                self.quiz_scores[course].append(score)
            
            # Add to history
            self.history.append_activity(
                "Sequence Completion", 
                datetime.now(), 
                score, 
                {"course": course, "sequence": sequence}
            )

    def complete_course(self, course):
        """Mark course as completed - O(1) time"""
        self.completed_courses.add(course)
        self.current_course = None
        self.history.append_activity(
            "Course Completion",
            datetime.now(),
            None,
            {"course": course}
        )

    def get_average_score(self, course=None):
        """Enhanced: Get average quiz scores - O(n) time"""
        if course:
            scores = self.quiz_scores.get(course, [])
            return sum(scores) / len(scores) if scores else 0
        else:
            all_scores = [score for course_scores in self.quiz_scores.values() for score in course_scores]
            return sum(all_scores) / len(all_scores) if all_scores else 0

    def set_learning_style(self, style):
        """Enhanced: Set learning style - O(1) time"""
        self.learning_style = style

class StudentHashMap:
    def __init__(self):
        self.student_map = {}

    def insert_student(self, student):
        """Insert student - O(1) average time"""
        self.student_map[student.student_id] = student

    def update_student_progress(self, student_id, course, sequence, score=None):
        """Update student progress - O(1) average time"""
        student = self.student_map.get(student_id)
        if student:
            student.update_progress(course, sequence, score)
        else:
            print(f"Student with ID {student_id} not found.")

    def retrieve_student_data(self, student_id):
        """Retrieve student data - O(1) average time"""
        student = self.student_map.get(student_id)
        if student:
            return {
                'name': student.name,
                'age': student.age,
                'gender': student.gender,
                'current_course': student.current_course,
                'progress': student.progress,
                'completed_courses': list(student.completed_courses),
                'learning_style': student.learning_style,
                'average_score': student.get_average_score(),
                'history': list(student.history.iterate_activities())
            }
        else:
            print(f"Student with ID {student_id} not found.")
            return None

    def get_all_students(self):
        """Enhanced: Get all students - O(1) time"""
        return list(self.student_map.values())

    def get_students_by_course(self, course_name):
        """Enhanced: Get students enrolled in specific course - O(n) time"""
        return [student for student in self.student_map.values() 
                if student.current_course == course_name]