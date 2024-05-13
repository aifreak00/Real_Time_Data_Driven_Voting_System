import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import simplejson as json
import streamlit as st
from kafka import KafkaConsumer
from streamlit_autorefresh import st_autorefresh
import psycopg2
from kafka.errors import NoBrokersAvailable
import requests
from PIL import Image
from io import BytesIO
import plotly.express as px


st.set_page_config(
        
        page_icon=":bar_chart:",
        layout="wide",
        
        # Collapsed sidebar by default
    )


# Override the default Streamlit title
st.markdown("""
    <style>
        .css-1bc9zcm {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

# Center the page title
st.markdown(
    """
    <div style="display: flex; justify-content: center; margin-top: -50px;">
        <h1>🗳️ Real-Time Indian Election Dashboard 📊</h1>
    </div>
    """,
    unsafe_allow_html=True,
)


# Define color palette


# color_palette = ["#440154", "#482878", "#3E4989", "#31688E", "#26838E", 
#                  "#1F9E89", "#35B779", "#6CCE59", "#B4DE2C", "#FDE725"]
# Set background color and text colors
# color_palette = ["#636EFA", "#EF553B", "#00CC96", "#AB63FA", 
#                  "#FFA15A", "#19D3F3", "#FF6692", "#B6E880", 
#                  "#FF97FF", "#FECB52"]


# Function to create a Kafka consumer
# ... (rest of the code)
# color_palette = ["#0072B2", "#D55E00", "#CC79A7", "#F0E442", 
#                  "#56B4E9", "#009E73", "#E69F00", "#64E572",
#                  "#F8766D", "#00BA38", "#619CFF", "#F564E3",
#                  "#9A6324", "#4D4D4D", "#E41A1C", "#377EB8",
#                  "#984EA3", "#FF7F00", "#2A2A2A", "#A6CEE3"]


color_palette = ["#5DA5DA", "#FAA43A", 
                   "#B276B2", "#DECF3F", 
                 "#F15854"]

# Function to create a Kafka consumer
def create_kafka_consumer(topic_name, max_retries=3, retry_delay=5):
    retries = 0
    while retries < max_retries:
        try:
            consumer = KafkaConsumer(
                topic_name,
                bootstrap_servers='localhost:9092',
                auto_offset_reset='earliest',
                value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                consumer_timeout_ms=120000  # Increase the consumer timeout to 10 seconds
            )
            return consumer
        except NoBrokersAvailable as e:
            retries += 1
            st.warning(
                f"Error connecting to Kafka broker: {e}. Retrying in {retry_delay} seconds... (Attempt {retries}/{max_retries})"
            )
            time.sleep(retry_delay)
    st.error(f"Failed to connect to Kafka broker after {max_retries} attempts. Please check your Kafka setup.")
    return None

# Function to fetch voting statistics from PostgreSQL database
@st.cache_data
def fetch_voting_stats():
    # Connect to PostgreSQL database
    conn = psycopg2.connect("host=localhost dbname=voting user=postgres password=postgres")
    cur = conn.cursor()

    # Fetch total number of voters
    cur.execute(""" SELECT count(*) voters_count FROM voters """)
    voters_count = cur.fetchone()[0]

    # Fetch total number of candidates
    cur.execute(""" SELECT count(*) candidates_count FROM candidates """)
    candidates_count = cur.fetchone()[0]

    return voters_count, candidates_count

# Function to fetch data from Kafka
def fetch_data_from_kafka(consumer, max_retries=3, retry_delay=5):
    retries = 0
    while retries < max_retries:
        try:
            messages = consumer.poll(timeout_ms=120000)  # Increase the polling timeout to 10 seconds
            if not messages:
                raise StopIteration("No messages received within the specified timeout.")
            data = []
            for message in messages.values():
                for sub_message in message:
                    data.append(sub_message.value)
            return data
        except StopIteration as e:
            retries += 1
            st.warning(
                f"No messages received from Kafka: {e}. Retrying in {retry_delay} seconds... (Attempt {retries}/{max_retries})"
            )
            time.sleep(retry_delay)
    st.error(f"Failed to receive messages from Kafka after {max_retries} attempts. Please check your Kafka setup.")
    return []

# Function to split a dataframe into chunks for pagination
@st.cache_data(show_spinner=False)
def split_frame(input_df, rows):
    df = [input_df.loc[i: i + rows - 1, :] for i in range(0, len(input_df), rows)]
    return df

# Function to paginate a table
def paginate_table(table_data):
    top_menu = st.columns(3)
    with top_menu[0]:
        sort_key = f"sort_data_radio_{table_data.shape[0]}"  # Generate a unique key based on table size
        sort = st.radio("Sort Data", options=["Yes", "No"], horizontal=1, index=1, key=sort_key)
    if sort == "Yes":
        with top_menu[1]:
            sort_field = st.selectbox("Sort By", options=table_data.columns)
        with top_menu[2]:
            sort_direction_key = f"sort_direction_radio_{table_data.shape[0]}"  # Generate a unique key based on table size
            sort_direction = st.radio(
                "Direction", options=["⬆️", "⬇️"], horizontal=True, key=sort_direction_key
            )
        table_data = table_data.sort_values(by=sort_field, ascending=sort_direction == "⬆️", ignore_index=True)

    pagination = st.container()
    bottom_menu = st.columns((4, 1, 1))
    with bottom_menu[2]:
        batch_size = st.selectbox("Page Size", options=[10, 25, 50, 100])
    with bottom_menu[1]:
        total_pages = (int(len(table_data) / batch_size) if int(len(table_data) / batch_size) > 0 else 1)
        current_page = st.number_input("Page", min_value=1, max_value=total_pages, step=1)
    with bottom_menu[0]:
        st.markdown(f"Page **{current_page}** of **{total_pages}** ")
    pages = split_frame(table_data, batch_size)
    pagination.dataframe(data=pages[current_page - 1], use_container_width=True)

# Function to load an image
def load_image(image_path):
    try:
        if image_path.startswith("http"):
            # Load image from URL
            response = requests.get(image_path)
            response.raise_for_status()
            image = Image.open(BytesIO(response.content))
        else:
            # Load image from local file path
            image = Image.open(image_path)
        return image
    except (requests.RequestException, FileNotFoundError) as e:
        st.error(f"Error loading image: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Error loading image: {str(e)}")
        return None

# Function to update data displayed on the dashboard
def update_data():
    # Placeholder to display last refresh time
    last_refresh = st.empty()
    last_refresh.text(f"Last refreshed at: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Fetch voting statistics
    voters_count, candidates_count = fetch_voting_stats()

    # Display total voters and candidates metrics
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Voters 👆", voters_count, delta_color="inverse")
    with col2:
        st.metric("Total Candidates 🗳️", candidates_count, delta_color="inverse")
    # Fetch data from Kafka on aggregated votes per candidate
    consumer = create_kafka_consumer("aggregated_votes_per_candidate")
    data = fetch_data_from_kafka(consumer)
    results = pd.DataFrame(data)

    # Identify the leading candidate
    results = results.loc[results.groupby('candidate_id')['total_votes'].idxmax()]
    leading_candidate = results.loc[results['total_votes'].idxmax()]

    # Display leading candidate information
    st.markdown("---")
    st.header('Leading Candidate 🏆')
    col1, col2 = st.columns(2)  # Two columns layout
    with col1:
    # Load and display the candidate's image
        image_path = leading_candidate['photo_url']
        image = load_image(image_path)
        if image is not None:
            st.image(image, width=200)
    with col2:
        st.header(leading_candidate['candidate_name'])
        st.subheader(leading_candidate['party_affiliation'])
        st.subheader(f"Total Vote: {leading_candidate['total_votes']:,}")

    # Display statistics and visualizations
    st.markdown("---")
    st.header('Statistics 📊')
    col1, col2 = st.columns(2)  # Two columns layout
# Display bar chart
    with col1:
        fig = px.bar(results, x='candidate_name', y='total_votes', color='party_affiliation', color_discrete_sequence=color_palette)
        st.plotly_chart(fig, use_container_width=True)
# Display donut chart
    with col2:
        fig = px.pie(results, values='total_votes', names='candidate_name', color_discrete_sequence=color_palette)
        st.plotly_chart(fig, use_container_width=True)
    # Display table with candidate statistics
        

    # Fetch data from Kafka on aggregated turnout by location
    location_consumer = create_kafka_consumer("aggregated_turnout_by_location")
    location_data = fetch_data_from_kafka(location_consumer)
    location_result = pd.DataFrame(location_data)

    # Identify locations with maximum turnout
    location_result = location_result.loc[location_result.groupby('state')['count'].idxmax()]
    location_result = location_result.reset_index(drop=True)

    # Display location-based voter information with pagination
    st.header("Location of Voters 🌍")
    paginate_table(location_result)

    # Update the last refresh time
    st.session_state['last_update'] = time.time()

    # Refresh the Streamlit app
    st.experimental_rerun()

# Title of the Streamlit dashboard


# Display sidebar
 

# Update and display data on the dashboard
update_data()