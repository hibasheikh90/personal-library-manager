# Description: A simple Streamlit app to manage a digital library of books.
import json
import streamlit as st
from pathlib import Path
import random

# 📁 JSON file to store books
LIBRARY_FILE = "library_data.json"

# 🌆 Image Handling: Online Image + Local Fallback
LIBRARY_IMAGE_URL = "https://images.pexels.com/photos/159711/books-bookstore-book-reading-159711.jpeg"
LOCAL_IMAGE_PATH = "library_cover.jpg"

def get_library_image():
    return LOCAL_IMAGE_PATH if Path(LOCAL_IMAGE_PATH).exists() else LIBRARY_IMAGE_URL

# 📥 Load books from file
def load_library():
    try:
        with open(LIBRARY_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# 💾 Save books to file
def save_library(library):
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

# ➕ Add a book
def add_book(library, title, author, year, genre, read_status):
    library.append({
        "title": title,
        "author": author,
        "year": year,
        "genre": genre,
        "read": read_status
    })
    save_library(library)

# 🗑 Remove a book
def remove_book(library, title):
    for book in library:
        if book["title"].lower() == title.lower():
            library.remove(book)
            save_library(library)
            return True
    return False

# 🔍 Search books
def search_books(library, query):
    return [book for book in library if query.lower() in book["title"].lower() or query.lower() in book["author"].lower()]

# 📊 Statistics
def calculate_statistics(library):
    total_books = len(library)
    read_books = sum(1 for book in library if book["read"])
    read_percentage = (read_books / total_books * 100) if total_books > 0 else 0
    return total_books, read_percentage

# 🎲 Random Book Suggestion
def get_random_book(library):
    return random.choice(library) if library else None

# 🎨 UI Configuration
st.set_page_config(page_title="📖 My Smart Library", page_icon="📚", layout="wide")

# 🌟 Sidebar Menu
st.sidebar.title("📚 Library Manager")
menu = st.sidebar.radio("📌 Menu", ["🏠 Home", "➕ Add Book", "🗑 Remove Book", "🔍 Search Books", "📚 View Library", "📊 Statistics", "🎲 Random Book"])

# 📥 Load Library Data
library = load_library()

# 🌟 Home Page
if menu == "🏠 Home":
    st.title("📖 Welcome to Your Digital Library")
    st.image(get_library_image(), use_container_width=True)
    st.write("""
        📚 Manage your personal book collection effortlessly.
        ➕ Add books
        🔍 Search for books
        📊 Track your reading progress
        🎲 Get a random book suggestion
    """)

# ➕ Add Book
elif menu == "➕ Add Book":
    st.title("➕ Add a New Book")
    with st.form("add_book_form"):
        title = st.text_input("📖 Book Title")
        author = st.text_input("✍️ Author")
        year = st.number_input("📅 Year", min_value=0, max_value=2100, step=1)
        genre = st.text_input("🎭 Genre")
        read_status = st.checkbox("✅ Mark as Read")
        submitted = st.form_submit_button("📚 Add Book")
        if submitted:
            add_book(library, title, author, year, genre, read_status)
            st.success(f"✅ '{title}' has been added!")

# 🗑 Remove Book
elif menu == "🗑 Remove Book":
    st.title("🗑 Remove a Book")
    title = st.text_input("📖 Enter Book Title")
    if st.button("🗑 Remove Book"):
        if remove_book(library, title):
            st.success(f"✅ '{title}' has been removed!")
        else:
            st.error("❌ Book not found!")

# 🔍 Search Books
elif menu == "🔍 Search Books":
    st.title("🔍 Search for a Book")
    query = st.text_input("🔎 Enter title or author")
    if st.button("🔍 Search"):
        results = search_books(library, query)
        if results:
            st.subheader(f"📖 Found {len(results)} Books:")
            for book in results:
                status = "✅ Read" if book["read"] else "📖 Unread"
                st.markdown(f"**📖 {book['title']}** - *{book['author']}* ({book['year']}) [{book['genre']}] - {status}")
        else:
            st.warning("❌ No books found!")

# 📚 View Library
elif menu == "📚 View Library":
    st.title("📚 Your Library Collection")
    if library:
        st.subheader(f"📖 Total Books: {len(library)}")
        for book in library:
            status = "✅ Read" if book["read"] else "📖 Unread"
            st.write(f"- **📖 {book['title']}** by *{book['author']}* ({book['year']}) - {book['genre']} - {status}")
    else:
        st.warning("📭 Your library is empty!")

# 📊 Statistics
elif menu == "📊 Statistics":
    st.title("📊 Library Statistics")
    total_books, read_percentage = calculate_statistics(library)
    col1, col2 = st.columns(2)
    col1.metric("📚 Total Books", total_books)
    col2.metric("📖 Read Percentage", f"{read_percentage:.2f}%")
    st.progress(read_percentage / 100)

# 🎲 Random Book Suggestion
elif menu == "🎲 Random Book":
    st.title("🎲 Get a Random Book Suggestion")
    book = get_random_book(library)
    if book:
        status = "✅ Read" if book["read"] else "📖 Unread"
        st.subheader(f"📖 {book['title']}")
        st.write(f"✍️ {book['author']} ({book['year']}) - {book['genre']} - {status}")
    else:
        st.warning("📭 No books in your library yet!")