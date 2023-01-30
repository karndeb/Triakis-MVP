import streamlit as st
from streamlit_modal import Modal
from tools.utility import df_to_grid, add_vertical_space, display_pdf


class ModalTest:
    class Model:
        pageTitle = "Test"

    def view(self, model):
        col1, col2, col3 = st.columns(3, gap="medium")
        with col1:
            pass
            # id_no = st.session_state.sel_row["selectedRows"][0]["Invoice Numbers"]
            # st.write(id_no)
            # add_vertical_space(10)
            # pdf = os.path.join(data_path,
            #                    (str(id_no) + '.pdf'))
            # display_pdf(pdf)
        with col2:
            pass
        with col3:
            add_vertical_space(30)
            modal = Modal("Demo Modal", key='12345')
            open_modal = st.button("Open")
            if open_modal:
                modal.open()
            if modal.is_open():
                with modal.container():
                    st.write("Text goes here")
