import streamlit as st
import requests
import pandas as pd
from matplotlib import pyplot as plt
from geopy.geocoders import Nominatim


if 'plant_info' not in st.session_state:
    st.session_state.plant_info = None
if 'detailed_info' not in st.session_state:
    st.session_state.detailed_info = None

API_KEY = 'your_api_key'
BASE_URL = 'https://perenual.com/api/'

section = st.sidebar.radio("**Sections**:", ["Basic Plant Care", "Plant Safety Checker"])
st.title('**BotaniDex**: Your Plant Care Assistant')

bg_color = st.sidebar.color_picker('Pick a **background color** for the app!', '#007D00')

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {bg_color};
    }}
    </style>
    """,
    unsafe_allow_html=True
)


def search_plant(plant_name):
    perenual_url = f"{BASE_URL}species-list?key={API_KEY}&q={plant_name}"
    response = requests.get(perenual_url).json()
    return response['data'] if 'data' in response else []


def check_plant_safety(plant_name, safety_type):
    if safety_type == "edible":
        perenual_url = f"{BASE_URL}species-list?key={API_KEY}&q={plant_name}&edible=1"
    elif safety_type == "poisonous":
        perenual_url = f"{BASE_URL}species-list?key={API_KEY}&q={plant_name}&poisonous=1"

    response = requests.get(perenual_url).json()
    return response['data'][0] if 'data' in response and response['data'] else None


def get_coordinates(countries):
    geolocator = Nominatim(user_agent="plant_app")
    coordinates = []
    for country in countries:
        location = geolocator.geocode(country)
        if location:
            coordinates.append([location.latitude, location.longitude])
    return coordinates


if section == "Basic Plant Care":
    st.subheader('Basic Plant Care')
    st.write("Discover essential care instructions for your plant "
             "and explore detailed insights to enhance your understanding of them.")

    plant_name = st.text_input('Enter plant name:')

    show_detailed_info = st.checkbox("Detailed Information")

    col1, col2 = st.columns([1, 7.5])
    with col1:
        search_button = st.button('Search', key='search_button', help='Click to search results')
    with col2:
        reset_button = st.button('Reset', key='reset_button', help='Click to reset search results')

    if reset_button:
        plant_name = ""
        show_detailed_info = False
        st.session_state.plant_info = None
        st.session_state.detailed_info = None

    if search_button and plant_name:
        plant_info = search_plant(plant_name)
        if plant_info:
            st.session_state.plant_info = plant_info[0]
            if show_detailed_info and st.session_state.plant_info.get('id'):
                details_url = f"{BASE_URL}species/details/{st.session_state.plant_info['id']}?key={API_KEY}"
                st.session_state.detailed_info = requests.get(details_url).json()

    if st.session_state.plant_info:
        st.subheader(f"Plant Information for '{st.session_state.plant_info['common_name']}'")

        col1, col2 = st.columns([2, 1])
        with col2:
            st.subheader("Plant Image")
            st.image(st.session_state.plant_info['default_image']['thumbnail'], caption='Plant Image', width=300)
        with col1:
            st.subheader("Basic Information")
            st.info(f"**Common Name:** {st.session_state.plant_info['common_name']}")
            st.info(f"**Cycle:** {st.session_state.plant_info['cycle']}")
            st.info(f"**Watering:** {st.session_state.plant_info['watering']}")
            st.info(f"**Sunlight:** {', '.join(st.session_state.plant_info['sunlight']) if st.session_state.plant_info['sunlight'] else 'N/A'}")

            if show_detailed_info and st.session_state.detailed_info:
                st.subheader("Detailed Information")
                if st.session_state.detailed_info.get('description'):
                    st.success(f"**Description:** {st.session_state.detailed_info['description']}")
                if st.session_state.detailed_info.get('type'):
                    st.info(f"**Type:** {st.session_state.detailed_info['type']}")
                if st.session_state.detailed_info.get('scientific_name'):
                    st.info(f"**Scientific Name:** {', '.join(st.session_state.detailed_info['scientific_name'])}")
                if st.session_state.detailed_info.get('other_name'):
                    st.info(f"**Other Names:** {', '.join(st.session_state.detailed_info['other_name']) if st.session_state.detailed_info['other_name'] else 'N/A'}")
                if st.session_state.detailed_info.get('propagation'):
                    st.info(f"**Propagation:** {', '.join(st.session_state.detailed_info['propagation'])}")
                if st.session_state.detailed_info.get('hardiness'):
                    st.info(f"**Hardiness:** Min {st.session_state.detailed_info['hardiness']['min']} - Max {st.session_state.detailed_info['hardiness']['max']}")
                if 'watering_general_benchmark' in st.session_state.detailed_info:
                    value = st.session_state.detailed_info['watering_general_benchmark']['value']
                    unit = st.session_state.detailed_info['watering_general_benchmark']['unit']
                    st.info(f"**Watering General Benchmark:** {value} {unit}")

                dropdown_stuff = st.multiselect(
                    "Additional Information Visualized",
                    ["Growth Rate / Care Level Bar Graph", "Pruning Line Graph", "Places of Origins Map"]
                )

                if "Growth Rate / Care Level Bar Graph" in dropdown_stuff and st.session_state.detailed_info:
                    st.subheader(f"Growth Rate / Care Level Visualization for '{st.session_state.plant_info['common_name']}'")

                    growth_rate = st.session_state.detailed_info.get('growth_rate', 'Unknown')
                    care_level = st.session_state.detailed_info.get('care_level', 'Unknown')

                    categories = ['Growth Rate', 'Care Level']
                    category_map = {
                        'Low': 1,
                        'Medium': 2,
                        'High': 3
                    }

                    data = {
                        'Growth Rate': category_map[growth_rate] if growth_rate in category_map else 0,
                        'Care Level': category_map[care_level] if care_level in category_map else 0
                    }

                    # Plotting
                    fig, ax = plt.subplots()
                    bar_width = 0.4
                    index = range(len(categories))

                    bars1 = ax.bar(index[0], data['Growth Rate'], bar_width, label='Growth Rate', color='blue')
                    bars2 = ax.bar(index[1], data['Care Level'], bar_width, label='Care Level', color='orange')

                    ax.set_xlabel('Categories')
                    ax.set_ylabel('Values')
                    ax.set_title('Growth Rate and Care Level')
                    ax.set_xticks(index)
                    ax.set_xticklabels(categories)
                    ax.set_yticks([1, 2, 3])
                    ax.set_yticklabels(['Low', 'Medium', 'High'])
                    ax.legend()

                    st.pyplot(fig)

                if "Pruning Line Graph" in dropdown_stuff and st.session_state.detailed_info:
                    st.subheader(f"Pruning Activity Line Graph for '{st.session_state.plant_info['common_name']}'")

                    month_map = {
                        "January": 1,
                        "February": 2,
                        "March": 3,
                        "April": 4,
                        "May": 5,
                        "June": 6,
                        "July": 7,
                        "August": 8,
                        "September": 9,
                        "October": 10,
                        "November": 11,
                        "December": 12
                    }

                    pruning_months = [month_map[month] for month in st.session_state.detailed_info['pruning_month']]

                    all_months = list(range(1, 13))

                    pruning_activity = [1 if month in pruning_months else 0 for month in all_months]

                    fig, ax = plt.subplots()
                    ax.plot(all_months, pruning_activity, marker='o', linestyle='-', color='green')
                    ax.set_xlabel('Month')
                    ax.set_ylabel('Pruning Activity')
                    ax.set_title('Pruning Activity Over the Year')
                    ax.set_xticks(all_months)
                    ax.set_xticklabels(
                        ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
                    ax.set_yticks([0, 1])
                    ax.set_yticklabels(['No Pruning', 'Pruning'])

                    st.pyplot(fig)

                if "Places of Origins Map" in dropdown_stuff and st.session_state.detailed_info:
                    st.subheader(f"Origin Map for '{st.session_state.plant_info['common_name']}'")

                    origins = st.session_state.detailed_info.get('origin', [])
                    coordinates = get_coordinates(origins)

                    if coordinates:
                        df = pd.DataFrame(coordinates, columns=['lat', 'lon'])
                        col1, col2 = st.columns([2, .75])
                        with col1:
                            st.map(df)
                        with col2:
                            st.write("**Place of Origins**:")
                            with st.expander("View Countries"):
                                for country in origins:
                                    st.write(country)


elif section == "Plant Safety Checker":
    st.subheader('Plant Safety Checker')
    st.write("Quickly validate whether a plant is poisonous or safe for consumption.")
    plant_name = st.text_input('Enter plant name:')

    display_format = st.selectbox("Choose display format:", ["Interactive Table", "Info Boxes"])

    col1, col2 = st.columns([2, 9])
    with col1:
        search_button = st.button('Search Safety', key='search_safety_button', help='Click to check plant safety')
    with col2:
        reset_button = st.button('Reset', key='reset_button', help='Click to reset search results')

    if reset_button:
        plant_name = ""

    if search_button and plant_name:
        plant_info = search_plant(plant_name)

        if plant_info:
            plant_info = plant_info[0]
            st.subheader(f"Plant Information for '{plant_info['common_name']}'")

            is_edible = check_plant_safety(plant_name, "edible")
            is_poisonous = check_plant_safety(plant_name, "poisonous")

            if display_format == "Interactive Table":
                data = {
                    'Plant Name': [plant_name],
                    'Edible': [bool(is_edible)],
                    'Poisonous': [bool(is_poisonous)],
                    'Image': [f'<img src="{plant_info["default_image"]["thumbnail"]}" width="100">']
                }
                df = pd.DataFrame(data)

                st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)
            else:

                col1, col2 = st.columns([2, 2.5])
                with col1:
                    st.image(plant_info['default_image']['thumbnail'], caption='Plant Image', width=300)
                with col2:
                    if is_edible:
                        st.success(f"The plant '{plant_name}' is edible.")
                    else:
                        st.warning(f"The plant '{plant_name}' is not listed as edible.")

                    if is_poisonous:
                        st.error(f"The plant '{plant_name}' is poisonous.")
                    else:
                        st.success(f"The plant '{plant_name}' is not listed as poisonous.")
        else:
            st.error(f"No plant found with the name '{plant_name}'. Please try again.")
