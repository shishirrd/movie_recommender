# code
import numpy as np
import pandas as pd
import streamlit as st

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

#import plotly.graph_objs as go
#import plotly.express as px

ratings = pd.read_csv("ratings.csv")
#ratings.head()

movies = pd.read_csv("movies.csv")
#movies.head()

n_ratings = len(ratings)
n_movies = len(ratings['movieId'].unique())
n_users = len(ratings['userId'].unique())

#print(f"Number of ratings: {n_ratings}")
#print(f"Number of unique movieId's: {n_movies}")
#print(f"Number of unique users: {n_users}")
#print(f"Average ratings per user: {round(n_ratings/n_users, 2)}")
#print(f"Average ratings per movie: {round(n_ratings/n_movies, 2)}")

user_freq = ratings[['userId', 'movieId']].groupby('userId').count().reset_index()
user_freq.columns = ['userId', 'n_ratings']
user_freq.head()


# Find Lowest and Highest rated movies:
mean_rating = ratings.groupby('movieId')[['rating']].mean()
# Lowest rated movies
lowest_rated = mean_rating['rating'].idxmin()
#movies.loc[movies['movieId'] == lowest_rated]
# Highest rated movies
highest_rated = mean_rating['rating'].idxmax()
#movies.loc[movies['movieId'] == highest_rated]
# show number of people who rated movies rated movie highest
#ratings[ratings['movieId']==highest_rated]
# show number of people who rated movies rated movie lowest
#ratings[ratings['movieId']==lowest_rated]

## the above movies has very low dataset. We will use bayesian average
movie_stats = ratings.groupby('movieId')[['rating']].agg(['count', 'mean'])
movie_stats.columns = movie_stats.columns.droplevel()

# Now, we create user-item matrix using scipy csr matrix
from scipy.sparse import csr_matrix

def create_matrix(df):
	
	N = len(df['userId'].unique())
	M = len(df['movieId'].unique())
	
	# Map Ids to indices
	user_mapper = dict(zip(np.unique(df["userId"]), list(range(N))))
	movie_mapper = dict(zip(np.unique(df["movieId"]), list(range(M))))
	
	# Map indices to IDs
	user_inv_mapper = dict(zip(list(range(N)), np.unique(df["userId"])))
	movie_inv_mapper = dict(zip(list(range(M)), np.unique(df["movieId"])))
	
	user_index = [user_mapper[i] for i in df['userId']]
	movie_index = [movie_mapper[i] for i in df['movieId']]

	X = csr_matrix((df["rating"], (movie_index, user_index)), shape=(M, N))
	
	return X, user_mapper, movie_mapper, user_inv_mapper, movie_inv_mapper

X, user_mapper, movie_mapper, user_inv_mapper, movie_inv_mapper = create_matrix(ratings)

from sklearn.neighbors import NearestNeighbors
def find_similar_movies(movie_id, X, k, metric='cosine', show_distance=False):
	
	neighbour_ids = []
	
	movie_ind = movie_mapper[movie_id]
	movie_vec = X[movie_ind]
	k+=1
	kNN = NearestNeighbors(n_neighbors=k, algorithm="brute", metric=metric)
	kNN.fit(X)
	movie_vec = movie_vec.reshape(1,-1)
	neighbour = kNN.kneighbors(movie_vec, return_distance=show_distance)
	for i in range(0,k):
		n = neighbour.item(i)
		neighbour_ids.append(movie_inv_mapper[n])
	neighbour_ids.pop(0)
	return neighbour_ids

st.title("What movie should I watch next?")
st.info("""Ever found yourself searching for just the right movie for what feels like hours, only to find your food cold by the time you select one? Here's a nifty way to find yourself some good-old fashioned classic movies, released even as early as the 1919 and right up to 2018! :sunglasses:""")
st.subheader("Select a movie from the list below")

movie_titles = dict(zip(movies['movieId'], movies['title']))

