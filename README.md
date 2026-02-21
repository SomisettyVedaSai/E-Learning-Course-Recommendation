# LMS-ADT-CaseStudy

A small Learning Management System (LMS) case study implemented using custom ADTs (Trie, Graph, Heap, Queue, HashMap, Dynamic Array) in Python. The project demonstrates how core data structures can be combined to build features like course dependency management, content search/autocomplete, scheduling, recommendation, and student progress tracking.

## Features

- Course dependency graph with topological sorting and prerequisite checks
- Content Trie for fast prefix-based search / autocomplete
- Recommendation heap for priority-based course suggestions and popularity tracking
- Sequence queue for course scheduling and priority management
- Student hash map and history array for tracking student progress and activities
- A `Main.py` integrating these ADTs into a simple CLI-style LMS

## Project structure

- `ContentTrie.py` - Trie implementation for course content and autocomplete
- `CourseGraph.py` - Directed graph for courses and prerequisites
- `RecommadationHeap.py` - Heap for course recommendations and popularity
- `SequenceQueue.py` - Circular queue for scheduling sequences
- `StudentHashMap.py` - Hash map and `Student` model
- `StudentHistoryArray.py` - Activity history storage for students
- `Main.py` - Integrates components into an interactive CLI-style system
- `TestCases.py` - Example test cases demonstrating functionality

## Requirements

- Python 3.8+

## Quick start

1. Create a virtual environment and activate it:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1   # PowerShell on Windows
```

2. Run the tests / example flows:

```powershell
python "Case Study/TestCases.py"
# or run the interactive main
python "Case Study/Main.py"
```

Note: The project uses only the Python standard library.

## License

This project has no license specified. Add a LICENSE file if you wish to publish it.

--
Generated README for the LMS ADT Case Study
