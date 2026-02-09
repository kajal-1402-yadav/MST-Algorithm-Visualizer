# MST Algorithm Visualizer (Prim’s & Kruskal’s)

A Python-based GUI application to **visualize Minimum Spanning Tree (MST) algorithms** using **Prim’s** and **Kruskal’s** approaches.  
The project provides an **interactive step-by-step visualization** of how MSTs are constructed using greedy algorithms.

---

## 📌 Features

- Interactive **graph creation**
  - Add custom vertices and weighted edges
  - Generate random graphs
- Visualization of:
  - **Prim’s Algorithm**
  - **Kruskal’s Algorithm**
- Step-by-step execution:
  - Play / Pause animation
  - Next and Previous step navigation
- Real-time display of:
  - Selected edges
  - Current MST cost
- Clear visual distinction:
  - MST edges (Green)
  - Examining edges (Yellow)
  - Non-selected edges (Gray)

---

## 🧠 Algorithms Used

### 1. Prim’s Algorithm
- Greedy algorithm
- Starts from an initial vertex
- Expands the tree by selecting the minimum weight edge connecting a visited vertex to an unvisited vertex
- **Works correctly only for connected graphs**

### 2. Kruskal’s Algorithm
- Greedy algorithm
- Sorts all edges by weight
- Adds edges one by one while avoiding cycles
- Cycle detection is implemented using **DFS**
- **For disconnected graphs, it produces a Minimum Spanning Forest (MSF)**

---

## ⚠️ Important Note on Disconnected Graphs

- A **Minimum Spanning Tree (MST)** exists **only for connected graphs**
- If the graph is **disconnected**:
  - Kruskal’s algorithm generates a **Minimum Spanning Forest (MSF)**
  - The displayed cost represents the **total cost of all trees in the forest**
- This behavior follows standard graph theory definitions

---

## 🖥️ User Interface Overview

- **Left Panel**
  - Graph visualization canvas
  - MST cost display
- **Right Panel**
  - Graph controls (add vertices, edges, random graph)
  - Algorithm controls (play, pause, step navigation)
  - Legend for edge colors

---

## 🛠️ Technologies Used

- **Python 3**
- **Tkinter** – GUI development
- **Math & Random libraries** – node placement and graph generation

---

