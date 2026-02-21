# 🎓 E-Learning & Course Recommendation

A Data Structures based adaptive Learning Management System (LMS) built in Python that intelligently manages courses, student progress, prerequisites, content search, and personalized course recommendations.

---

## 📌 Project Overview

**E-Learning & Course Recommendation** is a console-based academic project that demonstrates the practical integration of multiple core Data Structures into a real-world learning platform.

The system allows:

- Course prerequisite validation
- Intelligent content search
- Personalized course recommendations
- Student progress tracking
- Learning path generation
- Dynamic course scheduling
- Activity history monitoring

This project highlights how fundamental Data Structures can power a scalable educational system.

---

## 🧠 Core Data Structures Used

| Data Structure | File | Purpose |
|---------------|------|----------|
| Trie | `ContentTrie.py` | Fast keyword-based content search |
| Graph | `CourseGraph.py` | Course prerequisite management |
| HashMap | `StudentHashMap.py` | Efficient student record storage |
| Dynamic Array | `StudentHistoryArray.py` | Student activity tracking |
| Min-Heap | `RecommadationHeap.py` | Priority-based course recommendation |
| Queue | `SequenceQueue.py` | Course sequence scheduling |

---

## 🚀 Key Features

### 👨‍🎓 Student Features
- Student registration & login
- Learning style preference selection
- Course enrollment with prerequisite validation
- Automatic learning path generation
- Quiz score tracking
- Progress analytics dashboard
- Personalized course recommendations

### 👨‍💼 Admin Features
- Add new courses
- Add content to courses
- Manage course priorities
- View system statistics
- Monitor student data

### 🔎 Smart Search
- Prefix-based autocomplete using Trie
- Efficient content lookup in **O(m)** time

### 🎯 Intelligent Recommendation System
- Uses Min-Heap
- Recommends courses based on:
  - Progress
  - Completion history
  - Popularity trends

---

## 🏗️ Project Structure

```
E-Learning-Course-Recommendation/
│
├── ContentTrie.py
├── CourseGraph.py
├── StudentHashMap.py
├── StudentHistoryArray.py
├── SequenceQueue.py
├── RecommadationHeap.py
├── Main.py
├── TestCases.py
│
├── README.md
└── .gitignore
```

---

## ▶️ How to Run the Project

### 1️⃣ Clone the Repository

```
git clone https://github.com/your-username/E-Learning-Course-Recommendation.git
```

### 2️⃣ Navigate into the Folder

```
cd E-Learning-Course-Recommendation
```

### 3️⃣ Run the Application

```
python Main.py
```

---

## 🧪 Run Test Suite (Faculty Demonstration Mode)

```
python TestCases.py
```

The test suite demonstrates:

1. Prerequisite validation
2. Learning path generation
3. Trie-based search efficiency
4. Recommendation engine intelligence
5. Progress tracking analytics
6. Scheduling system functionality

---

## ⏱️ Time Complexity Highlights

| Operation | Complexity |
|-----------|------------|
| Student Insert | O(1) |
| Student Retrieval | O(1) |
| Trie Search | O(m) |
| Graph Traversal | O(V + E) |
| Heap Insert | O(log n) |
| Queue Operations | O(1) |

---

##  Learning Outcomes

This project demonstrates:

- Practical application of Data Structures
- System design using modular architecture
- Algorithm optimization techniques
- Efficient time and space complexity management
- Real-world integration of multiple ADTs

---

##  Why This Project is Strong

- Integrates 6+ Data Structures in one system
- Demonstrates algorithmic thinking

---

## Technologies Used

- Python 3.x
- Standard Library Modules
- OOP Concepts
- Algorithm Design

---

##  Author

Somisetty Veda Sai
Computer Science Engineering   
Data Structures Algorithm Project  

---

## 📜 License

This project is created for academic and educational purposes.
