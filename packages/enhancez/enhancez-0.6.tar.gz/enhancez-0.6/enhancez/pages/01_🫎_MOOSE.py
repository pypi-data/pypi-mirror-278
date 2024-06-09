import os
import subprocess
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor

import enhancez.file_utilities as utility
import requests
import streamlit as st
from enhancez.constants import MEDIA
from moosez.resources import AVAILABLE_MODELS
from streamlit_lottie import st_lottie_spinner

# Add CSS for theme purposes
css = '''
<style>
    section.main > div {max-width:75rem}
</style>
'''
st.markdown(css, unsafe_allow_html=True)


# Local function to load Lottie animations from URL
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


# Local function
def prep_moose_folder_structure(temp_dir: str, uid: str) -> str:
    """
    Prepares the folder structure for MOOSE
    :type temp_dir: str
    :param temp_dir: The temporary directory
    :type uid: str
    :param uid: The unique identifier
    :return: The path to the folder structure
    """
    parent_dir = os.path.dirname(temp_dir)
    moose_dir = os.path.join(parent_dir, 'MOOSE-' + uid)
    utility.create_directory(moose_dir)

    # Move the entire temp_dir into moose_dir
    new_temp_dir = os.path.join(moose_dir, os.path.basename(temp_dir))
    os.rename(temp_dir, new_temp_dir)

    return moose_dir


# Function to create a ZIP file of the moose_dir with a progress bar
def create_zip_file(dir_to_zip: str) -> str:
    zip_filename = dir_to_zip + ".zip"
    file_list = []
    for root, dirs, files in os.walk(dir_to_zip):
        for file in files:
            file_list.append(os.path.join(root, file))

    total_files = len(file_list)
    progress_bar = st.progress(0)

    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for i, file in enumerate(file_list):
            zipf.write(file, os.path.relpath(file, dir_to_zip))
            progress_bar.progress((i + 1) / total_files)

    return zip_filename


# Function to read a chunk of the file
def read_chunk(file_path, start, size):
    with open(file_path, 'rb') as f:
        f.seek(start)
        return f.read(size)


# Function to read file in parallel with a progress bar
def read_file_in_parallel(file_path, chunk_size):
    file_size = os.path.getsize(file_path)
    total_chunks = file_size // chunk_size + (file_size % chunk_size > 0)

    file_content = bytearray()
    progress_bar = st.progress(0)

    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(read_chunk, file_path, i * chunk_size, chunk_size)
            for i in range(total_chunks)
        ]
        for i, future in enumerate(futures):
            file_content.extend(future.result())
            progress_bar.progress((i + 1) / total_chunks)

    return bytes(file_content)


# Load the Lottie animation
lottie_url = "https://lottie.host/df92ac92-265f-490a-926d-419e5401f44d/803gCHDUDL.json"
lottie_animation = load_lottieurl(lottie_url)

# Initialize session state
if 'file_uploaded' not in st.session_state:
    st.session_state.file_uploaded = False
if 'temp_dir' not in st.session_state:
    st.session_state.temp_dir = None
if 'file_path' not in st.session_state:
    st.session_state.file_path = None
if 'moose_dir' not in st.session_state:
    st.session_state.moose_dir = None
if 'zip_file' not in st.session_state:
    st.session_state.zip_file = None
if 'file_downloaded' not in st.session_state:
    st.session_state.file_downloaded = False

# Tool description
st.title(MEDIA['MOOSE']['tag_line'], anchor='center')
st.write(MEDIA["MOOSE"]["description"])

# Get the logo of moose from MEDIA
st.image(MEDIA["MOOSE"]["logo"], use_column_width='auto')

# Upload the image
st.subheader("Upload your image to MOOSE: ", divider='violet')
uploaded_file = st.file_uploader("Only one DICOM series ZIP file or a NIFTI image allowed (.nii or .nii.gz)",
                                 type=["zip", "nii", "nii.gz"])

