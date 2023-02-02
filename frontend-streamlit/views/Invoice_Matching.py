import streamlit as st
import extra_streamlit_components as stx
from PIL import Image
import os
import pandas as pd
from pretty_notification_box import notification_box
from streamlit_modal import Modal
from tools.utility import df_to_grid, add_vertical_space, display_pdf, check_payment_and_click_status

dirname = os.path.dirname(os.path.dirname(__file__))
asset_path = os.path.abspath(os.path.join(dirname, 'assets/'))
data_path = os.path.abspath(os.path.join(dirname, 'data/'))


class InvoiceMatching:
    class Model:
        pageTitle = "Invoice Matching"
        titleInvoiceMatching = "## Invoice Matching"
        titleTab1 = "## Match Invoices"
        titleTab2 = "## Invoicing Errors"
        titleTab3 = "## Invoice Level Info"

    def view(self, model):
        with st.sidebar:
            st.markdown("---")
        chosen_tab = stx.tab_bar(data=[
            stx.TabBarItemData(id=1, title="Match Invoices", description="Match Invoices"),
            stx.TabBarItemData(id=2, title="Invoicing Errors", description="Get all the info about invoicing errors."),
            stx.TabBarItemData(id=3, title="Invoice Level Info", description="The master table at the invoice level"),
        ], default=1)
        # Develop Tab 1
        "<------------------------------------------------------------------------------------------------------------>"
        if chosen_tab == '1':
            val = stx.stepper_bar(steps=["step 1", "step 2", "step 3"])
            if val == 0:
                st.info(f" In step 1, you need to select what you pay for "
                        f"(Select any additional charges you want to pay for)")
                option = st.selectbox('Select the INCOTerms',
                                      ('Dont know', 'Ex Works (EXW)', 'Free Carrier (FCA)', 'Free Alongside Ship (FAS)',
                                       'Free On Board (FOB)', 'Cost and Freight (CFR)',
                                       'Cost, Insurance and Freight (CIF)', 'Carriage Paid To (CPT)',
                                       'Carriage and Insurance Paid To (CIP)', 'Delivered At Place (DAP)',
                                       'Delivered At Place Unloaded (DPU)', 'Delivered Duty Paid (DDP)'))

                st.write('You selected:', option)
                ## Todo
            if val == 1:
                st.info(f" In step 2, you need to upload the files that you want to match")
                uploaded_files = st.file_uploader("Choose your PDF/CSV files", accept_multiple_files=True)
                for uploaded_file in uploaded_files:
                    bytes_data = uploaded_file.read()
                    st.write("filename:", uploaded_file.name)
                    # st.write(bytes_data)
                    ## Todo
            if val == 2:
                st.info(f" In step 3, you need to fill in your contracted free time")
                ## Todo
                st.info("Skip this step and click on match invoice button below")
                st.button("Match Invoice")
        # Develop Tab 2
        "<------------------------------------------------------------------------------------------------------------>"
        if chosen_tab == '2':
            col1, col2, col3, col4, col5, col6, col7 = st.columns(7, gap="medium")
            with col1:
                with st.container():
                    im = Image.open(os.path.join(asset_path, 'Yellow-Info-Resized.jpg'), "r")
                    st.image(im, use_column_width="auto", output_format="auto")
                    st.markdown("<h2 style='text-align: center; color: black;'>Info</h2>",
                                unsafe_allow_html=True)
                    with st.expander("Expand"):
                        st.write("The number of identifiers in the invoices that were flagged were 5. "
                                 "Please take a detailed look in the table below")

            with col4:
                with st.container():
                    im = Image.open(os.path.join(asset_path, 'Red-Error-Resized.jpg'), 'r')
                    st.image(im, use_column_width="auto", output_format="auto")
                    st.markdown("<h2 style='text-align: center; color: black;'>Errors</h2>",
                                unsafe_allow_html=True)
                    with st.expander("Expand"):
                        st.write("The number of identifiers in the invoices that had errors were 7. "
                                 "Please take a detailed look in the table below")
            with col7:
                with st.container():
                    im = Image.open(os.path.join(asset_path, 'Green-Matched-Resized.jpg'), 'r')
                    st.image(im, use_column_width="auto", output_format="auto")
                    st.markdown("<h2 style='text-align: center; color: black;'>Matches</h2>",
                                unsafe_allow_html=True)
                    with st.expander("Expand"):
                        st.write("The number of identifiers in the invoices that matched were 14. "
                                 "Please take a detailed look in the table below")
            add_vertical_space(10)
            df = pd.read_csv(os.path.join(data_path, 'Sample-Invoice-Identifiers-Table.csv'))
            df_to_grid(df, 650, 'sel_row')
            col1, col2, col3, col4, col5 = st.columns(5, gap="medium")
            if st.session_state.sel_row:
                try:
                    with col1:
                        id_no = st.session_state.sel_row["selectedRows"][0]["Invoice Numbers"]
                        st.write(id_no)
                        add_vertical_space(10)
                        pdf = os.path.join(data_path, (str(id_no) + '.pdf'))
                        display_pdf(pdf)
                    with col4:
                        add_vertical_space(40)
                        charges = ["Basic Ocean Freight", "Garments On Hangers Service"]
                        selected = st.multiselect('Select the charges you want to ignore', charges)
                        if selected:
                            notification_box(icon='info', title='Attention',
                                             textDisplay=f"You have selected the following charges {selected}",
                                             externalLink=None, url=None, styles=None, key='notification_box_charge_sel')
                    with col5:
                        add_vertical_space(42)
                        st.button("Save")
                except (IndexError, UnboundLocalError, AttributeError):
                    print("No Invoice ID is selected yet")
                    notification_box(icon='info', title='Attention',
                                     textDisplay='No Invoice ID has been selected yet. Please select an invoice ID '
                                                 'to display and edit the invoice below', externalLink=None,
                                     url=None,
                                     styles=None, key='notification_box_not_sel')
            else:
                pass
        # Develop Tab 3
        "<------------------------------------------------------------------------------------------------------------>"
        if chosen_tab == '3':
            add_vertical_space(3)
            st.markdown("<h2 style='text-align: center; color: blue;'>Invoice Master Table</h2>",
                        unsafe_allow_html=True)
            add_vertical_space(7)
            df_invoice = pd.read_csv(os.path.join(data_path, 'Invoice-Level-Info-Table.csv'))
            df_to_grid(df_invoice, 1000, 'sel_row_table2')
            add_vertical_space(5)
            modal = Modal("Edit Payment status", key='modal')
            open_modal = st.button("Change Payment Status and Update Details", key='modal_button',
                                   on_click=check_payment_and_click_status())
            if open_modal:
                if st.session_state.sel_row_table2["selectedRows"][0]["Payment Status"] == "Unpaid":
                    modal.open()
            if modal.is_open():
                with modal.container():
                    st.text_input("Enter payment reference details")
                    add_vertical_space(1)
                    st.write("OR")
                    add_vertical_space(1)
                    st.file_uploader("Upload payment details")
                    st.button("Save")
                    st.button("Save and send payment details to vendor")
