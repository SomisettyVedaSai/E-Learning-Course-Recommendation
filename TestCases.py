"""
TestCases.py - Comprehensive test cases demonstrating key functionalities of the Learning Management System.
These test cases showcase the integration of all ADTs and their real-world applications.

Each test case includes:
1. Objective - What we're testing
2. Approach - How we test it
3. Expected Output - What should happen
4. Importance - Why this matters for the system
"""

import random
from datetime import datetime, timedelta
from ContentTrie import ContentTrie
from CourseGraph import CourseGraph
from StudentHashMap import StudentHashMap, Student
from RecommadationHeap import RecommadationHeap
from SequenceQueue import SequenceQueue

class LMSTestCases:
    def __init__(self):
        """Initialize all ADTs for testing"""
        self.course_graph = CourseGraph()
        self.content_trie = ContentTrie()
        self.student_map = StudentHashMap()
        self.recommendation_heap = RecommadationHeap()
        self.schedule_queue = SequenceQueue()
        
    def setup_test_data(self):
        """Setup common test data for all test cases"""
        # Setup courses
        courses = {
            "Data Structures": {
                "content": ["Arrays", "Linked Lists", "Stacks", "Queues", "Trees"],
                "prereqs": [],
                "sequences": [("Arrays Basics", timedelta(days=1)), 
                            ("Linked Lists", timedelta(days=2))]
            },
            "Algorithms": {
                "content": ["Sorting", "Searching", "Graph Algorithms"],
                "prereqs": ["Data Structures"],
                "sequences": [("Sorting Techniques", timedelta(days=2))]
            },
            "Database Systems": {
                "content": ["SQL", "Normalization", "Transactions"],
                "prereqs": ["Data Structures"],
                "sequences": [("SQL Basics", timedelta(days=3))]
            }
        }
        
        for course_name, details in courses.items():
            self.course_graph.add_module(course_name, [seq[0] for seq in details["sequences"]])
            for content in details["content"]:
                self.content_trie.insertContent(content)
                self.course_graph.add_content(course_name, content)
            for prereq in details["prereqs"]:
                self.course_graph.add_prerequisite(prereq, course_name)
            for sequence, duration in details["sequences"]:
                self.schedule_queue.schedule_course(sequence, duration, 1)
        
        # Setup students
        students = [
            Student("S001", "Alice Johnson", 20, "Female"),
            Student("S002", "Bob Smith", 22, "Male"),
            Student("S003", "Carol Davis", 21, "Female")
        ]
        
        for student in students:
            self.student_map.insert_student(student)

    def test_case_1_prerequisite_validation(self):
        """
        TEST CASE 1: Prerequisite Validation and Learning Path Generation
        
        Objective: Test if the system correctly validates prerequisites and generates 
                   optimal learning paths for students.
        
        Importance: Ensures students cannot skip foundational courses and follow 
                   a structured learning progression.
        
        Approach:
        1. Create courses with prerequisites
        2. Attempt to enroll students without completing prerequisites
        3. Generate learning paths
        4. Verify path correctness
        """
        print("=" * 70)
        print("TEST CASE 1: Prerequisite Validation and Learning Path Generation")
        print("=" * 70)
        
        # Setup
        self.setup_test_data()
        student = self.student_map.student_map["S001"]
        
        print("\n Available Courses:")
        for course in self.course_graph.graph:
            prereqs = self.course_graph.get_prerequisites(course)
            print(f"   - {course}: Prerequisites = {prereqs}")
        
        print(f"\n Student: {student.name}")
        print("   Completed Courses: None")
        
        # Test 1: Try to enroll in Algorithms without prerequisites
        print("\n Test 1: Enrolling in 'Algorithms' without prerequisites...")
        algorithms_prereqs = self.course_graph.find_all_prerequisites("Algorithms")
        can_enroll = self.course_graph.can_access_module("Algorithms", student.completed_courses)
        
        print(f"   Required: {algorithms_prereqs}")
        print(f"   Completed: {student.completed_courses}")
        print(f"   Can Enroll: {can_enroll}")
        
        # Test 2: Generate learning path
        print("\n Test 2: Generating Learning Path for 'Algorithms'...")
        learning_path = self.course_graph.get_learning_path("Algorithms")
        print(f"   Optimal Learning Path: {' → '.join(learning_path)}")
        
        # Test 3: Complete prerequisites and try again
        print("\n Test 3: Completing prerequisites and re-checking...")
        student.completed_courses.add("Data Structures")
        can_enroll_after = self.course_graph.can_access_module("Algorithms", student.completed_courses)
        print(f"   Completed Courses: {student.completed_courses}")
        print(f"   Can Enroll Now: {can_enroll_after}")
        
        # Verification
        assert not can_enroll, "❌ TEST FAILED: Should not allow enrollment without prerequisites"
        assert can_enroll_after, "❌ TEST FAILED: Should allow enrollment after completing prerequisites"
        assert "Data Structures" in learning_path, "❌ TEST FAILED: Learning path should include prerequisites"
        
        print(" TEST CASE 1 PASSED: Prerequisite validation working correctly!")
        return True

    def test_case_2_content_search_and_autocomplete(self):
        """
        TEST CASE 2: Content Search and Autocomplete Functionality
        
        Objective: Test the efficiency of content search using Trie data structure
                   and autocomplete suggestions.
        
        Importance: Demonstrates fast search capabilities crucial for user experience
                   in finding relevant course content.
        
        Approach:
        1. Insert multiple content items
        2. Test prefix-based search
        3. Test exact search
        4. Measure search performance
        """
        print("\n" + "=" * 70)
        print("TEST CASE 2: Content Search and Autocomplete Functionality")
        print("=" * 70)
        
        # Setup
        self.setup_test_data()
        
        # Test data
        test_prefixes = ["Arr", "Link", "Sort", "Data", "Graph"]
        
        print("\n Testing Autocomplete with Various Prefixes:")
        for prefix in test_prefixes:
            results = self.content_trie.autocomplete(prefix)
            print(f"   Prefix '{prefix}': {results}")
        
        # Test exact search
        print("\n Testing Exact Content Search:")
        exact_searches = ["Arrays", "Linked Lists", "NonExistent"]
        for search_term in exact_searches:
            # Since we don't have exact search, we'll check if it's in autocomplete results
            results = self.content_trie.autocomplete(search_term)
            found = any(search_term == result for result in results)
            print(f"   Search '{search_term}': {'Found' if found else 'Not Found'}")
        
        # Test performance with multiple searches
        print("\n Testing Search Performance:")
        import time
        start_time = time.time()
        
        # Perform multiple searches
        for _ in range(100):
            self.content_trie.autocomplete("Arr")
            self.content_trie.autocomplete("Lin")
            self.content_trie.autocomplete("Sort")
        
        end_time = time.time()
        print(f"   Time for 300 searches: {(end_time - start_time)*1000:.2f} ms")
        
        # Verification
        arr_results = self.content_trie.autocomplete("Arr")
        assert "Arrays" in arr_results, "❌ TEST FAILED: 'Arrays' should be found with prefix 'Arr'"
        
        link_results = self.content_trie.autocomplete("Lin")
        assert "Linked Lists" in link_results, "❌ TEST FAILED: 'Linked Lists' should be found with prefix 'Lin'"
        
        print(" TEST CASE 2 PASSED: Content search and autocomplete working efficiently!")
        return True

    def test_case_3_recommendation_system(self):
        """
        TEST CASE 3: Intelligent Course Recommendation System
        
        Objective: Test the recommendation heap's ability to suggest relevant courses
                   based on student progress and popularity.
        
        Importance: Demonstrates personalized learning experience and adaptive
                   course suggestions.
        
        Approach:
        1. Simulate student progress
        2. Add recommendations to heap
        3. Test priority-based recommendations
        4. Test popularity tracking
        """
        print("\n" + "=" * 70)
        print("TEST CASE 3: Intelligent Course Recommendation System")
        print("=" * 70)
        
        # Setup
        self.setup_test_data()
        student = self.student_map.student_map["S002"]
        
        print(f"\n Student: {student.name}")
        print(f"   Initial Progress: {student.progress}")
        
        # Simulate student completing sequences
        print("\n Simulating Student Progress...")
        courses_progress = {
            "Data Structures": 3,
            "Algorithms": 1,
            "Database Systems": 2
        }
        
        for course, progress in courses_progress.items():
            for i in range(progress):
                self.recommendation_heap.insert_recommendation(course, i + 1)
                student.update_progress(course, f"Sequence_{i+1}", random.randint(70, 95))
        
        print(f"   Final Progress: {student.progress} sequences completed")
        
        # Display recommendations
        print("\n Current Recommendations:")
        recommendations = self.recommendation_heap.display()
        
        # Test priority-based recommendations
        print("\n Testing Priority-based Filtering:")
        target_progress = 2
        filtered_recs = self.recommendation_heap.get_recommendations_for_progress(target_progress)
        print(f"   Recommendations for progress ≥ {target_progress}: {filtered_recs}")
        
        # Test popularity tracking
        print("\n Testing Popularity Tracking:")
        popular_courses = self.recommendation_heap.get_popular_courses(2)
        print(f"   Most Popular Courses: {popular_courses}")
        
        # Verification
        assert self.recommendation_heap.size() > 0, "❌ TEST FAILED: Should have recommendations"
        assert len(popular_courses) > 0, "❌ TEST FAILED: Should track popular courses"
        
        print(" TEST CASE 3 PASSED: Recommendation system working intelligently!")
        return True

    def test_case_4_student_progress_tracking(self):
        """
        TEST CASE 4: Comprehensive Student Progress Tracking
        
        Objective: Test the student history array and progress tracking across
                   multiple courses and sequences.
        
        Importance: Demonstrates complete learning journey tracking and
                   performance analytics.
        
        Approach:
        1. Simulate multiple learning activities
        2. Test history storage and retrieval
        3. Test progress calculations
        4. Test analytics features
        """
        print("\n" + "=" * 70)
        print("TEST CASE 4: Comprehensive Student Progress Tracking")
        print("=" * 70)
        
        # Setup
        self.setup_test_data()
        student = self.student_map.student_map["S003"]
        
        print(f"\n🎓 Student: {student.name}")
        print(f"   Initial Stats:")
        print(f"   - Progress: {student.progress}")
        print(f"   - Completed Courses: {len(student.completed_courses)}")
        print(f"   - History Items: {len(student.history.activities)}")
        
        # Simulate intensive learning session
        print("\n Simulating Learning Activities...")
        
        # Complete Data Structures course
        sequences_ds = ["Arrays_Basics", "Linked_Lists_Intro", "Stack_Operations"]
        for seq in sequences_ds:
            score = random.randint(75, 95)
            student.update_progress("Data Structures", seq, score)
            print(f"   Completed: Data Structures - {seq} (Score: {score})")
        
        student.complete_course("Data Structures")
        
        # Complete partial Algorithms course
        sequences_algo = ["Sorting_Basics", "Searching_Algorithms"]
        for seq in sequences_algo:
            score = random.randint(80, 98)
            student.update_progress("Algorithms", seq, score)
            print(f"   Completed: Algorithms - {seq} (Score: {score})")
        
        # Display comprehensive progress
        print(f"\n Final Student Statistics:")
        student_data = self.student_map.retrieve_student_data("S003")
        print(f"   - Total Progress: {student_data['progress']} sequences")
        print(f"   - Completed Courses: {student_data['completed_courses']}")
        print(f"   - Average Score: {student_data['average_score']:.1f}%")
        print(f"   - Total History Items: {len(student_data['history'])}")
        
        # Test history features
        print(f"\n Recent Activities:")
        recent = student.history.get_recent_activities(3)
        for i, activity in enumerate(recent, 1):
            print(f"   {i}. {activity.activity_type}: {activity.metadata}")
        
        # Verification
        assert student.progress == 5, f"❌ TEST FAILED: Expected 5 progress, got {student.progress}"
        assert "Data Structures" in student.completed_courses, "❌ TEST FAILED: Should have completed Data Structures"
        assert len(student.history.activities) >= 5, "❌ TEST FAILED: Should have sufficient history"
        
        print(" TEST CASE 4 PASSED: Student progress tracking comprehensive and accurate!")
        return True

    def test_case_5_course_scheduling_system(self):
        """
        TEST CASE 5: Dynamic Course Scheduling and Priority Management
        
        Objective: Test the sequence queue's ability to manage course schedules,
                   handle priorities, and estimate completion times.
        
        Importance: Demonstrates efficient resource allocation and timeline
                   management for learning paths.
        
        Approach:
        1. Schedule multiple courses with different priorities
        2. Test queue operations
        3. Test priority updates
        4. Test timeline estimation
        """
        print("\n" + "=" * 70)
        print("TEST CASE 5: Dynamic Course Scheduling and Priority Management")
        print("=" * 70)
        
        # Setup fresh schedule
        self.schedule_queue = SequenceQueue()
        
        print("\n Initial Schedule Setup:")
        courses_schedule = [
            ("Data Structures", timedelta(days=5), 1),   # High priority
            ("Algorithms", timedelta(days=7), 2),        # Medium priority
            ("Database Systems", timedelta(days=4), 3),  # Low priority
            ("Web Development", timedelta(days=6), 2),   # Medium priority
        ]
        
        for course, duration, priority in courses_schedule:
            self.schedule_queue.schedule_course(course, duration, priority)
        
        print(f"   Scheduled {len(courses_schedule)} courses")
        print(f"   Queue Size: {self.schedule_queue.get_queue_size()}")
        
        # Display current schedule
        print("\n Current Schedule:")
        self.schedule_queue.display()
        
        # Test priority update
        print("\n Testing Priority Update:")
        print("   Changing 'Database Systems' priority from 3 to 1...")
        self.schedule_queue.update_priority("Database Systems", 1)
        
        print("\n Updated Schedule (after priority change):")
        self.schedule_queue.display()
        
        # Test completion estimation
        print("\n Testing Completion Time Estimation:")
        total_duration = self.schedule_queue.estimate_completion_time()
        print(f"   Estimated Total Completion Time: {total_duration}")
        
        # Test sequence processing
        print("\n Testing Sequence Processing:")
        completed_courses = set()
        while not self.schedule_queue.is_empty():
            next_course = self.schedule_queue.dequeue()
            completed_courses.add(next_course[0])
            print(f"   Completed: {next_course[0]} (Priority: {next_course[1]})")
            if len(completed_courses) >= 2:  # Process only 2 for demo
                break
        
        # Test clearing completed courses
        print(f"\n Clearing completed courses: {completed_courses}")
        self.schedule_queue.clear_completed_courses(completed_courses)
        print(f"   Remaining in queue: {self.schedule_queue.get_queue_size()}")
        
        # Verification
        assert self.schedule_queue.get_queue_size() > 0, "❌ TEST FAILED: Should have remaining courses"
    
        print(" TEST CASE 5 PASSED: Course scheduling system working dynamically!")
        return True

    def run_all_test_cases(self):
        """Run all test cases and provide summary"""
        print(" STARTING LEARNING MANAGEMENT SYSTEM TEST SUITE")
        print("=" * 70)
        
        test_results = []
        
        try:
            test_results.append(("Prerequisite Validation", self.test_case_1_prerequisite_validation()))
        except Exception as e:
            print(f"❌ Test Case 1 Failed: {e}")
            test_results.append(("Prerequisite Validation", False))
        
        try:
            test_results.append(("Content Search", self.test_case_2_content_search_and_autocomplete()))
        except Exception as e:
            print(f"❌ Test Case 2 Failed: {e}")
            test_results.append(("Content Search", False))
        
        try:
            test_results.append(("Recommendation System", self.test_case_3_recommendation_system()))
        except Exception as e:
            print(f"❌ Test Case 3 Failed: {e}")
            test_results.append(("Recommendation System", False))
        
        try:
            test_results.append(("Progress Tracking", self.test_case_4_student_progress_tracking()))
        except Exception as e:
            print(f"❌ Test Case 4 Failed: {e}")
            test_results.append(("Progress Tracking", False))
        
        try:
            test_results.append(("Course Scheduling", self.test_case_5_course_scheduling_system()))
        except Exception as e:
            print(f"❌ Test Case 5 Failed: {e}")
            test_results.append(("Course Scheduling", False))
        
        # Print summary
        print("\n" + "=" * 70)
        print(" TEST SUITE SUMMARY")
        print("=" * 70)
        
        passed = 0
        for test_name, result in test_results:
            status = "✅ PASSED" if result else "❌ FAILED"
            print(f"   {test_name}: {status}")
            if result:
                passed += 1
        
        print(f"\n Overall Result: {passed}/{len(test_results)} tests passed")
        
        if passed == len(test_results):
            print(" ALL TEST CASES PASSED! System is functioning correctly.")
        else:
            print("  Some tests failed. Please check the implementation.")
        
        return passed == len(test_results)

def demonstration_mode():
    """Run a comprehensive demonstration for faculty"""
    print(" LEARNING MANAGEMENT SYSTEM - FACULTY DEMONSTRATION")
    print("=" * 70)
    print("This demonstration showcases 5 key test cases that highlight:")
    print("1. Prerequisite validation and learning path generation")
    print("2. Efficient content search using Trie data structure") 
    print("3. Intelligent course recommendations based on progress")
    print("4. Comprehensive student progress tracking and analytics")
    print("5. Dynamic course scheduling with priority management")
    print("=" * 70)
    
    input("\nPress Enter to start the demonstration...")
    
    # Run test cases
    test_suite = LMSTestCases()
    success = test_suite.run_all_test_cases()
    
    if success:
        print("\n" + "=" * 70)
        print(" DEMONSTRATION COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print("Key System Features Demonstrated:")
        print("• Robust prerequisite enforcement")
        print("• Fast content search (O(m) time complexity)")
        print("• Personalized course recommendations") 
        print("• Comprehensive progress analytics")
        print("• Efficient scheduling algorithms")
        print("• Integration of 6 different ADTs working together")
    else:
        print("\n  Demonstration completed with some issues.")

if __name__ == "__main__":
    demonstration_mode()