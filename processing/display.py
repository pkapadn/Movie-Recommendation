import os
from processing import preprocess
import pickle
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class Main:
    def __enter__(self):
        """Initialization code for resource management."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Cleanup code for resource management."""
        pass

    def __init__(self):
        """Initialize instance variables for dataframes."""
        self.new_df = None
        self.movies = None
        self.movies2 = None

    def getter(self):
        """Retrieve processed dataframes."""
        return self.new_df, self.movies, self.movies2

    def get_df(self):
        """Load or preprocess dataframes and save them as pickle files."""
        pickle_file_path = r'Files/new_df_dict.pkl'

        if os.path.exists(pickle_file_path):
            # Load movies dataframe
            with open(r'Files/movies_dict.pkl', 'rb') as pickle_file:
                self.movies = pd.DataFrame.from_dict(pickle.load(pickle_file))

            # Load movies2 dataframe
            with open(r'Files/movies2_dict.pkl', 'rb') as pickle_file:
                self.movies2 = pd.DataFrame.from_dict(pickle.load(pickle_file))

            # Load new_df dataframe
            with open(pickle_file_path, 'rb') as pickle_file:
                self.new_df = pd.DataFrame.from_dict(pickle.load(pickle_file))

        else:
            # Preprocess data if pickle files are not found
            self.movies, self.new_df, self.movies2 = preprocess.read_csv_to_df()

            # Save movies dataframe as pickle
            with open(r'Files/movies_dict.pkl', 'wb') as pickle_file:
                pickle.dump(self.movies.to_dict(), pickle_file)

            # Save movies2 dataframe as pickle
            with open(r'Files/movies2_dict.pkl', 'wb') as pickle_file:
                pickle.dump(self.movies2.to_dict(), pickle_file)

            # Save new_df dataframe as pickle
            with open(r'Files/new_df_dict.pkl', 'wb') as pickle_file:
                pickle.dump(self.new_df.to_dict(), pickle_file)

    def vectorise(self, col_name):
        """Vectorize a column and calculate cosine similarity."""
        cv = CountVectorizer(max_features=5000, stop_words='english')
        vec_tags = cv.fit_transform(self.new_df[col_name]).toarray()
        sim_bt = cosine_similarity(vec_tags)
        return sim_bt

    def get_similarity(self, col_name):
        """Compute or load similarity matrices for a given column."""
        pickle_file_path = fr'Files/similarity_tags_{col_name}.pkl'

        if not os.path.exists(pickle_file_path):
            similarity_tags = self.vectorise(col_name)
            with open(pickle_file_path, 'wb') as pickle_file:
                pickle.dump(similarity_tags, pickle_file)

    def main_(self):
        """Prepare resources by loading data and computing similarities."""
        self.get_df()
        self.get_similarity('tags')
        self.get_similarity('genres')
        self.get_similarity('keywords')
        self.get_similarity('tcast')
        self.get_similarity('tprduction_comp')
