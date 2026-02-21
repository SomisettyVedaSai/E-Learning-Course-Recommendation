"""
Main.py - Main application file integrating all ADTs for the Learning Management System.
Provides admin, student, and course management functionalities.

Time Complexity: Various depending on operations
Space Complexity: O(n) for storing system data
"""

import random
from datetime import datetime, timedelta

# Import all ADTs
from ContentTrie import ContentTrie
from CourseGraph import CourseGraph
from StudentHashMap import StudentHashMap, Student
from RecommadationHeap import RecommadationHeap
from SequenceQueue import SequenceQueue
from StudentHistoryArray import StudentHistoryArray

class LearningManagementSystem:
    def __init__(self):
        # Initialize all ADTs
        self.course_graph = CourseGraph()
        self.content_trie = ContentTrie()
        self.student_map = StudentHashMap()
        self.recommendation_heap = RecommadationHeap()
        self.schedule_queue = SequenceQueue()
        self.history_tracker = StudentHistoryArray()

    def initialize_courses_with_schedule(self):
        """Initialize predefined courses - O(n) time"""
        courses = {
            "Data Structures": {
                "content": ["Arrays", "Linked Lists", "Stacks", "Queues", "Trees"],
                "priority": 1,
                "prereqs": [],
                "sequences": [("Arrays Basics", timedelta(days=1)), 
                            ("Linked Lists Operations", timedelta(days=2)), 
                            ("Stack Implementation", timedelta(days=1))],
                "description": "Fundamental data structures and their implementations"
            },
            "Algorithms": {
                "content": ["Sorting", "Searching", "Graph Algorithms", "Dynamic Programming"],
                "priority": 2,
                "prereqs": ["Data Structures"],
                "sequences": [("Sorting Techniques", timedelta(days=2)), 
                            ("Binary Search", timedelta(days=1)),
                            ("Graph Traversal", timedelta(days=3))],
                "description": "Algorithm design and analysis techniques"
            },
            "Advanced Programming": {
                "content": ["Recursion", "Dynamic Programming", "Backtracking", "Optimization"],
                "priority": 3,
                "prereqs": ["Algorithms"],
                "sequences": [("Recursion Basics", timedelta(days=1)), 
                            ("Dynamic Programming Patterns", timedelta(days=3)),
                            ("Backtracking Problems", timedelta(days=2))],
                "description": "Advanced programming concepts and problem solving"
            },
            "Database Systems": {
                "content": ["SQL", "Normalization", "Indexing", "Transactions"],
                "priority": 2,
                "prereqs": ["Data Structures"],
                "sequences": [("SQL Basics", timedelta(days=2)), 
                            ("Database Design", timedelta(days=3))],
                "description": "Database design, implementation and management"
            }
        }

        for course_name, details in courses.items():
            # Add course to graph
            self.course_graph.add_module(
                course_name, 
                [seq[0] for seq in details["sequences"]],
                details["description"]
            )
            
            # Add content to trie
            for content in details["content"]:
                self.content_trie.insertContent(content)
                self.course_graph.add_content(course_name, content)
            
            # Add prerequisites
            for prereq in details["prereqs"]:
                self.course_graph.add_prerequisite(prereq, course_name)
            
            # Schedule sequences
            for sequence, duration in details["sequences"]:
                self.schedule_queue.schedule_course(sequence, duration, details["priority"])

        print("✓ Predefined courses with schedules initialized.")
        print(f"✓ Loaded {len(courses)} courses")

    def initialize_students_with_current_courses(self):
        """Initialize predefined students - O(n) time"""
        students = [
            {
                "student_id": "S101",
                "name": "Santosh",
                "age": 20,
                "gender": "Male",
                "completed_courses": ["Data Structures"],
                "scores": {"Data Structures": 85},
                "current_courses": ["Algorithms"],
                "learning_style": "Visual"
            },
            {
                "student_id": "S102", 
                "name": "Shanmukh",
                "age": 22,
                "gender": "Male",
                "completed_courses": ["Data Structures", "Algorithms"],
                "scores": {"Data Structures": 78, "Algorithms": 88},
                "current_courses": ["Advanced Programming"],
                "learning_style": "Kinesthetic"
            },
            {
                "student_id": "S103",
                "name": "Varma",
                "age": 21,
                "gender": "Male", 
                "completed_courses": [],
                "scores": {},
                "current_courses": ["Data Structures"],
                "learning_style": "Auditory"
            }
        ]
        
        for student_data in students:
            student = Student(
                student_data["student_id"],
                student_data["name"], 
                student_data["age"],
                student_data["gender"]
            )
            
            # Set learning style
            student.set_learning_style(student_data["learning_style"])
            
            # Add completed courses and scores
            for course, score in student_data["scores"].items():
                # Simulate sequence completion for completed courses
                sequences = self.course_graph.sequences.get(course, [])
                for seq in sequences:
                    student.update_progress(course, seq, random.randint(70, 95))
                student.complete_course(course)
                self.recommendation_heap.insert(course, score)
            
            # Set current courses
            if student_data["current_courses"]:
                student.current_course = student_data["current_courses"][0]
            
            self.student_map.insert_student(student)
        
        print("✓ Predefined students initialized.")
        print(f"✓ Loaded {len(students)} students")

    def random_quiz_score(self):
        """Generate random quiz score - O(1) time"""
        return random.randint(60, 100)

    # Admin functionalities
    def add_course(self):
        """Admin: Add new course - O(1) time"""
        course_name = input("Enter the course name to add: ").strip()
        if course_name in self.course_graph.graph:
            print(f"❌ Course '{course_name}' already exists.")
        else:
            description = input("Enter course description: ").strip()
            self.course_graph.add_module(course_name, description=description)
            print(f"✅ Course '{course_name}' added successfully.")

    def add_content_to_course(self):
        """Admin: Add content to course - O(m) time"""
        course_name = input("Enter course name for adding content: ").strip()
        if course_name in self.course_graph.graph:
            content = input("Enter content (title, keyword, tag): ").strip()
            self.content_trie.insertContent(content)
            self.course_graph.add_content(course_name, content)
            print(f"✅ Content '{content}' added to course '{course_name}'.")
        else:
            print("❌ Course not found.")

    def change_course_priority(self):
        """Admin: Change course priority - O(n) time"""
        course_name = input("Enter course name to change priority: ").strip()
        try:
            priority = int(input("Enter new priority level (lower is higher priority): "))
            self.schedule_queue.update_priority(course_name, priority)
            print(f"✅ Priority of course '{course_name}' updated to {priority}.")
        except ValueError:
            print("❌ Invalid priority. Please enter a number.")

    def view_system_stats(self):
        """Admin: View system statistics - O(n) time"""
        print("\n===== SYSTEM STATISTICS =====")
        print(f"Total Courses: {len(self.course_graph.graph)}")
        print(f"Total Students: {len(self.student_map.student_map)}")
        print(f"Total Content Items: {len(self.content_trie.getAllContents())}")
        print(f"Scheduled Sequences: {self.schedule_queue.get_queue_size()}")
        print(f"Active Recommendations: {self.recommendation_heap.size()}")
        
        # Popular courses
        popular = self.recommendation_heap.get_popular_courses(3)
        if popular:
            print("\nMost Popular Courses:")
            for course, count in popular:
                print(f"  - {course}: {count} recommendations")

    # Student functionalities
    def create_new_user(self):
        """Create new student account - O(1) time"""
        print("\n===== NEW STUDENT REGISTRATION =====")
        student_id = input("Enter Student ID: ").strip()
        
        # Check if student ID already exists
        if self.student_map.retrieve_student_data(student_id):
            print("❌ Student ID already exists. Please use a different ID.")
            return
            
        name = input("Enter Name: ").strip()
        age = int(input("Enter Age: "))
        gender = input("Enter Gender: ").strip()
        
        # Learning style preference
        print("\nSelect Learning Style:")
        print("1. Visual")
        print("2. Auditory") 
        print("3. Kinesthetic")
        style_choice = input("Enter choice (1-3): ").strip()
        styles = {"1": "Visual", "2": "Auditory", "3": "Kinesthetic"}
        learning_style = styles.get(style_choice, "Visual")
        
        student = Student(student_id, name, age, gender)
        student.set_learning_style(learning_style)
        self.student_map.insert_student(student)
        
        print(f"✅ Registration successful! Welcome {name}!")
        print(f" Your learning style: {learning_style}")
        
        # Start course search
        self.enhanced_search_content(student)

    def enhanced_search_content(self, student):
        """Enhanced content search with course recommendations - O(m + k) time"""
        print("\n===== COURSE SEARCH =====")
        prefix = input("Enter a keyword or course title to search: ").strip()
        
        if not prefix:
            print("❌ Please enter a search term.")
            return
            
        content_results = self.content_trie.autocomplete(prefix)
        
        if content_results:
            print(f"\n Found {len(content_results)} matching content(s):")
            for i, content in enumerate(content_results, 1):
                print(f"  {i}. {content}")
            
            # Find courses containing this content
            course_names = set()
            for content in content_results:
                courses = self.course_graph.get_courses_by_content(content)
                course_names.update(courses)
            
            if course_names:
                print(f"\n Related Courses ({len(course_names)} found):")
                for i, course in enumerate(course_names, 1):
                    desc = self.course_graph.get_course_description(course)
                    print(f"  {i}. {course} - {desc}")
                
                try:
                    choice = int(input(f"\nEnter the number of course you'd like to take (1-{len(course_names)}): "))
                    if 1 <= choice <= len(course_names):
                        course_name = list(course_names)[choice-1]
                        self.enroll_in_course(student, course_name)
                    else:
                        print("❌ Invalid choice.")
                except ValueError:
                    print("❌ Please enter a valid number.")
            else:
                print("❌ No courses found for the search term.")
        else:
            print("❌ No content found for that keyword.")

    def enroll_in_course(self, student, course_name):
        """Enroll student in course with prerequisite check - O(V + E) time"""
        print(f"\n🎓 Enrolling in: {course_name}")
        
        # Check prerequisites
        prerequisites = self.course_graph.find_all_prerequisites(course_name)
        missing_prereqs = [prereq for prereq in prerequisites 
                          if prereq not in student.completed_courses]
        
        if missing_prereqs:
            print(f"⚠️  Prerequisites required: {', '.join(missing_prereqs)}")
            choice = input("Do you want to see the learning path? (yes/no): ").strip().lower()
            if choice == 'yes':
                path = self.course_graph.get_learning_path(course_name)
                print(f" Recommended learning path: {' → '.join(path)}")
            return
        
        # Check if already completed
        if course_name in student.completed_courses:
            print("✅ You have already completed this course!")
            return
            
        # Enroll in course
        student.current_course = course_name
        print(f"✅ Successfully enrolled in '{course_name}'")
        
        # Start first sequence
        sequences = self.course_graph.sequences.get(course_name, [])
        if sequences:
            print(f" Starting first sequence: {sequences[0]}")
            self.complete_sequence(student, course_name, sequences[0])

    def complete_sequence(self, student, course_name, sequence):
        """Complete a course sequence - O(1) time"""
        quiz_score = self.random_quiz_score()
        student.update_progress(course_name, sequence, quiz_score)
        
        # Add recommendation
        self.recommendation_heap.insert_recommendation(course_name, student.progress)
        
        print(f"✅ Completed sequence: {sequence}")
        print(f"📊 Quiz Score: {quiz_score}/100")
        print(f"📈 Overall Progress: {student.progress} sequences completed")
        
        # Check if course is completed
        sequences = self.course_graph.sequences.get(course_name, [])
        completed_count = sum(1 for seq in sequences 
                            if f"{course_name}_{seq}" in student.completed_sequences)
        
        if completed_count == len(sequences):
            student.complete_course(course_name)
            print(f"🎉 Congratulations! You have completed '{course_name}'!")
            
            # Recommend next course
            self.recommend_next_course(student)

    def recommend_next_course(self, student):
        """Recommend next course based on progress - O(n) time"""
        print("\n💡 COURSE RECOMMENDATIONS:")
        
        # Get available courses (not completed)
        available_courses = [course for course in self.course_graph.graph 
                           if course not in student.completed_courses and 
                           course != student.current_course]
        
        if not available_courses:
            print("🎓 You've completed all available courses! Well done!")
            return
            
        # Filter by prerequisites
        eligible_courses = []
        for course in available_courses:
            prerequisites = self.course_graph.find_all_prerequisites(course)
            if all(prereq in student.completed_courses for prereq in prerequisites):
                eligible_courses.append(course)
        
        if eligible_courses:
            print("Based on your progress, we recommend:")
            for i, course in enumerate(eligible_courses, 1):
                desc = self.course_graph.get_course_description(course)
                print(f"  {i}. {course} - {desc}")
            
            try:
                choice = input("\nWould you like to enroll in one of these? (yes/no): ").strip().lower()
                if choice == 'yes':
                    course_num = int(input(f"Enter course number (1-{len(eligible_courses)}): "))
                    if 1 <= course_num <= len(eligible_courses):
                        self.enroll_in_course(student, eligible_courses[course_num-1])
            except ValueError:
                print("❌ Invalid input.")
        else:
            print("Complete more prerequisites to unlock new courses!")

    def view_student_dashboard(self, student_id):
        """View comprehensive student dashboard - O(n) time"""
        student_data = self.student_map.retrieve_student_data(student_id)
        if not student_data:
            print("❌ Student not found.")
            return
            
        print(f"\n===== STUDENT DASHBOARD =====")
        print(f"👤 Name: {student_data['name']}")
        print(f"🎯 Learning Style: {student_data['learning_style']}")
        print(f"📊 Overall Progress: {student_data['progress']} sequences")
        print(f"📈 Average Score: {student_data['average_score']:.1f}%")
        
        if student_data['current_course']:
            print(f"📚 Current Course: {student_data['current_course']}")
        else:
            print(" Current Course: None")
            
        print(f"✅ Completed Courses: {', '.join(student_data['completed_courses']) or 'None'}")
        
        # Recent activity
        recent_activities = list(student_data['history'])[-3:]
        if recent_activities:
            print(f"\n🕒 Recent Activity:")
            for activity in recent_activities:
                print(f"  - {activity.activity_type}: {activity.metadata}")

    def admin_menu(self):
        """Admin menu interface - O(n) time for various operations"""
        while True:
            print("\n===== ADMIN MENU =====")
            print("1. Add New Course")
            print("2. Add Content to Course") 
            print("3. Change Course Priority")
            print("4. View System Statistics")
            print("5. View All Courses")
            print("6. View All Students")
            print("7. Back to Main Menu")
            
            choice = input("Enter your choice: ").strip()
            
            if choice == '1':
                self.add_course()
            elif choice == '2':
                self.add_content_to_course()
            elif choice == '3':
                self.change_course_priority()
            elif choice == '4':
                self.view_system_stats()
            elif choice == '5':
                self.view_all_courses()
            elif choice == '6':
                self.view_all_students()
            elif choice == '7':
                break
            else:
                print("❌ Invalid choice. Please try again.")

    def student_menu(self):
        """Student menu interface - O(n) time for various operations"""
        while True:
            print("\n===== STUDENT MENU =====")
            print("1. New Student Registration")
            print("2. Existing Student Login")
            print("3. Back to Main Menu")
            
            choice = input("Enter your choice: ").strip()
            
            if choice == '1':
                self.create_new_user()
            elif choice == '2':
                self.existing_student_login()
            elif choice == '3':
                break
            else:
                print("❌ Invalid choice. Please try again.")

    def existing_student_login(self):
        """Student login functionality - O(1) time"""
        student_id = input("Enter your Student ID: ").strip()
        student_data = self.student_map.retrieve_student_data(student_id)
        
        if student_data:
            print(f"\n✅ Welcome back, {student_data['name']}!")
            self.student_dashboard_menu(student_id)
        else:
            print("❌ Student ID not found. Please register first.")

    def student_dashboard_menu(self, student_id):
        """Student dashboard menu - O(n) time for various operations"""
        while True:
            print(f"\n===== STUDENT DASHBOARD =====")
            print("1. View My Profile")
            print("2. Search and Enroll in Courses")
            print("3. View My Recommendations")
            print("4. View My Learning Path")
            print("5. Complete Current Sequence")
            print("6. Logout")
            
            choice = input("Enter your choice: ").strip()
            
            if choice == '1':
                self.view_student_dashboard(student_id)
            elif choice == '2':
                student = self.student_map.student_map[student_id]
                self.enhanced_search_content(student)
            elif choice == '3':
                self.view_recommendations()
            elif choice == '4':
                self.view_learning_path(student_id)
            elif choice == '5':
                self.complete_current_sequence(student_id)
            elif choice == '6':
                print(" Logging out...")
                break
            else:
                print("❌ Invalid choice. Please try again.")

    def view_all_courses(self):
        """View all available courses - O(n) time"""
        print("\n===== ALL COURSES =====")
        for course in self.course_graph.graph:
            desc = self.course_graph.get_course_description(course)
            sequences = self.course_graph.sequences.get(course, [])
            print(f"📚 {course}")
            print(f"   Description: {desc}")
            print(f"   Sequences: {len(sequences)}")
            print(f"   Prerequisites: {self.course_graph.get_prerequisites(course)}")
            print()

    def view_all_students(self):
        """View all students - O(n) time"""
        print("\n===== ALL STUDENTS =====")
        students = self.student_map.get_all_students()
        for student in students:
            print(f"🎓 {student.name} (ID: {student.student_id})")
            print(f"   Current Course: {student.current_course}")
            print(f"   Completed Courses: {len(student.completed_courses)}")
            print(f"   Learning Style: {student.learning_style}")
            print()

    def view_recommendations(self):
        """View course recommendations - O(n) time"""
        print("\n===== COURSE RECOMMENDATIONS =====")
        recommendations = self.recommendation_heap.display()
        if not recommendations:
            print("No recommendations available yet. Complete some courses first!")

    def view_learning_path(self, student_id):
        """View student's learning path - O(V + E) time"""
        student = self.student_map.student_map.get(student_id)
        if not student:
            print("❌ Student not found.")
            return
            
        if student.current_course:
            path = self.course_graph.get_learning_path(student.current_course)
            print(f"\n Learning Path for {student.current_course}:")
            print(" → ".join(path))
        else:
            print("❌ You are not enrolled in any course.")

    def complete_current_sequence(self, student_id):
        """Complete current sequence for student - O(1) time"""
        student = self.student_map.student_map.get(student_id)
        if not student or not student.current_course:
            print("❌ You are not enrolled in any course.")
            return
            
        course_name = student.current_course
        sequences = self.course_graph.sequences.get(course_name, [])
        
        if not sequences:
            print("❌ No sequences available for this course.")
            return
            
        # Find next incomplete sequence
        completed_sequences = [seq.split('_')[1] for seq in student.completed_sequences 
                             if seq.startswith(course_name)]
        
        for sequence in sequences:
            if sequence not in completed_sequences:
                self.complete_sequence(student, course_name, sequence)
                return
                
        print("✅ You have completed all sequences in this course!")

    def run(self):
        """Main application loop - O(n) time for initialization"""
        print("🚀 Initializing Learning Management System...")
        
        # Initialize with sample data
        self.initialize_courses_with_schedule()
        self.initialize_students_with_current_courses()
        
        print("\n" + "="*50)
        print("🎓 WELCOME TO SMART LEARNING MANAGEMENT SYSTEM")
        print("="*50)
        
        while True:
            print("\n===== MAIN MENU =====")
            print("1. Admin Portal")
            print("2. Student Portal") 
            print("3. View System Overview")
            print("4. Exit")
            
            choice = input("Enter your choice: ").strip()
            
            if choice == '1':
                self.admin_menu()
            elif choice == '2':
                self.student_menu()
            elif choice == '3':
                self.view_system_overview()
            elif choice == '4':
                print("👋 Thank you !!!! Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please try again.")

    def view_system_overview(self):
        """Enhanced system overview - O(n) time"""
        print("\n===== SYSTEM OVERVIEW =====")
        
        # Course information
        print(f"\n📚 COURSES ({len(self.course_graph.graph)} total):")
        for course in self.course_graph.graph:
            students_in_course = len(self.student_map.get_students_by_course(course))
            print(f"  - {course}: {students_in_course} students enrolled")
        
        # Student statistics
        students = self.student_map.get_all_students()
        print(f"\n👥 STUDENTS ({len(students)} total):")
        avg_progress = sum(student.progress for student in students) / len(students) if students else 0
        print(f"  - Average Progress: {avg_progress:.1f} sequences")
        
        # Learning styles distribution
        styles = {}
        for student in students:
            styles[student.learning_style] = styles.get(student.learning_style, 0) + 1
        
        print(f"  - Learning Styles:")
        for style, count in styles.items():
            print(f"    * {style}: {count} students")
        
        # Popular courses
        popular = self.recommendation_heap.get_popular_courses(3)
        if popular:
            print(f"\n🏆 POPULAR COURSES:")
            for course, count in popular:
                print(f"  - {course}: {count} recommendations")

# Run the application
if __name__ == "__main__":
    lms = LearningManagementSystem()
    lms.run()