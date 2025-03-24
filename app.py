import streamlit as st
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import process
import ast

# Set page config at the top
st.set_page_config(layout="wide", page_title="Smart Product Recommendation System")

# Load and preprocess data
@st.cache_data
def load_data():
    df = pd.read_csv("Dataset_preprocessed_with_accessory.csv")

    # Data cleaning
    df['price'] = pd.to_numeric(df['price'].replace('Not Available', np.nan), errors='coerce')
    df['rating'] = pd.to_numeric(df['rating'], errors='coerce')
    df['review_count'] = pd.to_numeric(df['review_count'], errors='coerce')

    # Handle missing values
    median_price = df['price'].median()
    df['price'] = df['price'].fillna(median_price)
    df['rating'] = df['rating'].fillna(0)
    df['review_count'] = df['review_count'].fillna(0)

    # Clean feature lists
    def safe_convert(x):
        try:
            if isinstance(x, str):
                if x.startswith('[') and x.endswith(']'):
                    return ast.literal_eval(x)
                else:
                    return [item.strip() for item in x.split(',')]
            return []
        except (ValueError, SyntaxError):
            return []

    df['features'] = df['features'].apply(safe_convert)

    return df

df = load_data()

# Feature engineering
df['text_features'] = df['product_title'] + ' ' + df['category'] + ' ' + df['brand'] + ' ' + df['features'].apply(lambda x: ' '.join(x))
tfidf = TfidfVectorizer(stop_words='english', ngram_range=(1,2))
tfidf_matrix = tfidf.fit_transform(df['text_features'])
cosine_sim = cosine_similarity(tfidf_matrix)

# Recommendation function
def get_recommendations(product_name, df, cosine_sim, price_range, for_accessories=False, brand_filter=None, category_filter=None, rating_filter=None):
    matches = process.extractBests(product_name.lower(), df['product_title'].str.lower(), limit=1)
    if not matches:
        return []

    idx = df[df['product_title'].str.lower() == matches[0][0].lower()].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:]

    seen_products = set()
    recommendations = []

    for i in sim_scores:
        product = df.iloc[i[0]]
        if len(recommendations) >= 5:
            break

        # Price filter
        if not (price_range[0] <= product['price'] <= price_range[1]):
            continue

        # Rating filter
        if rating_filter:
            valid_rating = False
            for (r_min, r_max) in rating_filter:
                if r_min <= product['rating'] < r_max:
                    valid_rating = True
                    break
            if not valid_rating:
                continue

        # Accessory filters
        if for_accessories:
            if brand_filter and product['brand'] not in brand_filter:
                continue
            if category_filter != 'All' and product['category'] != category_filter:
                continue
            if not product['is_accessory']:
                continue
        else:
            if product['is_accessory']:
                continue

        product_sig = f"{product['brand']}-{product['product_title']}"
        if product_sig in seen_products:
            continue
        seen_products.add(product_sig)

        recommendations.append({
            "title": product['product_title'],
            "price": product['price'],
            "brand": product['brand'],
            "rating": product['rating'],
            "review_count": product['review_count'],
            "image": product['image_url'],
            "features": product['features']
        })
    return recommendations

# Streamlit UI
st.markdown("""
    <style>
        .title-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 150px;
            background: linear-gradient(135deg, #6a11cb, #2575fc);
            color: #fff;
            font-size: 40px;
            font-weight: bold;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            margin-bottom: 30px;
        }
    </style>
    <div class="title-container">
        🔍 Smart Product Recommendation System
    </div>
""", unsafe_allow_html=True)


