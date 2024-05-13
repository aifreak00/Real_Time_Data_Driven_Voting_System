# 🗳️ Real-Time Voting System

## Welcome🎉

Welcome to our innovative Real-Time Voting System project! 🗳️ In this endeavor, we aim to create a robust platform for conducting elections in real-time. Join us as we leverage cutting-edge technologies to ensure efficient, secure, and transparent voting processes.

## 🚀 Get Started

Ready to kickstart your journey with our Real-Time Voting System? Dive into our comprehensive documentation, featuring setup guides, configuration best practices, and usage instructions to get your election process up and running in no time. Let's make voting accessible, transparent, and secure!

## About the Projectℹ️

Our project implements a real-time election voting system using Python, Kafka, Spark Streaming, Postgres, and Streamlit. Through Docker Compose, we orchestrate the seamless deployment of the required services in Docker containers, facilitating easy setup and scalability. The system is designed to handle large-scale elections with ease while maintaining integrity and reliability throughout the voting process.

## 🛠️ Key Components

- 🐍 **Python**: The primary language for building our system's backend logic and components. Python's versatility and extensive libraries make it ideal for handling various aspects of the voting system, from data generation to processing and visualization.

- 📊 **Kafka**: A distributed streaming platform for handling real-time data streams efficiently. Kafka plays a pivotal role in our system by managing the flow of voter data, ensuring fault tolerance, and enabling seamless communication between different components.

- 🚀 **Spark Streaming**: An extension of the Apache Spark platform for processing real-time data streams. Spark Streaming empowers us to perform complex data transformations and aggregations in real-time, providing insights into voter turnout, candidate statistics, and election trends.

- 🐘 **PostgreSQL**: A powerful open-source relational database for storing voting data securely. PostgreSQL ensures data integrity and reliability, enabling us to record and manage voting records with confidence while adhering to privacy and security standards.

- 🌐 **Streamlit**: An open-source Python library for building interactive web applications for data visualization. Streamlit enables us to create dynamic dashboards that present election statistics in real-time, fostering transparency and accessibility for stakeholders and voters alike.


## 🌟 System Components

- **Main.py**: Utilizes the Random User API to generate voter and candidate data. Establishes connections to Kafka and PostgreSQL, creates necessary tables in the database, and produces voter data to Kafka for further processing. The `generate_voter_data()` and `generate_candidate_data()` functions fetch data from the API, while `insert_voters()` inserts voter data into the PostgreSQL database.

- **Voting.py**: Consumes voter data from Kafka, assigns candidates randomly, records votes in PostgreSQL, and produces voting data back to Kafka. It ensures fault tolerance by handling exceptions during database operations and utilizes a Kafka consumer to receive voter data, assign candidates, and commit votes to the database. The `delivery_report()` function ensures message delivery confirmation to Kafka.

- **Spark-Streaming.py**: Reads voting data from Kafka topics, processes, and aggregates it using Spark Structured Streaming. It defines schemas for Kafka topics, reads data using Spark's Kafka integration, and aggregates votes per candidate and turnout by location. Finally, it writes the aggregated results back to Kafka topics ('aggregated_votes_per_candidate', 'aggregated_turnout_by_location').

- **Streamlit-App.py**: Creates a real-time dashboard using Streamlit to display election statistics. It fetches data from Kafka topics and PostgreSQL, updates the dashboard dynamically, and utilizes Streamlit's autorefresh feature to ensure real-time updates. The dashboard provides visualizations and tables for voter turnout, candidate statistics, and leading candidates.


## 🌟 In-Depth Exploration
Our Real-Time Voting System offers a comprehensive suite of functionalities, including:

**Data Generation**: Main.py utilizes the Random User API to generate realistic voter and candidate data, ensuring a dynamic and varied electorate.

**Real-Time Processing**: Voting.py and Spark-Streaming.py form the backbone of real-time data processing and analysis. Voting.py handles the assignment of candidates and records votes securely, while Spark-Streaming.py performs complex aggregations and analyses on the incoming voting data.

**Data Storage**: PostgreSQL serves as the reliable storage backend for our voting system, ensuring data integrity and availability throughout the electoral process.

**Interactive Dashboard**: Streamlit-App.py provides an intuitive and interactive interface for stakeholders to monitor the progress of the election in real-time, offering dynamic visualizations and statistics.

## 🏘️ Architecture/Workflows

![system_architecture](https://github.com/aifreak00/Real_Time_Data_Driven_Voting_System/assets/113664560/6e318c13-b58d-4a87-81d7-32dd95001ff0)


## Screenshots 📸

![Capture](https://github.com/aifreak00/Real_Time_Data_Driven_Voting_System/assets/113664560/59bd989c-57e2-4c17-8faf-de1d7328eab0)
![dgrg](https://github.com/aifreak00/Real_Time_Data_Driven_Voting_System/assets/113664560/56927029-fde4-49b8-9cef-0a8769f90a5c)
![dffgrg](https://github.com/aifreak00/Real_Time_Data_Driven_Voting_System/assets/113664560/7613a67d-5272-477a-98f7-9edcddb4de59)
![cc](https://github.com/aifreak00/Real_Time_Data_Driven_Voting_System/assets/113664560/7a9f89ac-faf8-422a-bb56-51ac3b545e58)



