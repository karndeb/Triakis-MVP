from st_aggrid import AgGrid, GridOptionsBuilder
import streamlit as st
from pretty_notification_box import notification_box
import base64
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.mime.application import MIMEApplication
from tools.msgtohtml_module import Msgtohtml


def df_to_grid(df, height=None, table_id=None):
    options_builder = GridOptionsBuilder.from_dataframe(df)
    options_builder.configure_selection(selection_mode="single",
                                        use_checkbox=True, groupSelectsChildren=False, groupSelectsFiltered=False)
    options_builder.configure_pagination(enabled=True, paginationAutoPageSize=True, paginationPageSize=10)
    grid_options = options_builder.build()
    return AgGrid(df, grid_options, height=height, fit_columns_on_grid_load=True, key=table_id)


def add_vertical_space(num_lines: int = 1):
    """Add vertical space to your Streamlit app."""
    for _ in range(num_lines):
        st.write("")


def display_pdf(file):
    """Display pdf in an iframe in your streamlit app"""
    # Opening file from file path
    with open(file, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # Iframe the PDF
    pdf_display = F'<iframe src="data:application/pdf;base64,' \
                  F'{base64_pdf}" width="700" height="900" type="application/pdf"></iframe>'

    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)


def check_payment_and_click_status():
    """ Callback function during modal button click. """
    # display a warning if the user clicked on paid invoice or information that invoice hasn't been selected
    try:
        if st.session_state.sel_row_table2 is None:
            notification_box(icon='info', title='Attention',
                             textDisplay='No Invoice ID has been selected yet. Please select an unpaid invoice '
                                         'to change payment status and update details', externalLink=None,
                             url=None,
                             styles=None, key='notification_box')
        elif st.session_state.sel_row_table2["selectedRows"][0]["Payment Status"] == "Paid":
            st.warning("This invoice is already paid. The change payment status button below won't work. "
                       "Please select an unpaid invoice")
    except (IndexError, UnboundLocalError, AttributeError):
        st.warning("No Invoice ID is selected yet")


def send_email(sender, password, receiver, smtp_server, smtp_port, email_message, subject, attachment=None):
    message = MIMEMultipart()
    message['To'] = Header(receiver)
    message['From'] = Header(sender)
    message['Subject'] = Header(subject)
    message.attach(MIMEText(email_message, 'plain', 'utf-8'))
    if attachment:
        att = MIMEApplication(attachment.read(), _subtype="txt")
        att.add_header('Content-Disposition', 'attachment', filename=attachment.name)
        message.attach(att)
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.ehlo()
    server.login(sender, password)
    text = message.as_string()
    server.sendmail(sender, receiver, text)
    server.quit()


def msg_to_html(path):
    html_res = Msgtohtml
    return html_res(path).email2html()
