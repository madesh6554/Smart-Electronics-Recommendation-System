# 🔍 Smart Product Recommendation System

## 📌 Overview
The **Smart Product Recommendation System** is a Streamlit-based web application that provides personalized product recommendations based on user queries. It leverages **TF-IDF vectorization** and **cosine similarity** to identify similar products and recommend relevant accessories. Users can apply filters such as **price range, rating, brand, and category** to refine their search.

✅ **Live Demo:** Smart Electronics Recommendation System

---

## 🚀 Features

- 🔎 **Product Search:** Search for products by name and get similar product recommendations.
- 🎯 **Accessory Suggestions:** Recommend relevant accessories for the selected product.
- 📊 **Advanced Filtering:** Filter products by:
    - Price range  
    - Rating  
    - Category and brand  
- 📄 **Product Details:** View product details, including price, rating, review count, and key features.
- 📈 **Responsive UI:** Clean and user-friendly interface with responsive product cards.
- ⚡ **Efficient Performance:** Uses caching with `st.cache_data` for optimized performance.

---

## 🛠️ Tech Stack

### **Frontend**
- Streamlit (Python-based UI framework)

### **Backend**
- `pandas` for data handling
- `numpy` for numerical operations
- `scikit-learn` for vectorization and cosine similarity

### **Data Processing**
- `fuzzywuzzy` for approximate string matching
- `TfidfVectorizer` for text-based product similarity

### **Visualization**
- Dynamic and interactive UI with Streamlit components

---

## 🔧 Installation & Usage

### ⚙️ 1. Clone the Repository
```bash
git clone <YOUR_REPO_LINK>
cd smart-product-recommendation-system
