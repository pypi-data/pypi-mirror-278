#!/usr/bin/env python3

# -*- coding: utf-8 -*-

'''
.. module:: file_utilities
   :platform: Unix, Windows
   :synopsis: This module provides utilities for file operations.

.. moduleauthor:: Lalith Kumar Shiyam Sundar  <lalith.shiyamsundar@meduniwien.ac.at>

'''

# Your code here

import base64
import os
import random
import string
from datetime import datetime

import psutil
import requests
import streamlit as st
from d3blocks import D3Blocks
from streamlit_image_comparison import image_comparison


# Local functions
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def create_directory(directory_path: str) -> None:
    """
    Creates a directory as specified
    :type directory_path: str
    :param directory_path: The directory to create
    """
    if not os.path.exists(directory_path):
        os.mkdir(directory_path)


def get_date_time():
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")
    return dt_string


def generate_random_ID(length=6):
    """Generate a random string of fixed length."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def display_gif(gif_path: str, gif_description: str = "alt text"):
    palceholder = st.empty()
    file_ = open(gif_path, "rb")
    contents = file_.read()
    data_url = base64.b64encode(contents).decode("utf-8")
    file_.close()

    palceholder.markdown(
        f'<p style="text-align:center;">'
        f'<img src="data:image/gif;base64,{data_url}" alt={gif_description} width="500" >'
        f'</p>',
        unsafe_allow_html=True
    )
    return palceholder


def get_number_of_possible_jobs(process_memory: int, process_threads: int) -> int:
    """
    Gets the number of available jobs based on system specifications and process parameters
    :param process_memory: Specify how much memory a process needs
    :param process_threads: Specify how many threads a process needs
    :return: Number of possible concurrent jobs as integer number
    """

    # Calculates minimum memory and thread number for process
    min_memory = process_memory * 1024 * 1024 * 1024  # GB
    min_threads = process_threads

    # Get currently available resources
    available_memory = psutil.virtual_memory().available
    available_threads = psutil.cpu_count()

    # Calculate number (integer) of possible jobs based on memory and thread number
    possible_jobs_memory = available_memory // min_memory
    possible_jobs_threads = available_threads // min_threads

    # Get the smallest value to determine number of jobs
    number_of_jobs = min(possible_jobs_memory, possible_jobs_threads)

    # Set number of jobs to -1, if it was 0 before
    if number_of_jobs == 0:
        number_of_jobs = -1

    return number_of_jobs


def plot_external_html(html_path: str):
    plot_file = open(html_path)
    plot = plot_file.read()
    st.markdown(plot, unsafe_allow_html=True)
    plot_file.close()


def display_external_html(html_directory: str):
    html_file = open(html_directory)
    st.components.v1.html(html_file.read())
    html_file.close()


def display_image_comparison(image1: str, image2: str, label1: str, label2: str):
    col_left, col_center, col_right = st.columns([1, 10, 1])
    with col_center:
        image_comparison(
            img1=image1,
            img2=image2,
            label1=label1,
            label2=label2,
            width=400
        )


def display_images_comparison_d3(image1: str, image2: str):
    d3 = D3Blocks()
    d3.imageslider(image1, image2, showfig=True, scale=True, figsize=[269, 821], filepath='./media/comparison.html',
                   background="black")
