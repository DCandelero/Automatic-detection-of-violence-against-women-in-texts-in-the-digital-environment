import streamlit as st

# Streamlit page config
st.set_page_config(page_title='dvaw_annotation', page_icon=':violence', layout="wide")

st.title('Image Analysis')

st.sidebar.header('Image Analysis')

container = st.container()
container.write("This is inside the container")
st.write("This is outside the container")

# Now insert some more in the container
container.write("This is inside too")