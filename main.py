import streamlit as st
import streamlit_option_menu
from streamlit_extras.stoggle import stoggle
from processing import preprocess
from processing.display import Main

# Setting the wide mode as default
st.set_page_config(layout="wide")

displayed = []

# Initialize session state variables
if 'movie_number' not in st.session_state:
    st.session_state['movie_number'] = 0

if 'selected_movie_name' not in st.session_state:
    st.session_state['selected_movie_name'] = ""

if 'user_menu' not in st.session_state:
    st.session_state['user_menu'] = ""


def main():
    """Main function to control app flow."""
    with Main() as bot:
        bot.main_()
        new_df, movies, movies2 = bot.getter()
        initial_options(new_df, movies)


def initial_options(new_df, movies):
    """Display tabs and manage their respective functionalities."""
    custom_styles()
    st.subheader('Movie Recommendation System')

    tab1, tab2 = st.tabs(["Recommend a Movie", "Description"])

    # Tab 1: Recommend a Movie
    with tab1:
        recommend_display(new_df)

    # Tab 2: Describe a Movie
    with tab2:
        display_movie_details()


def recommend_display(new_df):
    """Recommend a movie based on user selection."""
    if new_df.empty:
        st.error("No movies found to recommend.")
        return

    st.markdown(dropdown_styles(), unsafe_allow_html=True)
    selected_movie_name = st.selectbox('Choose a movie...', new_df['title'].values)
    st.session_state.selected_movie_name = new_df['title'].values[0]

    if selected_movie_name:
        with st.spinner('Fetching recommendations...'):
            st.session_state.selected_movie_name = selected_movie_name
            recommendation_tags(new_df, selected_movie_name, r'Files/similarity_tags_tags.pkl', "are")
            recommendation_tags(new_df, selected_movie_name, r'Files/similarity_tags_genres.pkl', "on the basis of genres are")
            recommendation_tags(new_df, selected_movie_name, r'Files/similarity_tags_tprduction_comp.pkl', "from the same production company are")
            recommendation_tags(new_df, selected_movie_name, r'Files/similarity_tags_keywords.pkl', "on the basis of keywords are")
            recommendation_tags(new_df, selected_movie_name, r'Files/similarity_tags_tcast.pkl', "on the basis of cast are")


def recommendation_tags(new_df, selected_movie_name, pickle_file_path, message):
    """Fetch and display recommendations based on a specific criterion."""
    movies, posters = preprocess.recommend(new_df, selected_movie_name, pickle_file_path)
    st.subheader(f'Best Recommendations {message}...')

    rec_movies, rec_posters = [], []
    cnt = 0
    for i, j in enumerate(movies):
        if cnt == 5:
            break
        if j not in displayed:
            rec_movies.append(j)
            rec_posters.append(posters[i])
            displayed.append(j)
            cnt += 1

    if len(rec_movies) < 5:
        st.warning("Not enough recommendations to display.")

    display_movie_cards(rec_movies, rec_posters)


def display_movie_cards(movies, posters):
    """Display movie cards with posters and titles."""
    st.markdown(image_card_styles(), unsafe_allow_html=True)
    cols = st.columns(len(movies))
    for col, movie, poster in zip(cols, movies, posters):
        with col:
            st.markdown(
                f"""
                <div class="image-card">
                    <img src="{poster}" alt="Movie Poster">
                    <p style="margin-top: 10px; font-weight: bold;">{movie}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


def display_movie_details():
    """Display detailed information for the selected movie."""
    selected_movie_name = st.session_state.selected_movie_name
    info = preprocess.get_details(selected_movie_name)

    with st.container():
        text_col, image_col = st.columns((2, 1))
        with text_col:
            st.text('\n')
            st.title(selected_movie_name)
            st.write("Overview")
            st.write(info[3], wrapText=False)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.text("Rating")
                st.write(info[8])
            with col2:
                st.text("No. of ratings")
                st.write(info[9])
            with col3:
                st.text("Runtime")
                st.write(info[6])

        with image_col:
            st.text('\n')
            st.image(info[0])

    st.markdown(image_container_styles(), unsafe_allow_html=True)
    st.header("Cast")
    display_cast(info[14])


def display_cast(cast):
    """Display cast information for the selected movie."""
    urls, bios = [], []
    for i in cast[:5]:
        url, bio = preprocess.fetch_person_details(i)
        urls.append(url)
        bios.append(bio)

    cols = st.columns(len(urls))
    for col, url in zip(cols, urls):
        with col:
            st.markdown(
                f"""
                <div class="image-container">
                    <img src="{url}" style="width: 100%; height: auto;" alt="Cast Member">
                </div>
                """,
                unsafe_allow_html=True,
            )


def custom_styles():
    """Inject custom styles for tabs and buttons."""
    st.markdown(
        """
        <style>
        div[data-testid="stTabs"] button[data-baseweb="tab"] {
            background-color: transparent !important;
            color: #0073e6 !important;
            border: none !important;
            padding: 10px 20px !important;
            font-size: 16px !important;
            font-weight: normal !important;
            cursor: pointer !important;
            transition: color 0.3s !important;
        }
        div[data-testid="stTabs"] button[data-baseweb="tab"]:hover {
            color: #005bb5 !important;
        }
        div[data-testid="stTabs"] button[data-baseweb="tab"][aria-selected="true"] {
            color: #005bb5 !important;
            font-weight: bold !important;
            border-bottom: 3px solid #005bb5 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def dropdown_styles():
    """CSS styles for dropdown menus."""
    return """
        <style>
        div[data-baseweb="select"] > div {
            background-color: #f5f5f5;
            border: 2px solid #0073e6;
            border-radius: 10px;
            color: #333333;
        }
        ul[data-baseweb="menu"] {
            background-color: #e6f7ff;
            color: #0073e6;
        }
        ul[data-baseweb="menu"] > li:hover {
            background-color: #0073e6;
            color: #ffffff;
        }
        </style>
    """


def image_card_styles():
    """CSS styles for movie image cards."""
    return """
        <style>
        .image-card {
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            background-color: #f9f9f9;
            border-radius: 15px;
            padding: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s;
        }
        .image-card:hover {
            transform: scale(1.05);
        }
        .image-card img {
            border-radius: 15px;
            max-width: 100%;
            height: auto;
        }
        </style>
    """


def image_container_styles():
    """CSS styles for cast image containers."""
    return """
        <style>
        .image-container {
            border: 2px solid #4CAF50;
            border-radius: 10px;
            overflow: hidden;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .image-container:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        </style>
    """


if __name__ == '__main__':
    main()
