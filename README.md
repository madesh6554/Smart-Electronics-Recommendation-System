🔍 Smart Product Recommendation System

📌 Overview
The Smart Product Recommendation System is a Streamlit-based web application that provides personalized product recommendations based on user queries. It leverages TF-IDF vectorization and cosine similarity to identify similar products and recommends relevant accessories. Users can apply filters such as price range, rating, brand, and category to refine their search.

✅ Live Demo: Smart Electronics Recommendation System

🚀 Features
🔎 Product Search: Search for products by name and get similar product recommendations.

🎯 Accessory Suggestions: Recommend relevant accessories for the selected product.

📊 Advanced Filtering: Filter products by:

Price range

Rating

Category and brand

📄 Product Details: View product details, including price, rating, review count, and key features.

📈 Responsive UI: Clean and user-friendly interface with responsive product cards.

⚡ Efficient Performance: Uses caching with st.cache_data for optimized performance.

🛠️ Tech Stack
Frontend: Streamlit (Python-based UI framework)

Backend:

pandas for data handling

numpy for numerical operations

scikit-learn for vectorization and cosine similarity

Data Processing:

fuzzywuzzy for approximate string matching

TfidfVectorizer for text-based product similarity

Visualization: Dynamic and interactive UI with Streamlit components

🔧 Installation & Usage
⚙️ 1. Clone the Repository
bash
Copy
Edit
git clone <YOUR_REPO_LINK>
cd smart-product-recommendation-system
🔥 2. Install Dependencies
Make sure you have Python installed, then install the required packages:

bash
Copy
Edit
pip install -r requirements.txt
🚀 3. Run the Application
bash
Copy
Edit
streamlit run app.py
📊 File Structure
perl
Copy
Edit
📂 smart-product-recommendation-system
 ├── 📄 app.py                 # Main Streamlit application
 ├── 📄 Dataset_preprocessed_with_accessory.csv   # Preprocessed product dataset
 ├── 📄 requirements.txt       # Dependencies list
 ├── 📄 README.md              # Project documentation
 ├── 📂 images                 # Image assets (if applicable)
⚙️ Filters & Functionality
✅ Filters Available
Price Range: Select minimum and maximum price.

Rating: Filter products by rating (2★ to 5★).

Category: Filter accessories by categories.

Brand: Multi-select brands to refine results.

🔥 Recommendation Logic
TF-IDF Vectorization: Text features are extracted from the product title, category, brand, and features.

Cosine Similarity: Products are ranked by similarity scores.

Accessory Filtering: Only accessories matching the category and brand filters are displayed.

📊 Dataset Details
Columns: product_title, category, brand, price, rating, review_count, features, image_url, is_accessory

Data Cleaning:

Missing prices replaced with the median price.

Non-numeric values are coerced to NaN.

Missing ratings and review counts filled with 0.

Lists are properly formatted using ast.literal_eval().

💡 Future Enhancements
🛒 Add-to-Cart Feature: Allow users to save products to a wishlist or cart.

📊 Product Comparisons: Enable side-by-side comparison of selected products.

🔥 Real-time Data: Integrate with live product APIs for up-to-date recommendations.

📚 Dependencies
The project requires the following Python libraries:

text
Copy
Edit
streamlit
pandas
numpy
scikit-learn
fuzzywuzzy
To install them, run:

bash
Copy
Edit
pip install -r requirements.txt
📩 Contributing
Contributions are welcome! Feel free to fork the project, create a new branch, and submit a pull request.

📜 License
This project is licensed under the MIT License.
