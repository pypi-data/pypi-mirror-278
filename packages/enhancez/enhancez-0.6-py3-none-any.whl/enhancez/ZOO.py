#!/usr/bin/env python3

# -*- coding: utf-8 -*-

'''
.. module:: enhancez
   :platform: Unix, Windows
   :synopsis: This is the main module for enhancez.

.. moduleauthor:: Lalith Kumar Shiyam Sundar  <lalith.shiyamsundar@meduniwien.ac.at>

'''

# Import necessary libraries

import streamlit as st

# Add custom CSS for theme purposes
css = '''
<style>
    section.main > div {
        max-width: 75rem;
    }
    .header-text {
        color: #ea45cf;
        font-size: 2.5em;
        font-weight: bold;
        text-align: center;
    }
    .sub-header {
        color: #ffffff;
        font-size: 1.5em;
        text-align: center;
        margin-bottom: 20px;
    }
    .intro-text {
        font-size: 1.2em;
        line-height: 1.6;
        margin-bottom: 40px;
    }
    .cta-button {
        display: flex;
        justify-content: center;
        margin-top: 30px;
    }
    .cta-button button {
        background-color: #ea45cf;
        color: #ffffff;
        font-size: 1.2em;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
</style>
'''
st.markdown(css, unsafe_allow_html=True)


def run():
    st.image("https://github.com/LalithShiyam/ENHANCE-ZOO/blob/master/Images/ENHANCE-ZOO-logo.png?raw=true",
             use_column_width='auto')

    st.header('ENHANCE-ZOO: A one-stop shop for PET imaging analysis', divider='rainbow')
    st.subheader('Bringing state-of-the-art PET analytics to your browser')

    intro_text = """
Welcome to ENHANCE-ZOO — your centralized hub for exploring the powerful ENHANCE-PET software suite. Whether you're a non-programmer or a busy physician, ENHANCE-ZOO is designed with you in mind. You don't need to install anything or open a terminal. Simply upload your data, and let our platform handle the rest. With ENHANCE-ZOO, you can seamlessly try out our cutting-edge PET imaging tools directly from your browser. Dive into our suite of applications by clicking on the various tools listed in the sidebar. We are excited to see how ENHANCE-ZOO can assist you in revolutionizing your PET imaging workflows!"""

    st.markdown(f'<p class="intro-text">{intro_text}</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="intro-text">Cheers from the ENHANCE-PET Team</p>', unsafe_allow_html=True)


if __name__ == '__main__':
    run()
