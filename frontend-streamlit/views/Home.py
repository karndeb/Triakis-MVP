import streamlit as st
from PIL import Image
import os

dirname = os.path.dirname(os.path.dirname(__file__))
asset_path = os.path.abspath(os.path.join(dirname, 'assets/'))


class Home:
    class Model:
        pageTitle = "About Triakis"

    def view(self, model):
        with st.sidebar:
            st.markdown("---")
        col1, col2, col3 = st.columns(3, gap="medium")
        with col2:
            size = 300, 300
            im = Image.open(os.path.join(asset_path, 'Original-Logo-Symbol.png'), 'r')
            im.thumbnail(size, Image.ANTIALIAS)
            # st.header(model.pageTitle)
            st.image(im, caption="Triakis", use_column_width="auto", output_format="auto")
        st.write('At Triakis, we empower businesses to manage procurement through paradigmn shifting '
                 'technological innovation. By enabling business to analyze and control their '
                 'finances with ease, business can save thousands of man hours & focus on being truly '
                 'customer centric')