if uploaded_file is not None and not st.session_state.file_uploaded:
    # Create a temporary directory with date versioning
    current_dir = os.path.dirname(os.path.abspath(__file__))
    uid = utility.get_date_time() + "_" + utility.generate_random_ID()
    temp_dir = os.path.join(current_dir, 'temp' + uid)
    utility.create_directory(temp_dir)

    # Save the uploaded file to the temp directory
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Check if the file is a ZIP file (DICOM)
    if uploaded_file.type == "application/zip":
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        # Remove the zip file
        os.remove(file_path)

    # Prepare the folder structure for MOOSE
    moose_dir = prep_moose_folder_structure(temp_dir, uid)

    # Update session state
    st.session_state.file_uploaded = True
    st.session_state.temp_dir = temp_dir
    st.session_state.file_path = file_path
    st.session_state.moose_dir = moose_dir

if st.session_state.file_path:
    st.write(f"Uploaded file: {os.path.basename(st.session_state.file_path)}")

# Select models to run
st.subheader("Choose the model(s) to run: ", divider='violet')
options = st.multiselect(
    "Please wait until the model tags are visible. Available models",
    AVAILABLE_MODELS,
    AVAILABLE_MODELS[0]
)

st.write(
    'Remember the models are run sequentially, so the time taken will be the sum of all the models selected. Please '
    'be patient and do not close the browser tab until all models are processed. Models will be executed in '
    'the following order: ')
st.write(options)

# Button to run the models
if st.session_state.file_uploaded and options:
    if st.button("Run MOOSE 🦌"):
        with st.container():
            lottie_placeholder = st.empty()
            timer_text = st.empty()
            start_time = time.time()

            total_models = len(options)
            with st_lottie_spinner(lottie_animation, height=200, width=200, key="lottie_spinner"):
                for i, model in enumerate(options):
                    # Process the file with the selected model
                    moose_cmd = f"moosez -d {st.session_state.moose_dir} -m {model}"
                    process = subprocess.Popen(moose_cmd, shell=True)

                    # Wait for the process to complete while updating elapsed time
                    while process.poll() is None:
                        time.sleep(1)  # Adjust the sleep time if needed
                        elapsed_time = time.time() - start_time
                        hours, rem = divmod(elapsed_time, 3600)
                        minutes, seconds = divmod(rem, 60)
                        timer_text.text(f"Elapsed time: {int(hours):02}:{int(minutes):02}:{int(seconds):02}")

                    # After the process completes, update elapsed time one final time
                    elapsed_time = time.time() - start_time
                    hours, rem = divmod(elapsed_time, 3600)
                    minutes, seconds = divmod(rem, 60)
                    timer_text.text(f"Elapsed time: {int(hours):02}:{int(minutes):02}:{int(seconds):02}")

            st.success("All models processed successfully!")

            # Create a ZIP file of the moose_dir with a progress bar
            st.subheader("Packing your MOOSE'd data! 🦌🎉")

            zip_file = create_zip_file(st.session_state.moose_dir)
            st.session_state.zip_file = zip_file

            st.subheader("Almost there...Preparing for download... 📦🚚📤")
            # Read the ZIP file in parallel with a progress bar
            chunk_size = 1024 * 1024  # 1MB chunks
            file_content = read_file_in_parallel(st.session_state.zip_file, chunk_size)

            # Provide download button for the ZIP file
            btn = st.download_button(
                label="Download now! 📥",
                data=file_content,
                file_name=os.path.basename(st.session_state.zip_file),
                mime="application/zip"
            )
            st.session_state.file_downloaded = True

# # Clean up the temp directory and files after the download
# if st.session_state.file_downloaded:
#     if st.session_state.moose_dir:
#         st.write(f"Removing directory: {st.session_state.moose_dir}")
#         shutil.rmtree(st.session_state.moose_dir)
#     if st.session_state.zip_file:
#         st.write(f"Removing file: {st.session_state.zip_file}")
#         os.remove(st.session_state.zip_file)
#     st.session_state.file_downloaded = False  # Reset the flag
#
#     # Delay cleanup to ensure download completes
#     time.sleep(5)
