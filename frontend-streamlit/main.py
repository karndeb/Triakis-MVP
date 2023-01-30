import streamlit as st
from st_on_hover_tabs import on_hover_tabs
from views.Home import Home
from views.Invoice_Matching import InvoiceMatching
from views.modal_test import ModalTest


st.set_page_config(page_title="Triakis", page_icon="assets/Favicon-Original.ico", layout="wide",
                   menu_items={'Get Help': 'https://www.extremelycoolapp.com/help',
                               'Report a bug': "https://www.extremelycoolapp.com/bug",
                               'About': "# This is a header. This is an *extremely* cool app!"})

st.markdown('<style>' + open('./tools/hover-style.css').read() + '</style>', unsafe_allow_html=True)


class Model:
    menuTitle = "Freight Audit and Payments Platform"
    module1 = "About Triakis"
    module2 = "Invoice Matching"
    module3 = "Dispute"
    module4 = "Rate"
    module5 = "Negotiation"
    module6 = "Payments"
    module7 = "Analytics"
    module8 = "User Guide"
    module9 = "Feedback"
    module10 = "Support"

    menuIcon = "menu"
    icon1 = "home"
    icon2 = "receipt"
    icon3 = "email"
    icon4 = "money"
    icon5 = "savings"
    icon6 = "payments"
    icon7 = "analytics"
    icon8 = "info"
    icon9 = "reviews"
    icon10 = "help"


def view(model):
    with st.sidebar:
        pages = on_hover_tabs(tabName=[model.module1, model.module2, model.module3, model.module4, model.module5,
                                       model.module6, model.module7, model.module8, model.module9, model.module10],
                             iconName=[model.icon1, model.icon2, model.icon3, model.icon4, model.icon5, model.icon6,
                                       model.icon7, model.icon8, model.icon9, model.icon10],
                             styles={'navtab': {'background-color': '#111',
                                                'color': '#818181',
                                                'font-size': '18px',
                                                'transition': '.3s',
                                                'white-space': 'nowrap',
                                                'text-transform': 'uppercase'},
                                     'tabOptionsStyle': {':hover :hover': {'color': 'off-white',
                                                                           'cursor': 'pointer'}},
                                     'iconStyle': {'position': 'fixed',
                                                   'left': '7.5px',
                                                   'text-align': 'left'},
                                     'tabStyle': {'list-style-type': 'none',
                                                  'margin-bottom': '30px',
                                                  'padding-left': '30px'}}, default_choice=0,
                             key="1")

    if pages == model.module1:
        Home().view(Home.Model())
        logout_widget()

    if pages == model.module2:
        InvoiceMatching().view(InvoiceMatching.Model())
        logout_widget()

    # if pages == model.module3:
    #     ModalTest().view(ModalTest.Model())
    #     logout_widget()


def logout_widget():
    with st.sidebar:
        st.text("User: Karn Deb")
        st.text("Version: 0.0.1")
        st.button("Logout")
        st.markdown("---")


view(Model())





