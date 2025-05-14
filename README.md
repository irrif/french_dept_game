# 🗺️ Learn the French Departments – An Interactive App

## 🎯 Objective

This project aims to make learning the **French departments** both **fun and interactive**. Through a dynamic and user-friendly interface, users can explore the map of France, take quizzes, and discover key information about each department.

## 🛠️ Technologies Used

- **Python** – main programming language
- **Dash** – Python framework for building interactive web applications
- **GeoJSON** – for rendering geographic data (department shapes on the map)

## 🌍 Key Features

- Interactive map of France displaying all departments
- Game to test geography knowledge

## 📦 Installation

### Prerequisites

- Python 3.9 or higher
- `conda` (Anaconda package manager)

### Steps

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/project-name.git
   cd project-name

2. Create virtual environment:
   ```bash
   conda env create -n dept_game --file environment.yaml

3. Activate virtual environment:
   ```bash
   conda activate dept_game

4. Run the app
   ```bash
   python game.py

5. Open your browser and go to `http://127.0.0.1:8050`

## 🧩 Future Improvements / Roadmap

Here are some planned features and enhancements to make the app even more engaging:

- 🎨 Color selected departments: Visually highlight departments that have already been chosen during gameplay.
- ❌ Wrong attempt feedback: After up to 3 incorrect guesses per department, highlight the area in red to indicate a failed attempt.
- 🔄 Add a reset or replay button for new quiz rounds.
- 🧠 Improve quiz logic with different modes (timed quiz, multiple choice, etc.).
- 🌐 Add support for English/French language toggle.
- 📊 Add user performance statistics (score, success rate, etc.).
