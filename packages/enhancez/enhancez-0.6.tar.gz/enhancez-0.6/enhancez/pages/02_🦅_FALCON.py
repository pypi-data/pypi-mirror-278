import os
import subprocess
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor

import enhancez.file_utilities as utility
import requests
import streamlit as st
from enhancez.constants import MEDIA
from streamlit_lottie import st_lottie_spinner

# Add CSS for theme purposes
css = '''
<style>
    section.main > div {max-width:75rem}
</style>
'''
st.markdown(css, unsafe_allow_html=True)


# Function to load Lottie animations from URL
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


# Function to create a ZIP file of the directory with a progress bar
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
lottie_url = "https://lottie.host/7baca5bb-59d6-47c1-b7a6-fc65cf840959/m1I0eApzPU.json"
lottie_animation = load_lottieurl(lottie_url)

# Initialize session state
if 'file_uploaded' not in st.session_state:
    st.session_state.file_uploaded = False
if 'temp_dir' not in st.session_state:
    st.session_state.temp_dir = None
if 'file_path' not in st.session_state:
    st.session_state.file_path = None
if 'zip_file' not in st.session_state:
    st.session_state.zip_file = None
if 'file_downloaded' not in st.session_state:
    st.session_state.file_downloaded = False
if 'falconz_dir' not in st.session_state:
    st.session_state.falconz_dir = None

# Tool description
st.title(MEDIA["FALCON"]["tag_line"], anchor='center')
st.write(MEDIA["FALCON"]["description"])

# Get the logo of FALCON from MEDIA
st.image(MEDIA["FALCON"]["logo"], use_column_width='auto')

# Upload the image
st.subheader("Upload your image to FALCON: ", divider='violet')
uploaded_file = st.file_uploader(
    "Only one 4D DICOM series ZIP file or a 3D NIFTI series ZIP file or a 4D NIFTI image allowed (.nii or .nii.gz)",
    type=["zip", "nii", "nii.gz"])

if uploaded_file is not None and not st.session_state.file_uploaded:
    # Create a temporary directory with date versioning
    current_dir = os.path.dirname(os.path.abspath(__file__))
    uid = utility.get_date_time() + "_" + utility.generate_random_ID()
    temp_dir = os.path.join(current_dir, 'temp_' + uid)
    utility.create_directory(temp_dir)

    # Save the uploaded file to the temp directory
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    if uploaded_file.type == "application/zip":
        # Handle ZIP file: Unzip and set directory for FALCON
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        os.remove(file_path)  # Remove the original ZIP file after extraction

        # Find the first directory inside the temp_dir
        unzipped_dir = None
        for item in os.listdir(temp_dir):
            item_path = os.path.join(temp_dir, item)
            if os.path.isdir(item_path):
                unzipped_dir = item_path
                break

        if unzipped_dir is None:
            st.error("Failed to find the unzipped directory inside the temporary directory.")
            st.stop()

        # Use the unzipped directory as the -d argument
        st.session_state.falconz_dir = unzipped_dir

    else:
        # Handle single 4D NIFTI file
        st.session_state.falconz_dir = file_path

    # Update session state
    st.session_state.file_uploaded = True
    st.session_state.temp_dir = temp_dir
    st.session_state.file_path = file_path

if st.session_state.file_path:
    st.write(f"Uploaded file: {os.path.basename(st.session_state.file_path)}")

st.subheader('Please select the registration parameters: ', divider='violet')
col1, col2 = st.columns(2)

with col1:
    registration_type = st.radio(
        "Registration type:",
        ["Rigid", "Affine", "Deformable"],
        horizontal=True,
    )

with col2:
    registration_mode = st.radio(
        "Mode (Cruise: Standard speed/accurate) Fast: (High speed/can be less accurate):",
        ["Cruise", "Fast"],
        horizontal=True,
    )

col1, col2 = st.columns(2)

with col1:
    starting_frame = st.number_input("Starting frame (For automatic calculation, don't change the default value):",
                                     value=99, min_value=0, step=1)

with col2:
    reference_frame = st.number_input("Reference frame (Default is last frame and -1 indicates that):", value=-1,
                                      min_value=-1, step=1)

st.subheader('Run the registration: ', divider='violet')
st.warning(f"FALCON will run with the following parameters: "
           f"Registration type: {registration_type} | Mode: {registration_mode} | Starting frame: {starting_frame} | "
           f"Reference frame: {reference_frame}")
st.write(
    'FALCON is quite fast, but if you are running total-body PET datasets, you can expect it to take a few minutes to run. '
    'Please be patient and do not refresh the page while the FALCON is running.')

# Button to run the models
if st.session_state.file_uploaded:
    if st.button("Run FALCON"):
        with st.container():
            lottie_placeholder = st.empty()
            timer_text = st.empty()
            start_time = time.time()
            with st_lottie_spinner(lottie_animation, height=200, width=200, key="lottie_spinner"):
                falcon_cmd = (f"falconz -d {st.session_state.falconz_dir} -rf {reference_frame} -sf {starting_frame}"
                              f" -r {registration_type.lower()} -m {registration_mode.lower()}")
                process = subprocess.Popen(falcon_cmd, shell=True)

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

            st.success("🦅 FALCON has performed motion correction successfully!")

            st.subheader("Packing your FALCON'd data! 🦅🎉")

            # Determine the location of the FALCONZ-* directory
            falconz_folder = None
            if uploaded_file.type == "application/zip":
                # Look for FALCONZ-* inside the temp_dir
                for item in os.listdir(st.session_state.temp_dir):
                    item_path = os.path.join(st.session_state.temp_dir, item)
                    if os.path.isdir(item_path) and item.startswith("FALCONZ-"):
                        falconz_folder = item_path
                        break
            else:
                # Look for FALCONZ-* in the same level as temp_dir
                parent_dir = os.path.dirname(st.session_state.temp_dir)
                for item in os.listdir(parent_dir):
                    item_path = os.path.join(parent_dir, item)
                    if os.path.isdir(item_path) and item.startswith("FALCONZ-"):
                        falconz_folder = item_path
                        break

            if falconz_folder is None:
                st.error("Failed to find the FALCONZ directory after processing.")
                st.stop()

            # ZIP the FALCONZ-* directory
            zip_file = create_zip_file(falconz_folder)
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
#     if st.session_state.temp_dir:
#         shutil.rmtree(st.session_state.temp_dir)
#     if st.session_state.zip_file:
#         os.remove(st.session_state.zip_file)
#     st.session_state.file_downloaded = False  # Reset the flag
#
#     # Delay cleanup to ensure download completes
#     time.sleep(5)
