# Project Description: Chess Dashboard Visualization

## Overview
The Chess Dashboard Visualization project aims to create an interactive and dynamic dashboard that visualizes chess game data retrieved from the Chess.com API. This project utilizes a robust architecture with Python for data retrieval and preprocessing, MongoDB atlas for efficient data storage, Tableau for advanced visualization, Docker for containerization, and Git for version control.

# Demo
(tableau/chess_project_rapid.pdf)

## Objectives
- **Data Retrieval**: Fetch real-time chess game data from the Chess.com API, including player statistics, match history, and performance metrics.
- **Data Preprocessing**: Implement data cleaning and transformation using Python to ensure the data is structured and suitable for analysis.
- **Database Storage**: Store processed data in MongoDB to enable efficient querying and retrieval of both historical and real-time data.
- **Interactive Dashboard**: Develop a live connection to Tableau to create an interactive dashboard that allows users to visualize and explore chess data through various metrics, filters, and visualizations.
- **Containerization**: Utilize Docker to package the application and its dependencies, ensuring consistent deployment across different environments.
- **Version Control**: Use Git for tracking changes in the codebase, facilitating collaboration, and managing project versions effectively.

## Technical Stack
- **Python**: Used for API interaction, data preprocessing, and MongoDB integration.
- **MongoDB Atlas**: Serves as the database for storing chess data.
- **Tableau**: Utilized for creating interactive visualizations and dashboards, allowing users to analyze chess performance and trends visually.
- **HTTPX**: For making asynchronous HTTP requests to the Chess.com API.
- **Docker**: Used to containerize the application, making it easier to deploy and manage dependencies.
- **Git**: Employed for version control, enabling collaborative development and efficient code management.
- **Logging**: Integrated logging for tracking data retrieval and processing status, as well as error handling.

## Implementation Steps
1. **API Key Retrieval**: Securely obtain the API key necessary for accessing the Chess.com API.
2. **Data Fetching**: Write Python scripts to retrieve data from the API, including player information and game results.
3. **Data Preprocessing**: Clean and transform the fetched data to ensure consistency and usability, handling missing values and normalizing data formats.
4. **Database Storage**: Connect to MongoDB and create a structured database schema to store the processed data.
5. **Dashboard Development**: Establish a live connection between MongoDB and Tableau, enabling real-time updates in the dashboard.
6. **Containerization**: Create a Docker container to encapsulate the application, ensuring it runs consistently across different environments.
7. **Version Control**: Initialize a Git repository to manage code changes, collaborate with other developers, and maintain project history.
8. **Visualization Design**: Create various visualizations in Tableau, such as player performance trends, game outcomes, and comparative analyses of different players.

## Features
1. **Interactive features**: Line trend and game records based on the time of day: morning, afternoon, evening. Changes can be viewed based on match type: rapid, bullet, blitz.
2. **Player Information**: Detailed profiles for each player, including player name, joined date, and player league.
3. **Accuracy winning/losing**: Summary of average player accuracy based on winning and losing games
4. **Top 5 Opening/Closing moves**: Bar chart representation of the most frequently used opening and closing moves by players, providing insights into strategies and trends
5. **Duration of matches**: Histogram displaying the distribution of match durations in seconds, enabling users to analyze how time affects game outcomes.
6. **Fastest/slowest/average time winning matches**: Summary statistics highlighting the fastest, slowest, and average time in seconds taken to win matches, helping users understand pacing and efficiency in gameplay.
