import streamlit as st
import extra_streamlit_components as stx
import streamlit.components.v1 as components
import os
import pandas as pd
from pretty_notification_box import notification_box
from tools.utility import add_vertical_space, df_to_grid, send_email, msg_to_html
from tools.constants import (SMTP_SERVER_ADDRESS, PORT, SENDER_ADDRESS, SENDER_PASSWORD)


dirname = os.path.dirname(os.path.dirname(__file__))
asset_path = os.path.abspath(os.path.join(dirname, 'assets/'))
data_path = os.path.abspath(os.path.join(dirname, 'data/'))


class DisputeManagement:
    class Model:
        pageTitle = "Dispute Management"
        titleInvoiceMatching = "## Dispute Management"
        titleTab1 = "## Dispute Shipment Files"
        titleTab2 = "## Dispute Table"
        titleTab3 = "## Email Dashboard"

    def view(self, model):
        with st.sidebar:
            st.markdown("---")
        chosen_tab = stx.tab_bar(data=[
            stx.TabBarItemData(id=1, title="Dispute Shipment Files", description="Raise disputes"),
            stx.TabBarItemData(id=2, title="Email Dashboard",
                               description="View email threads and details, send emails and close disputes"),
            stx.TabBarItemData(id=3, title="Dispute Table",
                               description="Get all the info at a Dispute ID level.")], default=1)
        # Develop the first Tab
        "<------------------------------------------------------------------------------------------------------------>"
        if chosen_tab == '1':
            st.info("Upload the shipment files you want to dispute")
            uploaded_file = st.file_uploader("Choose your PDF/CSV files", accept_multiple_files=False)
            # bytes_data = uploaded_file.read()
            # st.write("filename:", uploaded_file.name)
            # st.write(bytes_data)
            add_vertical_space(5)
            dispute_mapping = {'Incorrect Rates':
                                   ['Contractual rate not applied', 'Container rolled by carrier',
                                    'Agreed free time not applied', 'Charged due to delay by carrier'],
                               'Already Paid': ['Duplicate Invoice', 'Payment made to vendor',
                                                'Payment made to terminal'],
                               'Incorrect Payer': [],
                               'Missing Information': ['Time of Departure/Arrival', 'Place of receipt/destination',
                                                       'Reference Number Missing', 'Container number missing',
                                                       'Share more invoice details']}
            selected_reason = st.selectbox('Select the dispute reason', list(dispute_mapping.keys()))
            if selected_reason:
                notification_box(icon='info', title='Attention',
                                 textDisplay=f"You have selected {selected_reason}. "
                                             f"Now select the category below for {selected_reason}",
                                 externalLink=None, url=None, styles=None, key='notification_box_reason')
            add_vertical_space(5)
            selected_cat = st.selectbox(f'Select the dispute category for {selected_reason}.',
                                        dispute_mapping[selected_reason])
            if selected_cat:
                notification_box(icon='info', title='Attention',
                                 textDisplay=f"You have selected the {selected_cat} "
                                             f"category for the {selected_reason} reason for dispute.",
                                 externalLink=None, url=None, styles=None, key='notification_box_cat')
            add_vertical_space(5)
            st.info("Click on the button below to raise a dispute")
            add_vertical_space(2)
            st.button("Raise Dispute")
            ## Todo
        # Develop Tab 2
        "<------------------------------------------------------------------------------------------------------------>"
        if chosen_tab == '2':
            with st.form("Triakis Email Service"):
                subject = st.text_input(label="Subject", placeholder="Please enter the subject")
                fullName = st.text_input(label='Full Name', placeholder="Please enter the full Name")
                email = st.text_input(label="Email Id", placeholder="Please enter the full email address")
                text = st.text_input(label="Email text", placeholder="Please enter the email text here")
                attachment = st.file_uploader("Attachment")
                submit_res = st.form_submit_button(label='Send')

                if submit_res:
                    extra_info = """-------------------\nEmail address of receiver {}
                    \nSender full name {}\n--------------""".format(
                        email, fullName)

                    message = extra_info + text

                    send_email(sender=SENDER_ADDRESS, password=SENDER_PASSWORD, receiver=email,
                               smtp_server=SMTP_SERVER_ADDRESS, smtp_port=PORT, email_message=message, subject=subject,
                               attachment=attachment)
        # Develop Tab 3
        "<------------------------------------------------------------------------------------------------------------>"
        if chosen_tab == '3':
            add_vertical_space(3)
            st.markdown("<h2 style='text-align: center; color: blue;'>Dispute Master Table</h2>",
                        unsafe_allow_html=True)
            add_vertical_space(7)
            df = pd.read_csv(os.path.join(data_path, 'DisputeID-Level-Info-Table.csv'))
            df_to_grid(df, 1500, 'sel_row_table3')
            col1, col2, col3, col4, col5 = st.columns(5, gap="medium")
            if st.session_state.sel_row_table3:
                try:
                    with col1:
                        id_no = st.session_state.sel_row_table3["selectedRows"][0]["Dispute_ID"]
                        st.write(id_no)
                        add_vertical_space(10)
                        html_path = os.path.join(data_path, "dispute_thread_1.html")
                        p = open(html_path)
                        thread = components.html(p.read(), width=700, height=700, scrolling=True)
                    with col4:
                        add_vertical_space(30)
                        attachments_list = ["dispute-attachments-1", "dispute-attachments-2", "dispute-attachments-3"]
                        selected = st.multiselect('Select the attachments you want to download', attachments_list)
                        if selected:
                            notification_box(icon='info', title='Attention',
                                             textDisplay=f"You have selected the following attachments {selected}",
                                             externalLink=None, url=None, styles=None,
                                             key='notification_box_attachments_sel')
                    with col5:
                        add_vertical_space(32)
                        st.button("Download")
                except (IndexError, UnboundLocalError, AttributeError):
                    print("No Dispute ID is selected yet")
                    notification_box(icon='info', title='Attention',
                                     textDisplay='No Dispute ID has been selected yet. Please select a Dispute ID '
                                                 'to display the thread and download the attachments', externalLink=None,
                                     url=None,
                                     styles=None, key='notification_box_dispute_not_sel')
            else:
                pass

