# Dastarkhwan: Content-Based Food Recommendation System

A sophisticated food recommendation system that leverages content-based filtering and vector similarity to suggest personalized food items to users based on their preferences.

## 🍽️ Project Overview

Dastarkhwan is a Django-based web application that recommends food items to users by analyzing food content features and user preferences. The system employs advanced vector embeddings and similarity search techniques to provide personalized recommendations that improve as users interact with the platform.

## ✨ Key Features

- **User Preference Learning**: Captures user food preferences through an interactive survey
- **Content-Based Filtering**: Recommends food items based on ingredient similarity and content features
- **Real-time Recommendation Updates**: User embeddings dynamically update based on interactions with recommended items
- **Vector Similarity Search**: Uses FAISS (Facebook AI Similarity Search) for efficient high-dimensional vector similarity searches
- **Visual Food Representation**: Integrates with Pexels API to display relevant food images

## 🛠️ Technology Stack

- **Backend**: Django 5.1
- **Database**: SQLite
- **Vector Database**: FAISS for efficient similarity search
- **Data Processing**: NumPy, Pandas
- **APIs**: Pexels API for food images
- **Frontend**: HTML, CSS, JavaScript

## 📋 Project Structure

```
Content-Based-System/
├── RecApp/                      # Main application directory
│   ├── data/                    # Data storage
│   ├── management/              # Django management commands
│   ├── migrations/              # Database migrations
│   ├── static/                  # Static files (CSS, JS, images)
│   ├── templates/               # HTML templates
│   │   ├── dashboard.html       # Recommendation dashboard
│   │   ├── home.html            # Landing page
│   │   ├── login.html           # Login form
│   │   ├── signup.html          # Signup form
│   │   └── survey.html          # Food preference survey
│   ├── vector_db/               # Vector database files
│   │   ├── faiss_handler.py     # FAISS index handler
│   │   ├── item_index.faiss     # Pre-computed FAISS index
│   │   ├── load_vector_db.py    # Scripts to load vectors
│   │   └── titles.txt           # Mapping of titles to vectors
│   ├── admin.py                 # Admin panel configuration
│   ├── apps.py                  # App configuration
│   ├── models.py                # Database models
│   ├── signals.py               # Django signals
│   ├── urls.py                  # URL routing
│   ├── utils.py                 # Utility functions
│   └── views.py                 # View controllers
├── System/                      # Django project settings
│   ├── settings.py              # Project settings
│   ├── urls.py                  # Project URL configuration
│   └── wsgi.py                  # WSGI configuration
├── manage.py                    # Django management script
└── db.sqlite3                   # SQLite database
```

## 🧠 Recommendation Algorithm

The system implements a sophisticated content-based recommendation approach:

1. **Food Item Embeddings**: Each food item is represented as a high-dimensional vector capturing its key attributes including ingredients and preparation methods.

2. **User Profile Creation**: When a user completes the initial preference survey, the system creates a user embedding by averaging the embeddings of selected food items.

3. **Similarity Search**: The FAISS library efficiently searches for food items with embeddings most similar to the user's embedding.

4. **Recommendation Updates**: As users interact with recommended items, their profile embedding is updated using a weighted combination formula:
   ```
   new_user_embedding = 0.7 * old_user_embedding + 0.3 * clicked_item_embedding
   ```

5. **Normalized Vectors**: All embeddings are L2-normalized to ensure consistent similarity calculations.

## 🔄 User Workflow

1. **Registration**: Users create an account
2. **Preference Survey**: Users select food items they enjoy from various categories
3. **Initial Recommendations**: System generates personalized food recommendations
4. **Interaction**: Users explore and interact with recommendations
5. **Profile Refinement**: System continuously improves recommendations based on user interactions

## 🚀 Setting Up the Project

1. **Clone the repository**
   ```
   git clone https://github.com/Mirza-Abdul-Wasay5704/Content-Based-System.git
   cd Content-Based-System
   ```

2. **Create a virtual environment**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```
   pip install django numpy pandas faiss-cpu requests
   ```

4. **Set up API keys**
   - Get a Pexels API key from https://www.pexels.com/api/
   - Add it to your environment variables or update in settings.py

5. **Run database migrations**
   ```
   python manage.py migrate
   ```

6. **Start the development server**
   ```
   python manage.py runserver
   ```

7. **Access the application**
   Open your browser and navigate to http://127.0.0.1:8000/

## 🔗 Future Enhancements

- **Hybrid Recommendation System**: Integrate collaborative filtering to improve recommendations
- **Advanced NLP**: Implement deeper natural language processing for better ingredient analysis
- **Mobile App**: Develop a companion mobile application
- **Social Features**: Add sharing and social recommendation capabilities
- **Nutrient Analysis**: Include nutritional information in recommendations

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Contributors

- Mirza Abdul Wasay Uddin 
- Maisum Abbas
- Nihal Ali

## 📧 Contact

For any questions or suggestions, please reach out to 
[m.a.wasayuddin143@gmail.com](mailto:m.a.wasayuddin143@gmail.com),
[k224129@nu.edu.pk](mailto:k224129@nu.edu.pk),
[k224054@nu.edu.pk](mailto:k224054@nu.edu.pk).
