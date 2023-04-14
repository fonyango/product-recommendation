import numpy as np
import pandas as pd
import sklearn
from sklearn.decomposition import TruncatedSVD
import random

# load data
df = pd.read_csv('data.csv')

# flower list will be used to assign product ids
flower_list = ["Rose","Lily","Daisy","Sunflower","Tulip","Daffodil","Hydrangea","Pansy",
                "Carnation","Peony","Iris","Chrysanthemum","Magnolia","Marigold",
                "Orchid","Zinnia","Snapdragon",
                "Lavender","Honeysuckle","Foxglove","Jasmine","Petunia","Poppy","Lilac","Dahlia","Bluebell",
                "Fuchsia","Begonia","Geranium","Hibiscus","Cosmos","Amaryllis","Azalea","Anemone","Ranunculus",
                "Sweet Pea","Gladiolus","Primrose","Forget-me-not","Columbine","Crocus","Snowdrop","Camellia",
                "Narcissus","Freesia","Buttercup","Aster","Coneflower","Chrysoprase","Gaillardia","Hollyhock",
                "Queen Anne's Lace","Nasturtium","Verbena","Gardenia","Sweet William","Wisteria","Black-Eyed Susan",
                "Baby's Breath","Bachelor Button","Canterbury Bells","Celosia","Spider Lily","Stargazer Lily",
                "Sunray","Sweet Alyssum","Tickseed","Starflower","Tiger Lily","Torch Lily","Waxflower",
                "Water Lily","Weigela","Yarrow","Yellow Bell","Yellow Archangel","Yucca","Zenobia","Zephyranthes",
                "Gerbera Daisy","African Violet","Bird of Paradise","Blue Flag Iris","Blue Mist Shrub","Butterfly Bush",
                "Cardinal Flower","Chocolate Cosmos","Cockscomb","Crown Imperial","Dutch Iris","Evening Primrose",
                "Firethorn","Four O'Clock","French Marigold","Garden Phlox","Goldenrod",
                "Guernsey Lily","Japanese Anemone",
                "Japanese Iris","Lady's Mantle"]

def get_popular_products(user_id):
    
    # check if a user is a new or returning user

    if user_id not in df['UserId'].unique():
        popular_products = pd.DataFrame(df.groupby('ProductId')['Rating'].count()).reset_index()
        most_popular = popular_products.sort_values('Rating', ascending=False)
        top_five_products = most_popular[:4]
        result = top_five_products['ProductId'].unique()

    else:
        # check the products previously bought by a returning user
        products_bought = df[df['UserId']==user_id]
        product_list = list(set(products_bought['ProductId'].unique()))

        # get a random product from the list
        random_product_id = random.choice(product_list)

        ratings_utility_matrix = df.pivot_table(values='Rating', index='UserId',\
                                                columns='ProductId', fill_value=0)
        X = ratings_utility_matrix.T

        SVD = TruncatedSVD(n_components=10)
        decomposed_matrix = SVD.fit_transform(X)
        correlation_matrix = np.corrcoef(decomposed_matrix)

        product_names = list(X.index)
        product_ID = product_names.index(random_product_id)

        correlation_product_ID = correlation_matrix[product_ID]
        Recommend = list(X.index[correlation_product_ID > 0.90])

        # Removes the item already bought by the customer
        if product_ID in Recommend:
            Recommend.remove(product_ID) 
        else:
            pass

        result = Recommend[0:4]

    return result


# Dictionary to store the mapping between user IDs and flower names
user_flower_dict = {}

def assign_flower_names(user_id, product_ids):
    # If the user ID is already in the dictionary, return the existing mapping

    if user_id in user_flower_dict:
        print(user_flower_dict[user_id])
        return user_flower_dict[user_id]
    
    # Choose random unique flower names for the product IDs
    flower_names = random.sample(flower_list, len(product_ids))
    
    product_flower_dict = dict(zip(product_ids, flower_names))
    
    # choose random prices
    price_list = [random.randint(100, 250) for _ in range(5)]

    flower_dict = {
        "product_id":list(product_flower_dict.keys()),
        "flower_name":list(product_flower_dict.values()),
        "price":price_list
    }

    result = []
    for i in range(len(flower_dict['product_id'])):
        item = {
            'product_id': flower_dict['product_id'][i],
            'flower_name': flower_dict['flower_name'][i],
            'price': flower_dict['price'][i]
        }
        result.append(item)

    # Store the result in the user_flower_dict dictionary
    user_flower_dict[user_id] = result

    return result