#movie_names = ['Toy Story (1995)', 'Jumanji (1995)', 'Grumpier Old Men (1995)', 'Waiting to Exhale (1995)', 'Father of the Bride Part II (1995)', 'Heat (1995)', 'Sabrina (1995)', 'Tom and Huck (1995)', 'Sudden Death (1995)', 'GoldenEye (1995)', 'American President, The (1995)', 'Dracula: Dead and Loving It (1995)', 'Balto (1995)', 'Nixon (1995)', 'Cutthroat Island (1995)', 'Casino (1995)', 'Sense and Sensibility (1995)', 'Four Rooms (1995)', 'Ace Ventura: When Nature Calls (1995)', 'Money Train (1995)', 'Get Shorty (1995)', 'Copycat (1995)', 'Assassins (1995)', 'Powder (1995)', 'Leaving Las Vegas (1995)', 'Othello (1995)', 'Now and Then (1995)', 'Persuasion (1995)', 'City of Lost Children, The (CitÃ© des enfants perdus, La) (1995)', 'Shanghai Triad (Yao a yao yao dao waipo qiao) (1995)', 'Dangerous Minds (1995)', 'Twelve Monkeys (a.k.a. 12 Monkeys) (1995)', 'Babe (1995)', 'Dead Man Walking (1995)', 'It Takes Two (1995)', 'Clueless (1995)', 'Cry, the Beloved Country (1995)', 'Richard III (1995)', 'Dead Presidents (1995)', 'Restoration (1995)', 'Mortal Kombat (1995)', 'To Die For (1995)', 'How to Make an American Quilt (1995)', 'Seven (a.k.a. Se7en) (1995)', 'Pocahontas (1995)', 'When Night Is Falling (1995)', 'Usual Suspects, The (1995)', 'Mighty Aphrodite (1995)', 'Lamerica (1994)', 'Big Green, The (1995)', 'Georgia (1995)', 'Home for the Holidays (1995)', 'Postman, The (Postino, Il) (1994)', 'Indian in the Cupboard, The (1995)', 'Eye for an Eye (1996)', "Mr. Holland's Opus (1995)", "Don't Be a Menace to South Central While Drinking Your Juice in the Hood (1996)", 'Two if by Sea (1996)', 'Bio-Dome (1996)', 'Lawnmower Man 2: Beyond Cyberspace (1996)', 'French Twist (Gazon maudit) (1995)', 'Friday (1995)', 'From Dusk Till Dawn (1996)', 'Fair Game (1995)', 'Kicking and Screaming (1995)', 'MisÃ©rables, Les (1995)', 'Bed of Roses (1996)', 'Big Bully (1996)', 'Screamers (1995)', 'Nico Icon (1995)', 'Crossing Guard, The (1995)', 'Juror, The (1996)', 'White Balloon, The (Badkonake sefid) (1995)', "Things to Do in Denver When You're Dead (1995)", "Antonia's Line (Antonia) (1995)", 'Once Upon a Time... When We Were Colored (1995)', 'Angels and Insects (1995)', 'White Squall (1996)', 'Dunston Checks In (1996)', 'Black Sheep (1996)', 'Nick of Time (1995)', 'Mary Reilly (1996)', 'Vampire in Brooklyn (1995)', 'Beautiful Girls (1996)', 'Broken Arrow (1996)', 'In the Bleak Midwinter (1995)', 'Hate (Haine, La) (1995)', 'Heidi Fleiss: Hollywood Madam (1995)', 'City Hall (1996)', 'Bottle Rocket (1996)', 'Mr. Wrong (1996)', 'Unforgettable (1996)', 'Happy Gilmore (1996)', 'Bridges of Madison County, The (1995)', 'Nobody Loves Me (Keiner liebt mich) (1994)', 'Muppet Treasure Island (1996)', 'Catwalk (1996)', 'Braveheart (1995)', 'Taxi Driver (1976)', 'Rumble in the Bronx (Hont faan kui) (1995)', 'Before and After (1996)', 'Anne Frank Remembered (1995)', "Young Poisoner's Handbook, The (1995)", 'If Lucy Fell (1996)', 'Steal Big, Steal Little (1995)', 'Boys of St. Vincent, The (1992)', 'Boomerang (1992)', 'Chungking Express (Chung Hing sam lam) (1994)', 'Flirting With Disaster (1996)', 'NeverEnding Story III, The (1994)', "Jupiter's Wife (1994)", 'Pie in the Sky (1996)', 'Jade (1995)', 'Down Periscope (1996)', 'Man of the Year (1995)', 'Up Close and Personal (1996)', 'Birdcage, The (1996)', 'Brothers McMullen, The (1995)', 'Bad Boys (1995)', 'Amazing Panda Adventure, The (1995)', 'Basketball Diaries, The (1995)', 'Awfully Big Adventure, An (1995)', 'Amateur (1994)', 'Apollo 13 (1995)', 'Rob Roy (1995)', 'Addiction, The (1995)', 'Batman Forever (1995)', 'Beauty of the Day (Belle de jour) (1967)', 'Beyond Rangoon (1995)', 'Blue in the Face (1995)', 'Canadian Bacon (1995)', 'Casper (1995)', 'Clockers (1995)', 'Congo (1995)', 'Crimson Tide (1995)', 'Crumb (1994)', 'Desperado (1995)', 'Devil in a Blue Dress (1995)', 'Die Hard: With a Vengeance (1995)', 'Doom Generation, The (1995)', 'First Knight (1995)', 'Free Willy 2: The Adventure Home (1995)', 'Hackers (1995)', 'Jeffrey (1995)', 'Johnny Mnemonic (1995)', 'Judge Dredd (1995)', 'Jury Duty (1995)', 'Kids (1995)', 'Living in Oblivion (1995)', 'Lord of Illusions (1995)', 'Love & Human Remains (1993)', 'Mad Love (1995)', 'Mallrats (1995)', 'Mighty Morphin Power Rangers: The Movie (1995)', 'Mute Witness (1994)', 'Nadja (1994)', 'Net, The (1995)', 'Nine Months (1995)', 'Party Girl (1995)', 'Prophecy, The (1995)', 'Reckless (1995)', 'Safe (1995)', 'Scarlet Letter, The (1995)', 'Showgirls (1995)', 'Smoke (1995)', 'Something to Talk About (1995)', 'Species (1995)', 'Strange Days (1995)', 'Umbrellas of Cherbourg, The (Parapluies de Cherbourg, Les) (1964)', 'Three Wishes (1995)', 'Total Eclipse (1995)', 'To Wong Foo, Thanks for Everything! Julie Newmar (1995)', 'Under Siege 2: Dark Territory (1995)', 'Unstrung Heroes (1995)', 'Unzipped (1995)', 'Walk in the Clouds, A (1995)', 'Waterworld (1995)', "White Man's Burden (1995)", 'Wild Bill (1995)', 'Browning Version, The (1994)', 'Bushwhacked (1995)', 'Burnt by the Sun (Utomlyonnye solntsem) (1994)', 'Before the Rain (Pred dozhdot) (1994)', 'Before Sunrise (1995)', 'Billy Madison (1995)', 'Babysitter, The (1995)', 'Boys on the Side (1995)', 'Cure, The (1995)', 'Castle Freak (1995)', 'Circle of Friends (1995)', 'Clerks (1994)', 'Don Juan DeMarco (1995)', 'Disclosure (1994)', 'Drop Zone (1994)', 'Destiny Turns on the Radio (1995)', 'Death and the Maiden (1994)', 'Dolores Claiborne (1995)', 'Dumb & Dumber (Dumb and Dumber) (1994)', 'Eat Drink Man Woman (Yin shi nan nu) (1994)', 'Exotica (1994)', 'Exit to Eden (1994)', 'Ed Wood (1994)', 'French Kiss (1995)', 'Forget Paris (1995)', 'Far From Home: The Adventures of Yellow Dog (1995)', 'Goofy Movie, A (1995)', 'Hideaway (1995)', 'Fluke (1995)', 'Farinelli: il castrato (1994)', 'Gordy (1995)', 'Hoop Dreams (1994)', 'Heavenly Creatures (1994)', 'Houseguest (1994)', 'Immortal Beloved (1994)', 'Heavyweights (Heavy Weights) (1995)']

movie_titles2 = dict(zip(movies['title'], movies['movieId']))
movie_title = st.selectbox("Movie Title", movie_titles2)
movie_ids = movie_titles2[movie_title]

similar_ids = find_similar_movies(movie_ids, X, k=10)
movie_title = movie_titles[movie_ids]

st.subheader(f"Since you watched {movie_title}")
for i in similar_ids:
    st.write(movie_titles[i])