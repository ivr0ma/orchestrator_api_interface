import streamlit as st
import aiohttp
import asyncio

def todo_api_base_url():
    return "http://todo_sqlite:80"

def url_shortener_api_base_url():
    return "http://short_url:80"

# Todo API functions
async def fetch_todo_items():
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{todo_api_base_url()}/items") as response:
            return await response.json()

async def create_todo_item(data):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{todo_api_base_url()}/items", json=data) as response:
            return await response.json()

async def update_todo_item(item_id, data):
    async with aiohttp.ClientSession() as session:
        async with session.put(f"{todo_api_base_url()}/items/{item_id}", json=data) as response:
            return await response.json()

async def delete_todo_item(item_id):
    async with aiohttp.ClientSession() as session:
        async with session.delete(f"{todo_api_base_url()}/items/{item_id}") as response:
            return await response.text()

# URL Shortener API functions
async def shorten_url(full_url):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{url_shortener_api_base_url()}/shorten", json={"url": full_url}) as response:
            return await response.json()

async def fetch_url_stats(short_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{url_shortener_api_base_url()}/stats/{short_id}") as response:
            return await response.json()

def main():
    st.title("Combined Interface: Todo List & URL Shortener")

    menu = ["Todo List", "URL Shortener"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Todo List":
        st.subheader("Todo List Management")

        todo_action = st.radio("Choose Action", ["View Items", "Add Item", "Update Item", "Delete Item"])

        if todo_action == "View Items":
            st.write("Fetching all todo items...")
            items = asyncio.run(fetch_todo_items())
            if items:
                for item in items:
                    st.write(f"ID: {item['id']}, Title: {item['title']}, Completed: {item['completed']}")
            else:
                st.write("No items found.")

        elif todo_action == "Add Item":
            title = st.text_input("Title")
            description = st.text_area("Description")
            completed = st.checkbox("Completed")
            if st.button("Add Item"):
                new_item = {
                    "title": title,
                    "description": description,
                    "completed": completed
                }
                result = asyncio.run(create_todo_item(new_item))
                st.success(f"Item added: {result}")

        elif todo_action == "Update Item":
            item_id = st.number_input("Item ID", min_value=1, step=1)
            title = st.text_input("New Title")
            description = st.text_area("New Description")
            completed = st.checkbox("Completed")
            if st.button("Update Item"):
                updated_item = {
                    "title": title,
                    "description": description,
                    "completed": completed
                }
                result = asyncio.run(update_todo_item(item_id, updated_item))
                st.success(f"Item updated: {result}")

        elif todo_action == "Delete Item":
            item_id = st.number_input("Item ID", min_value=1, step=1)
            if st.button("Delete Item"):
                result = asyncio.run(delete_todo_item(item_id))
                st.success(f"Item deleted: {result}")

    elif choice == "URL Shortener":
        st.subheader("URL Shortener Management")

        url_action = st.radio("Choose Action", ["Shorten URL", "View Stats"])


        if url_action == "Shorten URL":
            full_url = st.text_input("Enter the URL to shorten")
            if st.button("Shorten URL"):
                if full_url:
                    result = asyncio.run(shorten_url(full_url))
                    if "short_url" in result:
                        st.success(f"Short URL: {result['short_url']}")
                    else:
                        st.error("Failed to shorten URL. Please check the input.")
                else:
                    st.error("Please enter a valid URL.")

        elif url_action == "View Stats":
            short_id = st.text_input("Enter the Short ID")
            if st.button("Get Stats"):
                if short_id:
                    result = asyncio.run(fetch_url_stats(short_id))
                    if "short_id" in result and "full_url" in result:
                        st.write(f"Short ID: {result['short_id']}")
                        st.write(f"Full URL: {result['full_url']}")
                    else:
                        st.error("Stats not found for the given Short ID.")
                else:
                    st.error("Please enter a valid Short ID.")

if __name__ == "__main__":
    main()
