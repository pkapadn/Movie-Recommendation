import streamlit as st
import streamlit_option_menu
from streamlit_extras.stoggle import stoggle
from processing import preprocess
from processing.display import Main

# Setting the wide mode as default
st.set_page_config(layout="wide")

displayed = []

if 'movie_number' not in st.session_state:
    st.session_state['movie_number'] = 0

if 'selected_movie_name' not in st.session_state:
    st.session_state['selected_movie_name'] = ""

if 'user_menu' not in st.session_state:
    st.session_state['user_menu'] = ""


def main():
    def initial_options():
        st.markdown(
            """
            <style>
            /* Custom styling specifically for tabs */
            div[data-testid="stTabs"] button[data-baseweb="tab"] {
                background-color: transparent; /* Make tab background transparent */
                color: #0073e6;                /* Set text color */
                border: none;                  /* Remove border */
                border-radius: 0;              /* No rounded corners */
                padding: 10px 20px;            /* Padding for spacing */
                font-size: 16px;               /* Font size */
                font-weight: normal;           /* Normal font weight */
                cursor: pointer;               /* Pointer cursor on hover */
                transition: color 0.3s;        /* Smooth text color transition */
            }
            div[data-testid="stTabs"] button[data-baseweb="tab"]:hover {
                color: #005bb5;                /* Change text color on hover */
            }
            div[data-testid="stTabs"] button[data-baseweb="tab"][aria-selected="true"] {
                color: #005bb5;                /* Active tab text color */
                font-weight: bold;             /* Bold text for active tab */
                border-bottom: 3px solid #005bb5; /* Custom underline for active tab */
            }
            div[data-testid="stTabs"] button[data-baseweb="tab"][aria-selected="true"]:hover {
                color: #003f7f;                /* Darker text color on hover for active tab */
            }

            /* Completely remove Streamlit's default tab underline */
            div[data-testid="stTabs"] div[data-baseweb="tab-highlight"] {
                background: none !important;  /* Remove the pink highlight line */
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        st.subheader('Movie Recommendation System')
        # To display menu
          # Create tabs
        tab1,tab2 = st.tabs(["Recommend a Movie","Description"])

        # Tab 1: Recommend a Movie
        with tab1:
            # st.header("Recommend a Movie")
            # Add your recommendation UI logic here
            recommend_display()

        # Tab 2: Describe a Movie
        with tab2:
            # st.header("Describe a Movie")
            # Add your movie description logic here
            display_movie_details()

        # Tab 3: Check All Movies
        # with tab3:
        #     # st.header("Check All Movies")
        #     # Add your movie list UI logic here
        #     paging_movies()

        # if st.session_state.user_menu == 'Recommend me a similar movie':
        #     recommend_display()

        # elif st.session_state.user_menu == 'Describe me a movie':
        #     display_movie_details()

        # elif st.session_state.user_menu == 'Check all Movies':
        #     paging_movies()

    def recommend_display():

    
        if new_df.empty:
            st.error("No movies found to recommend.")
            return
        # Add custom CSS for the selectbox
        st.markdown(
            """
            <style>
            /* Style the dropdown */
            div[data-baseweb="select"] > div {
                background-color: #f5f5f5;  /* Change background color */
                border: 2px solid #0073e6; /* Add border */
                border-radius: 10px;       /* Round the edges */
                color: #333333;            /* Text color */
                width : 50%;
                alignItems: center
            }

            /* Style the dropdown options */
            ul[data-baseweb="menu"] {
                background-color: #e6f7ff; /* Dropdown options background */
                color: #0073e6;           /* Dropdown options text color */
            }

            /* Change font size and padding for the dropdown text */
            div[data-baseweb="select"] span {
                font-size: 16px;          /* Font size */
                padding: 5px;             /* Padding */
            }

            /* Hover effect for dropdown options */
            ul[data-baseweb="menu"] > li:hover {
                background-color: #0073e6;
                color: #ffffff;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        selected_movie_name = st.selectbox(
            'Choose a movie...', new_df['title'].values
        )
        st.session_state.selected_movie_name = new_df['title'].values[0]
        # st.markdown(
        #     """
        #     <style>
        #     /* Custom button styling */
        #     .custom-button {
        #         background-color: #0073e6; /* Background color */
        #         color: white;             /* Text color */
        #         border: none;             /* Remove border */
        #         border-radius: 10px;      /* Rounded corners */
        #         padding: 10px 20px;       /* Padding */
        #         font-size: 16px;          /* Font size */
        #         cursor: pointer;          /* Pointer cursor on hover */
        #         transition: background-color 0.3s, transform 0.2s; /* Smooth transitions */
        #     }
        #     .custom-button:hover {
        #         background-color: #005bb5; /* Darker background on hover */
        #         transform: scale(1.05);    /* Slight zoom on hover */
        #     }
        #     </style>
        #     """,
        #     unsafe_allow_html=True
        # )
        # rec_button =  st.markdown('<button class="custom-button">Show Recommendation</button>', unsafe_allow_html=True)
        # rec_button = st.button('Show Recommendation')
        if selected_movie_name:
            with st.spinner('Fetching recommendations...'):
                st.session_state.selected_movie_name = selected_movie_name
                recommendation_tags(new_df, selected_movie_name, r'Files/similarity_tags_tags.pkl',"are")
                recommendation_tags(new_df, selected_movie_name, r'Files/similarity_tags_genres.pkl',"on the basis of genres are")
                recommendation_tags(new_df, selected_movie_name,
                                    r'Files/similarity_tags_tprduction_comp.pkl',"from the same production company are")
                recommendation_tags(new_df, selected_movie_name, r'Files/similarity_tags_keywords.pkl',"on the basis of keywords are")
                recommendation_tags(new_df, selected_movie_name, r'Files/similarity_tags_tcast.pkl',"on the basis of cast are")

    def recommendation_tags(new_df, selected_movie_name, pickle_file_path,str):

        movies, posters = preprocess.recommend(new_df, selected_movie_name, pickle_file_path)
        st.subheader(f'Best Recommendations {str}...')

        rec_movies = []
        rec_posters = []
        cnt = 0
        # Adding only 5 uniques recommendations
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
        
        st.markdown(
            """
            <style>
            .image-card {
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
                background-color: #f9f9f9;
                border-radius: 15px; /* Rounded corners */
                padding: 15px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Subtle shadow */
                transition: transform 0.2s; /* Animation on hover */
            }

            .image-card:hover {
                transform: scale(1.05); /* Slight zoom on hover */
            }

            .image-card img {
                border-radius: 15px; /* Make the image rounded */
                max-width: 100%; /* Keep the image responsive */
                height: auto;
            }
            </style>
            """,
            unsafe_allow_html=True
            )
        # Columns to display informations of movies i.e. movie title and movie poster
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            
            st.markdown(
                f"""
                <div class="image-card">
                    <img src="{rec_posters[0]}" alt="Movie Poster">
                    <p style="margin-top: 10px; font-weight: bold;">{rec_movies[0]}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            # st.text()
        with col2:
            st.markdown(
                f"""
                <div class="image-card">
                    <img src="{rec_posters[1]}" alt="Movie Poster">
                    <p style="margin-top: 10px; font-weight: bold;">{rec_movies[1]}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col3:
            
            st.markdown(
                f"""
                <div class="image-card">
                    <img src="{rec_posters[2]}" alt="Movie Poster">
                    <p style="margin-top: 10px; font-weight: bold;">{rec_movies[2]}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col4:
           
            st.markdown(
                f"""
                <div class="image-card">
                    <img src="{rec_posters[3]}" alt="Movie Poster">
                    <p style="margin-top: 10px; font-weight: bold;">{rec_movies[3]}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col5:
            st.markdown(
                f"""
                <div class="image-card">
                    <img src="{rec_posters[4]}" alt="Movie Poster">
                    <p style="margin-top: 10px; font-weight: bold;">{rec_movies[4]}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    def display_movie_details():

        selected_movie_name = st.session_state.selected_movie_name
        # movie_id = movies[movies['title'] == selected_movie_name]['movie_id']
        info = preprocess.get_details(selected_movie_name)

        with st.container():
            text_col, image_col = st.columns((2, 1))
            with text_col:
                st.text('\n')
                st.text('\n')
                st.title(selected_movie_name)
                st.text('\n')
                st.write("Overview")
                st.write(info[3], wrapText=False)
                st.text('\n')
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
                

                
                # col1, col2, col3 = st.columns(3)
                # with col1:
                #     st.text("Release Date")
                #     st.text(info[4])
                # with col2:
                #     st.text("Budget")
                #     st.text(info[1])
                # with col3:
                #     st.text("Revenue")
                #     st.text(info[5])

                st.text('\n')
                # col1, col2, col3 = st.columns(3)
                # with col1:
                #     str = ""
                #     st.text("Genres")
                #     for i in info[2]:
                #         str = str + i + " . "
                #     st.write(str)

                # with col2:
                #     str = ""
                #     st.text("Available in")
                #     for i in info[13]:
                #         str = str + i + " . "
                #     st.write(str)
                # with col3:
                #     st.text("Directed by")
                #     st.text(info[12][0])
                # st.text('\n')

            with image_col:
                st.text('\n')
                st.image(info[0])

        st.markdown(
            """
            <style>
            .image-container {
                border: 2px solid #4CAF50; /* Add a green border */
                border-radius: 10px; /* Make the corners rounded */
                overflow: hidden;
                transition: transform 0.3s, box-shadow 0.3s; /* Smooth animation on hover */
            }
            .image-container:hover {
                transform: scale(1.05); /* Slightly zoom the image on hover */
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Add a shadow effect */
            }
            .cast-container {
                background-color: #f4f4f4;
                padding: 20px;
                border-radius: 10px;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )
            
        st.header("Cast")
        cnt = 0
        urls = []
        bio = []
        for i in info[14]:
            if cnt == 5:
                break
            url, biography = preprocess.fetch_person_details(i)
            urls.append(url)
            bio.append(biography)
            cnt += 1

        # Define columns for layout
        col1, col2, col3, col4, col5 = st.columns(5)

        columns = [col1, col2, col3, col4, col5]
        for idx, col in enumerate(columns):
            with col:
                # Add an image container for hover effect
                st.markdown(f"""
                <div class="image-container">
                    <img src="{urls[idx]}" style="width: 100%; height: auto;" alt="Cast Member">
                </div>
                """, unsafe_allow_html=True)
                
               

    def paging_movies():
        max_pages = movies.shape[0] // 10
        if movies.empty:
            st.error("No movies to display.")
            return

        # Create a container to center the columns
        with st.container():
            # Add some spacing above for centering
            st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)

            # Create a centered layout using columns
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col1:
                if st.button("Prev"):
                    if st.session_state['movie_number'] >= 10:
                        st.session_state['movie_number'] -= 10

            with col2:
                st.write(f"Page {st.session_state['movie_number'] // 10 + 1} of {max_pages + 1}")

            with col3:
                if st.button("Next"):
                    if st.session_state['movie_number'] + 10 < len(movies):
                        st.session_state['movie_number'] += 10

        display_all_movies(st.session_state['movie_number'])




    def display_all_movies(start):

        i = start
        with st.container():
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                id = movies.iloc[i]['movie_id']
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies['title'][i])
                i = i + 1

            with col2:
                id = movies.iloc[i]['movie_id']
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies['title'][i])
                i = i + 1

            with col3:
                id = movies.iloc[i]['movie_id']
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies['title'][i])
                i = i + 1

            with col4:
                id = movies.iloc[i]['movie_id']
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies['title'][i])
                i = i + 1

            with col5:
                id = movies.iloc[i]['movie_id']
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies['title'][i])
                i = i + 1

        with st.container():
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                id = movies.iloc[i]['movie_id']
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies['title'][i])
                i = i + 1

            with col2:
                id = movies.iloc[i]['movie_id']
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies['title'][i])
                i = i + 1

            with col3:
                id = movies.iloc[i]['movie_id']
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies['title'][i])
                i = i + 1

            with col4:
                id = movies.iloc[i]['movie_id']
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies['title'][i])
                i = i + 1

            with col5:
                id = movies.iloc[i]['movie_id']
                link = preprocess.fetch_posters(id)
                st.image(link, caption=movies['title'][i])
                i = i + 1

        st.session_state['page_number'] = i

    with Main() as bot:
        bot.main_()
        new_df, movies, movies2 = bot.getter()
        initial_options()


if __name__ == '__main__':
    main()
