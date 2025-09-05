import streamlit as st
from PIL import Image

st.set_page_config(
    page_title='Home',
    page_icon='🍛'
)

image_path = 'images/logo_curry_company.png' 
image = Image.open(image_path)
st.sidebar.image(image, width=210)

st.markdown(
    """
    # Curry Company Growth Dashboard
    ## Welcome to the Curry Company Growth Dashboard! 🍛📈
    
    This dashboard is designed to provide insights into the growth and performance of Curry Company. Here, you can explore various metrics related to delivery operations, customer satisfaction, and overall business trends.
    
    ### Features:
    - **Delivery Performance**: Analyze delivery times, distances, and efficiency.
    - **Customer Satisfaction**: Monitor ratings and feedback from customers.
    - **Operational Insights**: Understand traffic patterns, city-wise performance, and festival impacts.
    
    ### How to Use:
    - Navigate through different sections using the sidebar.
    - Apply filters to customize your view based on dates, traffic conditions, and more.
    - Visualize data through interactive charts and maps for better understanding.
    
    We hope this dashboard helps you make informed decisions and drives the growth of Curry Company!
    
    ---
    """,
    unsafe_allow_html=True  
)