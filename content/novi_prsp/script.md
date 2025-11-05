---
nav_exclude: true
---


### **Course: Programming for Solving Complex Problems**

#### **Course Overview**

This course provides a thorough introduction to competitive programming, focusing on the design and implementation of efficient and correct algorithms for complex problems. Students will learn to analyze problems, identify appropriate algorithmic techniques, implement solutions in C++, and test them in a competitive setting. The curriculum draws heavily from foundational algorithm theory and practical problem-solving heuristics. The goal is not just to prepare students for programming contests like the ICPC or IOI, but to significantly strengthen their general problem-solving, algorithm design, and coding skills, which are invaluable for software engineering and computer science research.

#### **Course Methodology**

*   **Lectures:** Weekly lectures will introduce the theoretical underpinnings of each topic, drawing from "Introduction to Algorithms" for rigor and depth.
*   **Problem-Solving Sessions:** Practical examples and strategies will be demonstrated, primarily using patterns from the "Competitive Programmer's Handbook."
*   **Problem Sets:** Weekly problem sets will feature problems from online judges (such as Codeforces, TopCoder, USACO) that require the implementation of the week's topics.
*   **Contests:** Several timed online contests will be held throughout the semester to simulate a competitive environment and assess practical skills.

#### **Required Texts**
1.  *Introduction to Algorithms, Third Edition* by Cormen, Leiserson, Rivest, and Stein (CLRS).
2.  *Competitive Programmer's Handbook* by Antti Laaksonen (CPH).

---

### **Semester Curriculum (15 Weeks)**

**Part I: Core Techniques and Paradigms (Weeks 1-7)**

This part establishes the foundation for competitive programming.

*   **Week 1: Introduction to Competitive Programming & C++ Essentials**
    *   **Topics:** What is competitive programming? The structure of a contest. Setting up an efficient C++ environment. Fast I/O. Essential C++ STL components: `vector`, `string`, `pair`, `tuple`. Using macros and `typedef` for speed.
    *   **Reading:** CPH Chapters 1 & 4. CLRS Chapter 10.

*   **Week 2: Time Complexity Analysis and Sorting**
    *   **Topics:** Big O notation. Calculating time complexity from loops and recursion. Identifying complexity classes (logarithmic, linear, polynomial, exponential). Sorting theory: O(n²) sorts (Bubble, Insertion) vs. O(n log n) sorts (Merge Sort, Quicksort). Lower bound for comparison sorting. Practical application: `std::sort` with custom comparators.
    *   **Reading:** CPH Chapters 2 & 3. CLRS Chapters 2, 3, 7, & 8.

*   **Week 3: Complete Search and Backtracking**
    *   **Topics:** Brute-force approaches. Generating all subsets (recursion and bit manipulation). Generating all permutations. The backtracking paradigm for systematically exploring search spaces (e.g., N-Queens). Pruning the search space to optimize.
    *   **Reading:** CPH Chapter 5. CLRS doesn't have a dedicated chapter, but the concepts are fundamental.

*   **Week 4: Greedy Algorithms**
    *   **Topics:** The greedy-choice property. Optimal substructure in greedy algorithms. Classic problems: Activity Selection (scheduling), Coin Problem (change-making), Huffman Codes. Proving the correctness of a greedy strategy.
    *   **Reading:** CPH Chapter 6. CLRS Chapter 16.

*   **Week 5: Divide and Conquer & Binary Search**
    *   **Topics:** The divide-and-conquer paradigm revisited. Classic problems: Maximum Subarray Sum. Binary search as a divide-and-conquer technique. Applying binary search on the answer/monotonic functions.
    *   **Reading:** CPH Chapter 3. CLRS Chapter 4.

*   **Week 6: Introduction to Dynamic Programming**
    *   **Topics:** The core principles of DP: optimal substructure and overlapping subproblems. Memoization (top-down) vs. Tabulation (bottom-up). State representation. Classic 1D DP problems: Fibonacci, Coin Problem, Longest Increasing Subsequence, Edit Distance.
    *   **Reading:** CPH Chapter 7. CLRS Chapter 15.

*   **Week 7: Advanced Dynamic Programming Techniques**
    *   **Topics:** DP on grids (paths and tilings). DP on subsets (bitmask DP). Introduction to DP on trees. The Knapsack problem family (0-1 and unbounded).
    *   **Reading:** CPH Chapter 7 & 10. CLRS Chapter 16.

**Part II: Graph Algorithms (Weeks 8-11)**

Graphs are a cornerstone of competitive programming problems.

*   **Week 8: Graph Representation and Traversal**
    *   **Topics:** Graph terminology. Representations: Adjacency List, Adjacency Matrix, Edge List. Breadth-First Search (BFS) and its applications (shortest path in unweighted graphs). Depth-First Search (DFS) and its applications (cycle detection, topological sorting).
    *   **Reading:** CPH Chapters 11 & 12. CLRS Chapter 22.

*   **Week 9: Shortest Path Algorithms**
    *   **Topics:** Properties of shortest paths. Dijkstra's algorithm for non-negative weights (implementation with priority queue). Bellman-Ford algorithm for graphs with negative weights (and negative cycle detection).
    *   **Reading:** CPH Chapter 13. CLRS Chapter 24.

*   **Week 10: All-Pairs Shortest Paths and Minimum Spanning Trees (MST)**
    *   **Topics:** Floyd-Warshall algorithm for all-pairs shortest paths. The MST problem. Prim's algorithm. Kruskal's algorithm and its reliance on the Union-Find data structure.
    *   **Reading:** CPH Chapters 13 & 15. CLRS Chapters 23 & 25.

*   **Week 11: Flows, Matchings, and Strong Connectivity**
    *   **Topics:** Maximum Flow (Ford-Fulkerson method). Max-Flow Min-Cut Theorem. Maximum Bipartite Matching. Strongly Connected Components (Kosaraju's algorithm or Tarjan's algorithm).
    *   **Reading:** CPH Chapters 17 & 20. CLRS Chapters 22.5 & 26.

**Part III: Advanced & Specialized Topics (Weeks 12-15)**

This section covers topics that frequently appear in harder contest problems.

*   **Week 12: Data Structures for Range Queries**
    *   **Topics:** Static array queries (prefix sums). Dynamic queries: Fenwick Tree (Binary Indexed Tree) for sum queries. Segment Tree for sum, min/max, and other range queries.
    *   **Reading:** CPH Chapter 9. CLRS Chapter 14 (as a basis for augmenting data structures).

*   **Week 13: Number Theory and Combinatorics**
    *   **Topics:** Prime numbers (Sieve of Eratosthenes). GCD (Euclid's algorithm). Modular arithmetic, modular inverse, and modular exponentiation. Binomial coefficients and combinatorics.
    *   **Reading:** CPH Chapters 21 & 22. CLRS Chapter 31.

*   **Week 14: String Algorithms and Computational Geometry**
    *   **Topics:** String hashing (Rabin-Karp). Knuth-Morris-Pratt (KMP) algorithm. Trie data structure. Basic geometric primitives (cross product, orientation). Convex Hull (Graham Scan).
    *   **Reading:** CPH Chapters 26, 29, & 30. CLRS Chapters 32 & 33.

*   **Week 15: Final Review and Contest Strategy**
    *   **Topics:** Review of all major algorithmic paradigms and data structures. Discussion of problem-solving strategies in a contest setting: choosing which problem to solve, debugging, and time management. Final practice session.

---
This curriculum provides a balanced mix of fundamental theory and practical application, preparing students not only for the challenges of competitive programming but also for advanced coursework and technical interviews.