# Sidebar Filters
with st.sidebar:
    st.markdown('<div class="filter-header">Filters</div>', unsafe_allow_html=True)

    # Price Filter
    min_price = float(df['price'].min())
    max_price = float(df['price'].max())
    price_range = st.slider(
        "Price Range:",
        min_value=min_price,
        max_value=max_price,
        value=(min_price, max_price),
        format="₹%.2f"
    )

    # Rating Filter
    st.markdown("**Rating:**")
    rating_5 = st.checkbox("★★★★★ (4.5 & above)")
    rating_4 = st.checkbox("★★★★☆ (4.0 - 4.4)")
    rating_3 = st.checkbox("★★★☆☆ (3.0 - 3.9)")
    rating_2 = st.checkbox("★★☆☆☆ (2.0 - 2.9)")

    selected_ratings = []
    if rating_5:
        selected_ratings.append((4.5, 5.0))
    if rating_4:
        selected_ratings.append((4.0, 4.5))
    if rating_3:
        selected_ratings.append((3.0, 4.0))
    if rating_2:
        selected_ratings.append((2.0, 3.0))

    # Category Filter
    accessory_categories = ['All'] + sorted(df[df['is_accessory']]['category'].unique().tolist())
    selected_category = st.selectbox(
        "Accessory Category:",
        options=accessory_categories,
        index=0
    )

    # Brand Filter
    if selected_category == 'All':
        available_brands = df[df['is_accessory']]['brand'].unique().tolist()
    else:
        available_brands = df[(df['is_accessory']) & (df['category'] == selected_category)]['brand'].unique().tolist()

    selected_brands = st.multiselect(
        "Accessory Brands:",
        options=sorted(available_brands),
        default=[]
    )

# Main Content
search_query = st.text_input("Search for products:", "Apple iPhone 16")

# Get Recommendations
similar_products = get_recommendations(search_query, df, cosine_sim, price_range, rating_filter=selected_ratings)
accessories = get_recommendations(search_query, df, cosine_sim, price_range,
                                for_accessories=True,
                                brand_filter=selected_brands,
                                category_filter=selected_category,
                                rating_filter=selected_ratings)

# ... (rest of the display code remains unchanged) ...


def product_card(product):
    # Ensure features list is properly formatted
    features = product['features'] if isinstance(product['features'], list) else []
    
    features_html = "".join([f"<li>{feat}</li>" for feat in features]) if features else "<li>No features available</li>"
    
    return f"""
    <div style="
        padding: 15px;
        border-radius: 10px;
        margin: 10px;
        background: #ffffff;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        color: #333333;
        height: 500px;
        overflow: hidden;
        display: flex;
        flex-direction: column;
    ">
        <img src="{product['image']}" style="border-radius:8px; margin-bottom:10px; width:100%; height:200px; object-fit: contain;">
        <div style="flex-grow: 1; overflow: hidden;">
            <h4 style="margin:0 0 10px 0; color: #222222; text-align: center; font-size: 1.1em;">{product['title'][:80]}</h4>
            <div style="margin-bottom: 10px; text-align: center;">
                <span style="background: #f0f2f6; padding: 3px 8px; border-radius: 5px; margin-right: 5px;">
                    ★ {product['rating']:.1f} ({product['review_count']} reviews)
                </span>
                <span style="background: #e3f2fd; padding: 3px 8px; border-radius: 5px;">
                    ₹{product['price']:,.2f}
                </span>
            </div>
            <div style="margin-top: 10px;">
                <b style="color: #1a73e8;">Key Features:</b>
                <div style="max-height: 150px; overflow-y: auto; margin-top: 5px; border: 1px solid #eee; border-radius: 8px; padding: 8px;">
                    <ul style="margin: 0; padding-left: 20px; font-size: 14px;">
                        {features_html}
                    </ul>
                </div>
            </div>
        </div>
    </div>
    """
def product_details(product):
    with st.expander(f"Details for {product['title']}"):
        st.image(product['image'], caption=product['title'], width=300)  # Use width instead of use_column_width
        st.write(f"**Brand:** {product['brand']}")
        st.write(f"**Rating:** {product['rating']} (from {product['review_count']} reviews)")
        st.write(f"**Price:** ₹{product['price']:,.2f}")
        st.write("**Features:**")
        for feature in product['features']:
            st.write(f"- {feature}")

# Display Similar Products (Main Products)
if similar_products:
    st.markdown("## Similar Products")
    cols = st.columns(3)
    for idx, product in enumerate(similar_products[:3]):
        with cols[idx % 3]:
            st.markdown(product_card(product), unsafe_allow_html=True)
            product_details(product)

# Display Accessories
if accessories:
    st.markdown("## Recommended Accessories")
    cols = st.columns(4)
    for idx, product in enumerate(accessories[:4]):
        with cols[idx % 4]:
            st.markdown(product_card(product), unsafe_allow_html=True)
            product_details(product)

# Empty state handling
if not similar_products and not accessories:
    st.warning("No products found matching your search. Try different keywords!")
elif not similar_products:
    st.warning("No similar products found. Try adjusting your search!")
elif not accessories:
    st.warning("No accessories found matching filters. Try adjusting filters!")
