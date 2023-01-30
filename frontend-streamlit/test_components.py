# Import the wrapper function from your package
from components.streamlit_button_card import st_button_card
import streamlit as st

# st.title("Testing Streamlit custom components - Button Card")
# Add Streamlit widgets to define the parameters for the Button Card
Body = "The no of invoicing errors is 10. Please click on the expand button to get a detailed view"
Title = "Invoice Errors"
card = st_button_card(body=Body, title=Title)
st.write(card)
