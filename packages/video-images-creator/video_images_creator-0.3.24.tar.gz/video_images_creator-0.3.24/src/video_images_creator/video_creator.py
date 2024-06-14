import subprocess
import cv2
import numpy as np
import os
from pathlib import Path
import shutil
import secrets
import string
import math
from PIL import Image, ImageDraw, ImageFont
from urllib.request import urlopen
import re
import glob
from math import floor
import azure.cognitiveservices.speech as speechsdk
import pkg_resources
import wave
import concurrent.futures
import contextlib

import requests
from pydub import AudioSegment
from pydub.silence import split_on_silence


def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(secrets.choice(characters) for _ in range(length))
    return random_string


def add_alpha_channel(img):
    if img.shape[2] == 4:  # Image already has an alpha channel
        return img
    else:  # Add alpha channel to the image
        alpha_channel = np.ones((img.shape[0], img.shape[1], 1), dtype=img.dtype) * 255  # Fully opaque
        return np.concatenate((img, alpha_channel), axis=-1)

def set_transparency(img, opacity):
    # Ensure the image has an alpha channel
    img_with_alpha = add_alpha_channel(img)
    # Adjust the alpha channel to set the desired opacity
    #img_with_alpha[:, :, 3] = img_with_alpha[:, :, 3] * opacity 

    if opacity == 1.0:
        img_with_alpha[:, :, 3] = 255
    else:
        img_with_alpha[:, :, 3] = 128
    return img_with_alpha


def sort_key(filename):
    # Split the filename into its numerical components, assuming the format is "prefix_number_number.extension"
    parts = re.split(r'[_\.]', filename)  # This splits the filename by underscores and the dot before the extension
    # Convert the numerical parts to integers for proper sorting, ignoring the non-numerical parts
    return [int(part) for part in parts if part.isdigit()]


def add_images_in_frameset_v2(blended_roi_img_url_dict, background, directory_name, current_index, total_frames, transparency):

    x_coordinate_increement = 0 
    initial_x_coordinate = 0
    feature_images_urls = list(blended_roi_img_url_dict.keys())
    image_file_prefix = ""
    if total_frames == 180:
        image_file_prefix = "_preview_frames" 

    if len(feature_images_urls) == 5:
        ###
        x_coordinate_increement = 0
        initial_x_coordinate = 335
        background = cv2.imread(pkg_resources.resource_filename('video_images_creator', "5featureframe.png"))
    elif len(feature_images_urls) == 4:
        initial_x_coordinate = 713
        background_img_url = "https://testkals.s3.amazonaws.com/4featureframe.png"
    elif len(feature_images_urls) == 3:
        initial_x_coordinate = 985
        background = cv2.imread(pkg_resources.resource_filename('video_images_creator', "3featureframe.png"))
    elif len(feature_images_urls) == 2:
        initial_x_coordinate = 1340
        background_img_url = "https://testkals.s3.amazonaws.com/2featureframe.png" 
    elif len(feature_images_urls) == 1:
        initial_x_coordinate = 1635
        background = cv2.imread(pkg_resources.resource_filename('video_images_creator', "animaionfeature.png"))
    else:
        print("Exit?///") 

    max_index = len(feature_images_urls) - 1
    running_index = 0
    
  
    for feature_images_url in feature_images_urls: 

        x_coordinate = initial_x_coordinate + x_coordinate_increement
        x, y = x_coordinate + 13, 486

        blended_roi = blended_roi_img_url_dict[feature_images_url]["blended_roi"]
        h_o = blended_roi_img_url_dict[feature_images_url]["h_o"]
        w_o = blended_roi_img_url_dict[feature_images_url]["w_o"]


        if running_index == 0 or running_index == max_index:
            blended_roi = set_transparency(blended_roi, transparency)
            #background[y:y+h_o, x:x+w_o] = blended_roi[:, :, :3] 
            overlay_image = blended_roi[..., :3]  # RGB channels
            mask = blended_roi[..., 3:] / 255.0  # Alpha channel normalized

            background[y:y+h_o, x:x+w_o] = (1.0 - mask) * background[y:y+h_o, x:x+w_o] + mask * overlay_image 

        else:
            blended_roi = set_transparency(blended_roi, transparency)
            background[y:y+h_o, x:x+w_o] = blended_roi[:, :, :3]

        running_index = running_index + 1

        x_coordinate_increement = x_coordinate_increement + 626 


    file_name = f'{directory_name}/frame_{current_index}_{total_frames}{image_file_prefix}.jpg' 
    cv2.imwrite(file_name, background)

    current_index_ = current_index

    return ( current_index + 1 )

def create_feature_set_frames_v2(current_index, directory_name, feature_images_urls): 


    current_index = add_blank_background_frames(directory_name, current_index)

    temp_feature_images_urls = feature_images_urls[:1]
    feature_images_url = temp_feature_images_urls[0]
    initial_x_coordinate = 1635
    x_coordinate_increement = 0


    x_coordinate = initial_x_coordinate + x_coordinate_increement

    x, y = x_coordinate + 13, 486
    # Generate the rounded image 


    overlay = read_image(feature_images_url)
    background = cv2.imread(pkg_resources.resource_filename('video_images_creator', "animaionfeature.png"))
    
    x_coordinate = initial_x_coordinate + x_coordinate_increement
    screen_width, screen_height = 545, 1190
    x, y = x_coordinate + 13, 486

    overlay = cv2.resize(overlay, (screen_width, screen_height))
    corner_radius = 30
    mask = create_rounded_mask(overlay, corner_radius)
    # Generate the rounded image
    rounded_image = get_rounded_image(overlay, mask)
    h_o, w_o, _ = rounded_image.shape
    blended_roi = refined_alpha_blend(background[y:y+h_o, x:x+w_o], rounded_image)
    blended_roi_img_url_dict = {}
    #blended_roi_img_url_dict[feature_images_url] = blended_roi

    dict_obj = { "blended_roi": blended_roi, "h_o": h_o, "w_o": w_o }

    blended_roi_img_url_dict[feature_images_url] = dict_obj


    current_index = add_images_in_frameset_v2(blended_roi_img_url_dict, background, directory_name, current_index,12, 0.1) 

    current_index = add_images_in_frameset_v2(blended_roi_img_url_dict, background, directory_name, current_index,12, 0.5) 

    current_index = add_images_in_frameset_v2(blended_roi_img_url_dict, background, directory_name, current_index,120, 1.0) 

    if len(feature_images_urls[:3]) >=3 :

        temp_feature_images_urls = feature_images_urls[:3] 
        temp_feature_images_urls[0], temp_feature_images_urls[1] = temp_feature_images_urls[1], temp_feature_images_urls[0] 

        blended_roi_img_url_dict = {} 
        x_coordinate_increement = 0
        background = cv2.imread(pkg_resources.resource_filename('video_images_creator', "3featureframe.png"))

        for feature_images_url in temp_feature_images_urls: 

            initial_x_coordinate = 985
        

            x_coordinate = initial_x_coordinate + x_coordinate_increement

            x, y = x_coordinate + 13, 486
            # Generate the rounded image 


            overlay = read_image(feature_images_url)
        
            
            x_coordinate = initial_x_coordinate + x_coordinate_increement
            screen_width, screen_height = 545, 1190
            x, y = x_coordinate + 13, 486

            overlay = cv2.resize(overlay, (screen_width, screen_height))
            corner_radius = 30
            mask = create_rounded_mask(overlay, corner_radius)
            # Generate the rounded image
            rounded_image = get_rounded_image(overlay, mask)
            h_o, w_o, _ = rounded_image.shape
            blended_roi = refined_alpha_blend(background[y:y+h_o, x:x+w_o], rounded_image)
            dict_obj = { "blended_roi": blended_roi, "h_o": h_o, "w_o": w_o }
            blended_roi_img_url_dict[feature_images_url] = dict_obj

            x_coordinate_increement = x_coordinate_increement + 650


        current_index = add_images_in_frameset_v2(blended_roi_img_url_dict, background, directory_name, current_index,12, 0.1) 

        current_index = add_images_in_frameset_v2(blended_roi_img_url_dict, background, directory_name, current_index,12, 0.5) 

        current_index = add_images_in_frameset_v2(blended_roi_img_url_dict, background, directory_name, current_index, 120, 1.0)

    if len(feature_images_urls) >= 5:

        temp_feature_images_urls = feature_images_urls[:5] 
        temp_feature_images_urls[0], temp_feature_images_urls[2] = temp_feature_images_urls[2], temp_feature_images_urls[0]


        x_coordinate_increement = 0
        initial_x_coordinate = 400
        background = cv2.imread(pkg_resources.resource_filename('video_images_creator', "5featureframe.png"))
        blended_roi_img_url_dict = {}


        for feature_images_url in temp_feature_images_urls: 

            initial_x_coordinate = 335
            

            x_coordinate = initial_x_coordinate + x_coordinate_increement

            x, y = x_coordinate + 13, 486
            # Generate the rounded image 


            overlay = read_image(feature_images_url)

            
            x_coordinate = initial_x_coordinate + x_coordinate_increement
            screen_width, screen_height = 545, 1190
            x, y = x_coordinate + 13, 486

            overlay = cv2.resize(overlay, (screen_width, screen_height))
            corner_radius = 30
            mask = create_rounded_mask(overlay, corner_radius)
            # Generate the rounded image
            rounded_image = get_rounded_image(overlay, mask)
            h_o, w_o, _ = rounded_image.shape
            blended_roi = refined_alpha_blend(background[y:y+h_o, x:x+w_o], rounded_image)
            dict_obj = { "blended_roi": blended_roi, "h_o": h_o, "w_o": w_o }
            blended_roi_img_url_dict[feature_images_url] = dict_obj

            x_coordinate_increement = x_coordinate_increement + 626

        current_index = add_images_in_frameset_v2(blended_roi_img_url_dict, background, directory_name, current_index,12, 0.1) 

        current_index = add_images_in_frameset_v2(blended_roi_img_url_dict, background, directory_name, current_index,12, 0.5) 

        current_index = add_images_in_frameset_v2(blended_roi_img_url_dict, background, directory_name, current_index,180, 1.0) 

    return current_index


def add_images_in_single_frame(feature_images_url, directory_name, current_index, transparency, frames):
 
    x_coordinate = 1650
    x, y = x_coordinate, 540
    background = cv2.imread(pkg_resources.resource_filename('video_images_creator', "featureframe.png"))


    overlay = read_image(feature_images_url) 
    screen_width, screen_height = 551, 1210
    overlay = cv2.resize(overlay, (screen_width, screen_height)) 
    corner_radius = 30
    mask = create_rounded_mask(overlay, corner_radius)
    rounded_image = get_rounded_image(overlay, mask)
    x, y = 1650, 540
    h_o, w_o, _ = rounded_image.shape 
    blended_roi = refined_alpha_blend(background[y:y+h_o, x:x+w_o], rounded_image) 

    blended_roi = set_transparency(blended_roi, transparency)

    #background[y:y+h_o, x:x+w_o] = blended_roi[:, :, :3] 

    overlay_image = blended_roi[..., :3]  # RGB channels
    mask = blended_roi[..., 3:] / 255.0  # Alpha channel normalized
    
    background[y:y+h_o, x:x+w_o] = (1.0 - mask) * background[y:y+h_o, x:x+w_o] + mask * overlay_image
    
    file_name = f'{directory_name}/frame_{current_index}.jpg' 
    cv2.imwrite(file_name, background)

    current_index_ = current_index

    for i in range(1,frames): 
        index = i + current_index_
        destination = f'{directory_name}/frame_{index}.jpg'
        shutil.copyfile(file_name, destination)
        current_index = current_index + 1 

    


    return current_index


def add_blank_background_frames(directory_name, current_index):
  
    # background = cv2.imread("features/startfeatureframe.png")
    # file_name = f'{directory_name}/frame_{current_index}.jpg' 
    # cv2.imwrite(file_name, background)


    ending_page_image = cv2.imread(pkg_resources.resource_filename('video_images_creator', "startfeatureframe.png"))

    #create original image with cv2 imwrite
    original_file_name = f'{directory_name}/frame_{current_index}_49.jpg'
    cv2.imwrite(original_file_name, ending_page_image)

    # current_index_ = current_index

    # for i in range(1,50): 
    #     index = i + current_index_
    #     destination = f'{directory_name}/frame_{index}.jpg'
    #     shutil.copyfile(original_file_name, destination)
    #     current_index = current_index + 1

    return ( current_index + 1 )


def add_images_in_frameset(feature_images_urls, directory_name, current_index, total_frames, transparency):
 
    x_coordinate_increement = 0 
    initial_x_coordinate = 0

    if len(feature_images_urls) == 5:
        ###
        x_coordinate_increement = 0
        initial_x_coordinate = 400
        background = cv2.imread(pkg_resources.resource_filename('video_images_creator', "5featureframe.png"))
    elif len(feature_images_urls) == 4:
        initial_x_coordinate = 713
        background_img_url = "https://testkals.s3.amazonaws.com/4featureframe.png"
    elif len(feature_images_urls) == 3:
        initial_x_coordinate = 1025
        background = cv2.imread(pkg_resources.resource_filename('video_images_creator', "3featureframe.png"))
    elif len(feature_images_urls) == 2:
        initial_x_coordinate = 1340
        background_img_url = "https://testkals.s3.amazonaws.com/2featureframe.png" 
    elif len(feature_images_urls) == 1:
        initial_x_coordinate = 1650
        background = cv2.imread(pkg_resources.resource_filename('video_images_creator', "animaionfeature.png"))
    else:
        print("Exit?///") 

    max_index = len(feature_images_urls) - 1
    running_index = 0
    
  
    for feature_images_url in feature_images_urls: 

        x_coordinate = initial_x_coordinate + x_coordinate_increement

        x, y = x_coordinate + 13, 486
        overlay = read_image(feature_images_url) 
        screen_width, screen_height = 545, 1190
        overlay = cv2.resize(overlay, (screen_width, screen_height))
        corner_radius = 30
        mask = create_rounded_mask(overlay, corner_radius)
        # Generate the rounded image
        rounded_image = get_rounded_image(overlay, mask)
        h_o, w_o, _ = rounded_image.shape
        blended_roi = refined_alpha_blend(background[y:y+h_o, x:x+w_o], rounded_image)


        if running_index == 0 or running_index == max_index:
            blended_roi = set_transparency(blended_roi, transparency)
            #background[y:y+h_o, x:x+w_o] = blended_roi[:, :, :3] 
            overlay_image = blended_roi[..., :3]  # RGB channels
            mask = blended_roi[..., 3:] / 255.0  # Alpha channel normalized

            background[y:y+h_o, x:x+w_o] = (1.0 - mask) * background[y:y+h_o, x:x+w_o] + mask * overlay_image
        else:
            blended_roi = set_transparency(blended_roi, transparency)
            background[y:y+h_o, x:x+w_o] = blended_roi[:, :, :3] 

        running_index = running_index + 1

        
        #background[y:y+h_o, x:x+w_o] = blended_roi[:, :, :3] 

        #background = overlay_transparent(background, blended_roi, x_coordinate, 650)  # Adjust y-coordinate as needed


        x_coordinate_increement = x_coordinate_increement + 626 


    file_name = f'{directory_name}/frame_{current_index}.jpg' 
    cv2.imwrite(file_name, background)

    current_index_ = current_index

    for i in range(1,total_frames): 
        index = i + current_index_
        destination = f'{directory_name}/frame_{index}.jpg'
        shutil.copyfile(file_name, destination)
        current_index = current_index + 1

    return current_index


def create_starting_frames(current_index, directory_name, ending_page_image, total_frames, image_suffix):

    # if ending_page_image_url == "terminal":
    #     ending_page_image = pkg_resources.resource_filename('video_images_creator', "terminal.png")

    # elif ending_page_image_url == "preterminal":
    #     ending_page_image = pkg_resources.resource_filename('video_images_creator', "preterminal.png")
    # else:
    #     return
    
    #create original image with cv2 imwrite
    if image_suffix != "":
        original_file_name = f'{directory_name}/frame_{current_index}_{total_frames}_{image_suffix}.jpg'
    else:
        original_file_name = f'{directory_name}/frame_{current_index}_{total_frames}.jpg'
    #original_file_name = f'{directory_name}/frame_{current_index}_{total_frames}.jpg'
    cv2.imwrite(original_file_name, ending_page_image)
    # for i in range(1,total_frames): 
    #     index = current_index + i
    #     destination = f'{directory_name}/frame_{index}.jpg'
    #     shutil.copyfile(original_file_name, destination)
    #     #cv2.imwrite(destination, ending_page_image) 

    return (current_index + 1)

def add_images_in_single_frame_V2(feature_images_url, font, directory_name, current_index, feature_title):
    first_image = True 
    background = ''
    x_coordinate = 1590
    overlay = read_image(feature_images_url) 
    screen_width, screen_height = 660, 1419
    x, y = x_coordinate, 370
    background = cv2.imread(pkg_resources.resource_filename('video_images_creator', "featureframe.png"))

    overlay = cv2.resize(overlay, (screen_width, screen_height))  
    
    if first_image == True:
        first_image = False

        corner_radius = 30
        mask = create_rounded_mask(overlay, corner_radius)
        # Generate the rounded image
        rounded_image = get_rounded_image(overlay, mask)


        h_o, w_o, _ = rounded_image.shape 
        blended_roi = refined_alpha_blend(background[y:y+h_o, x:x+w_o], rounded_image) 


        background[y:y+h_o, x:x+w_o] = blended_roi[:, :, :3] 

        # line = feature_title

        # pil_image = Image.fromarray(cv2.cvtColor(background, cv2.COLOR_BGR2RGB))
        # draw = ImageDraw.Draw(pil_image)
        
        # #print(x_coordinate) 
        # #print(len(line))
        # if len(line) > 13: 
        #     x_coordinate = int(max((3840 -  ( len(line) * 40 )  ),0) / 2 ) #tradeoff calc
        # #print(x_coordinate)
        # draw.text((x_coordinate, 1910), line.strip(), font=font, fill=(88, 88, 88))  

        # background = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)


        file_name = f'{directory_name}/frame_{current_index}_180_feature_frames.jpg' 
        cv2.imwrite(file_name, background)

        # current_index_ = current_index

        # for i in range(1,180): 
        #     index = i + current_index_
        #     destination = f'{directory_name}/frame_{index}.jpg'
        #     shutil.copyfile(file_name, destination)
        #     current_index = current_index + 1 

    


    return (current_index + 1)


def add_feature_frames(feature_images_urls, directory_name, current_index, feature_titles):

    index = 0
     # Load the custom font
    font_path = pkg_resources.resource_filename('video_images_creator', 'Rubik-Medium.ttf')
    font_size = 84
    font = ImageFont.truetype(font_path, font_size)
  
    
    for feature_images_url in feature_images_urls:
        current_index = add_images_in_single_frame_V2(feature_images_url, font, directory_name, current_index, feature_titles[index]) 
        index = index + 1 

    return current_index



def build_v2(feature_images_urls, feature_names):

    ensure_required_directories_existis()
    current_index = 1
    folder_name = generate_random_string(10)  
    directory_name = f'images/{folder_name}'
    os.mkdir(directory_name)
    terminal_image_path = pkg_resources.resource_filename('video_images_creator', "terminal.png")
    terminal_image = cv2.imread(terminal_image_path)

    pre_terminal_image_path = pkg_resources.resource_filename('video_images_creator', "preterminal.png")
    preterminal_image = cv2.imread(pre_terminal_image_path)

    current_running_index = create_starting_frames(current_index, directory_name, terminal_image,400) 
    #feature_images_urls = ["https://buildernowassets.azureedge.net/builder-now-beta/uploads/staging/build_card_hero_image/file/103054602/1a0d1594-1e81-4181-b4bb-92d31f197539.png", "https://buildernowassets.azureedge.net/builder-now-beta/uploads/staging/build_card_hero_image/file/103054583/30188996-01e3-4eab-9a36-552f70d1bb73.png", "https://buildernowassets.azureedge.net/builder-now-beta/uploads/staging/build_card_hero_image/file/130179838/d41999b6-b89d-4f3a-988b-3a3dd85dd986.png", "https://buildernowassets.azureedge.net/builder-now-beta/uploads/staging/build_card_hero_image/file/130179842/d9954a75-b307-4839-b634-f18c4e4b7b1a.png", "https://builderbuckets.blob.core.windows.net/builder-now-production/uploads/production/build_card_hero_image/file/40258072/987611d1-19cd-4931-a618-0897aa0d79d1.png", "https://builderbuckets.blob.core.windows.net/builder-now-production/uploads/production/build_card_hero_image/file/40258074/b82fae9a-4d79-45e9-a286-dc6f1b92a0c4.png", "https://builderbuckets.blob.core.windows.net/builder-now-production/uploads/production/build_card_hero_image/file/40258060/5cc635d6-b63a-4b20-929f-cf12eb178765.png"]
    #feature_titles = ["Splash Screen", "User Profile", "Signup/ Login", "Categories/ Sub-Categories", "Order Summary", "Payment Details", "Order Summary"]

    current_running_index = create_starting_frames(current_running_index, directory_name, preterminal_image, 80)
    current_running_index = create_feature_set_frames_v2(current_running_index, directory_name, feature_images_urls)


    current_running_index = add_feature_frames(feature_images_urls, directory_name, current_running_index, feature_names) 

    current_running_index = create_starting_frames(current_running_index, directory_name, preterminal_image, 60)
    current_running_index = create_starting_frames(current_running_index, directory_name, terminal_image, 180) 



    image_files = sorted([f for f in os.listdir(directory_name) if f.endswith(('.jpg', '.png'))], key=sort_key) 

    temp_text_file = f'{directory_name}/temp_ffmpeg_list.txt'

    total_duration = 0


    with open(temp_text_file, 'w') as file:
        for image in image_files:
            # Extract the number of frames from the filename (assuming it's after the last '_')
            frames = int(image.split('_')[-1].split('.')[0])
            duration = frames / 60  # Calculate duration in seconds
            total_duration = total_duration + duration

            # Write the file command for this image
            file.write(f"file '{os.path.join('', image)}'\n")
            # Write the duration command for this image
            file.write(f"duration {duration}\n")

        # For the concat demuxer, the last file should not have a duration specified
        # So, we add the last file entry again without a duration
        file.write(f"file '{os.path.join('', image_files[-1])}'\n")


    run_ffmpeg_v3(directory_name, folder_name, temp_text_file, total_duration) 
    return flush_video_images(directory_name, folder_name)


def synthesize_speech_with_ssml(intro_text, features_intro_text, feature_descriptions, subscription_key, service_region, output_file):
    """
    Synthesizes speech from SSML input and saves the output as an audio file.

    Parameters:
    - subscription_key (str): Azure Cognitive Services Speech subscription key.
    - service_region (str): Azure service region (e.g., "westus").
    - output_file (str): Output audio file path.
    """
    try:
        #print(intro_text)
        #print(feature_descriptions)
        # Create an instance of a speech config with specified subscription key and service region
        speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=service_region)

        # Set the speech synthesis output format
        speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Riff48Khz16BitMonoPcm)

        # Create an audio configuration that points to an output audio file
        audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file)

        # Create a speech synthesizer using the configured speech config and audio config
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

        # Define the SSML with the desired voice, language, and include a break
        ssml = f"""
        <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-GB'>
            <voice name='en-GB-SoniaNeural'>
                {intro_text}.
                <break time='500ms'/>
                Over the next few minutes we will walk through the app.
                <break time='200ms'/>
                {features_intro_text}
                <break time='760ms'/> 
                {feature_descriptions}
            </voice>
        </speak>
        """
        # Synthesize the speech from the SSML
        result = synthesizer.speak_ssml_async(ssml).get()

        # Check the result
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            return 0, "Audio saved successfully."  # Success code and message
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            error_message = f"Speech synthesis canceled: {cancellation_details.reason}"
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    error_message += f" Error details: {cancellation_details.error_details}"
                return 1, error_message  # Error code and message
        return 2, "Synthesis failed for an unknown reason."  # Unexpected error code and message

    except Exception as e:
        return 99, f"An exception occurred: {str(e)}"  # Exception code and message



def convert_to_stereo_48khz_16bit(input_file, output_file):
    """
    Converts an audio file to stereo, with a sample rate of 48 kHz and 16 bits per sample using FFmpeg.

    Parameters:
    - input_file (str): Path to the input audio file.
    - output_file (str): Path where the converted audio file will be saved.

    Returns:
    - None
    """
    # FFmpeg command components
    ffmpeg_cmd = [
        'ffmpeg',
        '-y',
        '-i', f'./{input_file}',  # Input file
        '-ac', '2',
        output_file  # Output file
    ]

    # Run the FFmpeg command
    try:
        subprocess.run(ffmpeg_cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred during conversion: {e}")


def add_pause_with_pydub(input_filename, output_filename, pause_duration_milliseconds):
    # Load the existing audio file
    try:
        sound = AudioSegment.from_wav(input_filename)
        silence = AudioSegment.silent(duration=pause_duration_milliseconds)
        combined = sound + silence
        combined.export(output_filename, format="wav")
        return True 
    except Exception as e:
        print(f"An error occurred: {e}") 
    return False


def combine_wav_files(output_file, input_files):
    # Open the first file to get the parameters
    with wave.open(input_files[0], 'rb') as wav:
        params = wav.getparams()

    # Open the output file
    with wave.open(output_file, 'wb') as outfile:
        outfile.setparams(params)  # Set the parameters to match the input files

        # Go through each input file and append the audio
        for file in input_files:
            with wave.open(file, 'rb') as infile:
                while True:
                    data = infile.readframes(1024)
                    if not data:
                        break
                    outfile.writeframes(data)

def synthesize_text(speech_obj, subscription_key, service_region, tts_audio_folder):

    text = speech_obj["text"]
    audio_index = speech_obj["audio_index"]
    generate_audio = speech_obj["generate_audio"] 
    audio_blob_url = speech_obj["audio_blob_url"]
    output_file = f"{tts_audio_folder}/{audio_index}.wav"

    if generate_audio is True and len(audio_blob_url) > 0:

        try:
            response = requests.get(audio_blob_url)
            # Check if the request was successful
            if response.status_code == 200:
                # Write the content to a local file
                with open(output_file, 'wb') as f:
                    f.write(response.content)
                    return 0, "Audio saved successfully.", output_file, audio_index, speech_obj["type"], speech_obj["step_feature_count"] 
        except Exception as ep:
            return 99, f"An exception occurred: {str(ep)}", "", "", "", ""
        
    speech_config = speechsdk.SpeechConfig(subscription=subscription_key, region=service_region)
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Riff48Khz16BitMonoPcm)
    speech_config.speech_synthesis_voice_name = 'en-GB-SoniaNeural'
    audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

    ssml = f"""
    <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-GB'>
        <voice name='en-GB-SoniaNeural'>
            {text}
        </voice>
    </speak>
    """
    try:
        result = synthesizer.speak_ssml_async(ssml).get()
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            # print("Speech synthesized to [{}] for text [{}]".format(output_file, ssml))
            return 0, "Audio saved successfully.", output_file, audio_index, speech_obj["type"], speech_obj["step_feature_count"]  # Success code and message
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            error_message = f"Speech synthesis canceled: {cancellation_details.reason}"
            #print("Speech synthesis canceled: {}".format(cancellation_details.reason))
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                if cancellation_details.error_details:
                    #print("Error details: {}".format(cancellation_details.error_details))
                    error_message += f" Error details: {cancellation_details.error_details}"
                return 1, error_message, "", "", "", ""  # Error code and message
        return 2, "Synthesis failed for an unknown reason.", "", "","",""  # Unexpected error code and message
    except Exception as e:
        return 99, f"An exception occurred: {str(e)}", "", "", "",""


def get_wav_duration(filename):
    with contextlib.closing(wave.open(filename, 'r')) as file:
        frames = file.getnframes()
        rate = file.getframerate()
        duration = frames / float(rate)
        return duration


def run_parallel_tts_process(all_speech_objs, subscription_key, service_region, tts_audios_folder, process_mode):
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(all_speech_objs)) as executor:
        # Schedule the synthesize_text function to be called for each set of texts
        future_to_text = {executor.submit(synthesize_text, speech_obj, subscription_key, service_region, tts_audios_folder): speech_obj for speech_obj in all_speech_objs}
        for future in concurrent.futures.as_completed(future_to_text):
            text = future_to_text[future]
            try:

                result_code, message, file_name, audio_index, speech_type, set_feature_count = future.result()

                if result_code == 0:
                    #succeeded 
                    duration = get_wav_duration(file_name)
                    min_duration = 3.0
                    if speech_type == "project_intro":
                        min_duration = 8.3 
                        if process_mode == "byscript":
                            min_duration = duration
                    if speech_type == "feature_intro":
                        min_duration = 9.5
                    if duration > min_duration and speech_type in ["feature_description"] and process_mode == "byscript": 
                        duration = duration / set_feature_count
                    if duration < min_duration and speech_type in ["project_intro", "feature_intro", "feature_description"]:
                        seconds_diff = min_duration - duration
                        milli_seconds_diff = seconds_diff * 1000
                        pause_success = add_pause_with_pydub(file_name, file_name, milli_seconds_diff)
                        if pause_success and os.path.exists(file_name) and os.path.getsize(file_name) > 0:
                            duration = min_duration
                            if speech_type in ["feature_description"] and process_mode == "byscript":
                                duration = 5.0

                    speech_obj = [obj for obj in all_speech_objs if obj["audio_index"] == audio_index ]

                    if speech_obj:
                        speech_obj = speech_obj[0]
                        speech_obj["duration"] = duration
                        speech_obj["filename"] = file_name 


            except Exception as exc:
                print(f'Text {text} generated an exception: {exc}') 
                return {} 
            
    return all_speech_objs


def compute_feature_count_stepwise(feature_desriptions):
    current_count = 0
    current_parent = ""
    parents_to_index_counts = {}
    current_index = 0
    for fd in feature_desriptions:
        if fd != "<break time='200ms'/>..":
            current_parent = fd
            parents_to_index_counts[fd] = [current_index]
        else:
            parents_to_index_counts[current_parent].append(current_index)
        current_index = current_index + 1

    step_counts = []

    for ind in range(len(feature_desriptions)): 

        for key,value in parents_to_index_counts.items():
            if ind in value:
                step_counts.append(len(value)) 
    return step_counts     

def build_v3(process_dict):

    feature_images_urls = process_dict["image_urls"] 
    feature_names = process_dict["feature_names"] 
    feature_descriptions = process_dict["feature_desciptions"] 
    feature_ids = process_dict["feature_ids"]
    existing_audios = process_dict["audio_script_blob_urls"] 
    build_card_name = process_dict["project_name"] 
    subscription_key = process_dict["subscription_key"]
    service_region = process_dict["service_region"] 
    intro_text = process_dict["intro_text"]
    preview_screen_text = process_dict["preview_screen_text"]
    preview_feature_image_urls = process_dict["preview_feature_image_urls"]  
    process_mode = process_dict["process_mode"] 

    if process_mode is None:
        process_mode = "legacy"

    ensure_required_directories_existis()
    current_index = 1
    folder_name = generate_random_string(10)  
    directory_name = f'images/{folder_name}/audios'
    os.makedirs(directory_name, exist_ok=True) 

    directory_name = f'images/{folder_name}'
    tts_audios_folder = f'images/{folder_name}/audios'
    tts_output_filename = f'{directory_name}/tts_outfile_name.wav'
    tts_output_2_channel_filename = f'{directory_name}/tts_2_chnl_outfile_name.wav'
    project_intro_text = f"Hey, I am Natasha, We are excited to share with you the prototype for {build_card_name} that we have designed.<break time='500ms'/>"
    feature_intro_text = f"Starting with the {feature_names[0]} users will be able to then interact with {feature_names[1]} and {feature_names[2]} <break time='200ms'/> "
    feature_count_stepwise = compute_feature_count_stepwise(feature_descriptions) 
    print("feature_count_stepwise ", feature_count_stepwise)


    if process_mode == "byscript":
        project_intro_text = f"{intro_text}<break time='100ms'/>"
        feature_intro_text = f"{preview_screen_text}..<break time='600ms'/>"


    pattern = r"[\n\r\t]|<p>|<br>|<b>|</p>|</br>|&nbsp;|&#39;"
    feature_desciption_stripped = ""

    for fd in feature_descriptions:
        feature_desciption_stripped = feature_desciption_stripped + " " + re.sub(pattern, '', fd)

    terminal_image_path = pkg_resources.resource_filename('video_images_creator', "terminal.png")
    terminal_image = cv2.imread(terminal_image_path)

    pre_terminal_image_path = pkg_resources.resource_filename('video_images_creator', "preterminal.png")
    preterminal_image = cv2.imread(pre_terminal_image_path)



    terminal_image_frames = 500 
    preterminal_image_frames = 70 
    if process_mode == "byscript":
        terminal_image_frames = 200
        preterminal_image_frames = 35 

    current_running_index = create_starting_frames(current_index, directory_name, terminal_image, terminal_image_frames, "start_frames") 
    #feature_images_urls = ["https://buildernowassets.azureedge.net/builder-now-beta/uploads/staging/build_card_hero_image/file/103054602/1a0d1594-1e81-4181-b4bb-92d31f197539.png", "https://buildernowassets.azureedge.net/builder-now-beta/uploads/staging/build_card_hero_image/file/103054583/30188996-01e3-4eab-9a36-552f70d1bb73.png", "https://buildernowassets.azureedge.net/builder-now-beta/uploads/staging/build_card_hero_image/file/130179838/d41999b6-b89d-4f3a-988b-3a3dd85dd986.png", "https://buildernowassets.azureedge.net/builder-now-beta/uploads/staging/build_card_hero_image/file/130179842/d9954a75-b307-4839-b634-f18c4e4b7b1a.png", "https://builderbuckets.blob.core.windows.net/builder-now-production/uploads/production/build_card_hero_image/file/40258072/987611d1-19cd-4931-a618-0897aa0d79d1.png", "https://builderbuckets.blob.core.windows.net/builder-now-production/uploads/production/build_card_hero_image/file/40258074/b82fae9a-4d79-45e9-a286-dc6f1b92a0c4.png", "https://builderbuckets.blob.core.windows.net/builder-now-production/uploads/production/build_card_hero_image/file/40258060/5cc635d6-b63a-4b20-929f-cf12eb178765.png"]
    #feature_titles = ["Splash Screen", "User Profile", "Signup/ Login", "Categories/ Sub-Categories", "Order Summary", "Payment Details", "Order Summary"]


    current_running_index = create_starting_frames(current_running_index, directory_name, preterminal_image, preterminal_image_frames, "")
    current_running_index = create_feature_set_frames_v2(current_running_index, directory_name, preview_feature_image_urls)


    current_running_index = add_feature_frames(feature_images_urls, directory_name, current_running_index, feature_names)


    current_running_index = create_starting_frames(current_running_index, directory_name, preterminal_image, 100,"")
    current_running_index = create_starting_frames(current_running_index, directory_name, terminal_image, 250, "") 


    image_files = sorted([f for f in os.listdir(directory_name) if f.endswith(('.jpg', '.png'))], key=sort_key)  

    all_speech_objs = [] 
    
    
    project_intro_speech_obj = {
        "text": project_intro_text,
        "type": "project_intro",
        "uniq_id": "project_intro",
        "audio_index": 0,
        "generate_audio": True,
        "audio_blob_url": "",
        "step_feature_count": 1
    }


    post_intro_speech_obj = {
        "text": "Over the next few minutes we will walk through the app.<break time='200ms'/>",
        "type": "post_intro",
        "uniq_id": "post_intro",
        "audio_index": 1,
        "generate_audio": True,
        "audio_blob_url": "",
        "step_feature_count": 1
    } 

    if process_mode == "legacy":
        all_speech_objs.append(post_intro_speech_obj) 


    features_intro_speech_obj = {
        "text": feature_intro_text,
        "type": "feature_intro",
        "uniq_id": "feature_intro",
        "audio_index": 2,
        "generate_audio": True,
        "audio_blob_url": "",
         "step_feature_count": 1
    } 

    all_speech_objs.append(features_intro_speech_obj)

    audio_index = 3
    feature_index = 0

    feature_desciption_formatted = []

    for fd in feature_descriptions:
        pattern = r"[\n\r\t]|<p>|<br>|<b>|</p>|</br>|&nbsp;|&#39;"
        feature_desciption_ = re.sub(pattern, '', fd)
        #feature_desciption_ = feature_desciption_.replace("<break time='600ms'/>","")
        feature_desciption_formatted.append(feature_desciption_)
        feature_desciption_speech_obj = {
            "text": feature_desciption_,
            "type": "feature_description",
            "uniq_id": feature_ids[feature_index],
            "audio_index": audio_index,
            "generate_audio": not(existing_audios[feature_index] == ""),
            "audio_blob_url": existing_audios[feature_index],
            "step_feature_count": feature_count_stepwise[feature_index]
        }

        audio_index = audio_index + 1
        feature_index = feature_index + 1
        all_speech_objs.append(feature_desciption_speech_obj)

    all_speech_objs = run_parallel_tts_process(all_speech_objs, subscription_key, service_region, tts_audios_folder, process_mode) 

    all_audio_file_names = [item['filename'] for item in all_speech_objs if 'filename' in item]

    combine_wav_files(tts_output_filename, all_audio_file_names)


    temp_text_file = f'{directory_name}/temp_ffmpeg_list.txt'

    total_duration = 0
    current_feature_index = 0 
    total_preview_frames_duration = 0

    # Open a temporary text file to write the file and duration commands for FFmpeg
    with open(temp_text_file, 'w') as file:
        for image in image_files:
            # Extract the number of frames from the filename (assuming it's after the last '_')  

            image_ = image.replace("_feature_frames", "") 
            image_ = image_.replace("_start_frames","")
            image_ = image_.replace("_preview_frames","")
            seconds = 0

            frames = int(image_.split('_')[-1].split('.')[0])
            duration = frames / 60  # Calculate duration in seconds

            if "_feature_frames" in image:
                pattern = r"[\n\r\t]|<p>|<br>|<b>|</p>|</br>|&nbsp;|&#39;" 
                feature_desciption_ = re.sub(pattern, '', feature_descriptions[current_feature_index])  
                #feature_desciption_ = feature_desciption_.replace("<break time='600ms'/>","")
                uniq_id = feature_ids[current_feature_index]

                speech_obj = [obj for obj in all_speech_objs if obj["uniq_id"] == uniq_id ]
                if speech_obj:
                    speech_obj = speech_obj[0]
                    duration = speech_obj["duration"] 


            if "start_frames" in image:
                speech_obj = [obj for obj in all_speech_objs if obj["uniq_id"] == "project_intro" ]
                if speech_obj:
                    speech_obj = speech_obj[0]
                    duration = speech_obj["duration"] 

            if "_preview_frames" in image:
                speech_obj = [obj for obj in all_speech_objs if obj["uniq_id"] == "feature_intro" ]
                if speech_obj:
                    speech_obj = speech_obj[0] 
                    duration_ = speech_obj["duration"] 
                    #print("the duration of _preview_frames ", duration_, " the duff us ", abs(duration_ - 10.2))
                    duration = 5 +  abs(duration_ - 10.2)

          
         
            total_duration = total_duration + duration

            # if "_preview_frames" in image:
            #     total_preview_frames_duration = total_preview_frames_duration + duration

            # Write the file command for this image
            file.write(f"file '{os.path.join('', image)}'\n")

            # Write the duration command for this image
            file.write(f"duration {duration}\n")

            if "_feature_frames" in image:
                current_feature_index = current_feature_index + 1
            #it is a feature frame

    # For the concat demuxer, the last file should not have a duration specified
    # So, we add the last file entry again without a duration
        file.write(f"file '{os.path.join('', image_files[-1])}'\n") 


    # features_intro_text = f"Starting with the {feature_names[0]} users will be able to then interact with {feature_names[0]} and {feature_names[4]}"
    # preview_page_len_diff = abs( total_preview_frames_duration - ( len(features_intro_text) * 0.0645 ) )
    # pause_intro_text_len_ms = int( preview_page_len_diff * 1000 )

    # if pause_intro_text_len_ms > 1000:
    #     features_intro_text = f"Starting with the {feature_names[0]} users will be able to then interact with {feature_names[0]} and {feature_names[4]}.<break time='{pause_intro_text_len_ms}ms'/>"

    # result_code, message = synthesize_speech_with_ssml(project_intro_text, features_intro_text, feature_desciption_stripped, subscription_key, service_region, tts_output_filename)

    # if result_code != 0:
    #     print(f"An error occurred during synthesis. Code: {result_code}")
    #     return flush_video_images(directory_name, folder_name)
    # else:
    #     convert_to_stereo_48khz_16bit(tts_output_filename, tts_output_2_channel_filename)
    #     run_ffmpeg_v4(directory_name, folder_name, temp_text_file, tts_output_2_channel_filename, total_duration) 
    #     return flush_video_images(directory_name, folder_name)

    convert_to_stereo_48khz_16bit(tts_output_filename, tts_output_2_channel_filename)
    run_ffmpeg_v4(directory_name, folder_name, temp_text_file, tts_output_2_channel_filename, total_duration) 
    return flush_video_images(directory_name, folder_name)
        


        



        


   

    








def build(image_file_paths, feature_names, project_name, logo_url):
    ensure_required_directories_existis()
    current_index = 0
    folder_name = generate_random_string(10)  
    directory_name = f'images/{folder_name}' 
    bg_image_path = pkg_resources.resource_filename('video_images_creator', "builderbackground.png") 
    bg_img = cv2.imread(bg_image_path) 
    ending_page_image_path = pkg_resources.resource_filename('video_images_creator', "closingframe_f.png") 
    ending_page_image = cv2.imread(ending_page_image_path) 
    os.mkdir(directory_name) 
    put_project_name(bg_img, project_name, directory_name, logo_url)
    for index in range(len(image_file_paths) - 1):
        if index % 2 == 0:
            current_index = create_right_to_left_movement(image_file_paths[index + 1], image_file_paths[index], current_index, directory_name, project_name, feature_names[index], feature_names[index + 1], bg_img) 
        else:
            current_index = create_left_to_right_movement(image_file_paths[index], image_file_paths[index + 1], current_index, directory_name, project_name, feature_names[index], feature_names[index+1], bg_img) 
        #print("done for feature index ", index)

    create_ending_frames(current_index, directory_name, ending_page_image) 
    #print("done with creation of ending frames")
    run_ffmpeg(directory_name, folder_name) 
    return flush_video_images(directory_name, folder_name) 

def put_project_name(bg_image, project_name, directory_name, logo_url): 

    project_name_x = 80
    logo_to_be_added = False
    # if logo_url:
    #     logo = read_image(logo_url)
    #     logo_height, logo_width, _ = logo.shape
    #     new_logo_width = min(logo_width, 130)
    #     new_logo_height = min(logo_height, 130)
    #     #logo = cv2.resize(logo, (new_logo_width, new_logo_height))  
    #     logo = logo[0:new_logo_height, 0:new_logo_width]
    #     logo_to_be_added = True
    #     if new_logo_width == 130:
    #         project_name_x = 150
    #     else:
    #         project_name_x = project_name_x + int(( 130 - new_logo_width ) * 1.9 )
    
    pil_image = Image.fromarray(cv2.cvtColor(bg_image, cv2.COLOR_BGR2RGB)) 
    draw = ImageDraw.Draw(pil_image)
    font_path = pkg_resources.resource_filename('video_images_creator', 'Rubik-Medium.ttf')
    font_size = 27
    font = ImageFont.truetype(font_path, font_size) 
    draw.text((project_name_x, 40), project_name, font=font, fill=(255, 255, 255)) 
    bg_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    if logo_to_be_added:
        bg_image[20:20+new_logo_height, 10:10+new_logo_width] = logo
    #bg_image[20:20+new_logo_height, 10:10+new_logo_width] = logo
    # Save and return the modified image
    cv2.imwrite(f'{directory_name}/bg_img.jpg', bg_image)   

    image_path = pkg_resources.resource_filename('video_images_creator', "combined_left.jpg")
    bg_image = cv2.imread(image_path)
    pil_image = Image.fromarray(cv2.cvtColor(bg_image, cv2.COLOR_BGR2RGB))   
    draw = ImageDraw.Draw(pil_image)
    draw.text((project_name_x, 40), project_name, font=font, fill=(255, 255, 255))  
    bg_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR) 
    if logo_to_be_added:
        bg_image[20:20+new_logo_height, 10:10+new_logo_width] = logo
    #bg_image[20:20+new_logo_height, 10:10+new_logo_width] = logo
    # Save and return the modified image
    cv2.imwrite(f'{directory_name}/combined_left_new.jpg', bg_image)   

    image_path = pkg_resources.resource_filename('video_images_creator', "combined_right.jpg")
    bg_image = cv2.imread(image_path)
    pil_image = Image.fromarray(cv2.cvtColor(bg_image, cv2.COLOR_BGR2RGB))   
    draw = ImageDraw.Draw(pil_image)
    draw.text((project_name_x, 40), project_name, font=font, fill=(255, 255, 255)) 
    bg_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR) 
    if logo_to_be_added:
        bg_image[20:20+new_logo_height, 10:10+new_logo_width] = logo
    #bg_image[20:20+new_logo_height, 10:10+new_logo_width] = logo
    # Save and return the modified image
    cv2.imwrite(f'{directory_name}/combined_right_new.jpg', bg_image) 
    
def create_ending_frames(current_index, directory_name, ending_page_image):
    for i in range(110): 
        index = current_index + i
        destination = f'{directory_name}/frame_{index}.jpg'
        #shutil.copyfile(img1, destination)
        cv2.imwrite(destination, ending_page_image)


def create_left_to_right_movement(left_image_file_path, right_image_file_path, current_index_, directory_name, project_name, left_screen_name, right_screen_name, bg_img):

    #create images  

    #print("inside left to right movement method")

    left_image_file_name = left_image_file_path
    right_image_file_name = right_image_file_path

    parent_current_index = current_index_
    left_image = build_screen_optimised(left_image_file_name, f'{directory_name}/combined_left_image_{current_index_}.jpg', 455, directory_name, 'left')
    right_image = build_screen_optimised(right_image_file_name, f'{directory_name}/combined_right_image_{current_index_}.jpg', 1179, directory_name, 'right')  

    #print("built parent screens")

    put_text(f'{directory_name}/combined_left_image_with_name_{current_index_}.jpg', left_image, left_screen_name, project_name, 455) 
    put_text(f'{directory_name}/combined_right_image_with_name_{current_index_}.jpg', right_image, right_screen_name, project_name, 1179) 

    #print("added texts")

    # left_image_with_name = build_screen(left_image_file_name, f'{directory_name}/combined_left_image_with_name_{current_index_}.jpg', 455, left_screen_name, True)
    # right_image_with_name = build_screen(right_image_file_name, f'{directory_name}/combined_right_image_with_name_{current_index_}.jpg', 1179, right_screen_name, True) 




    img1 = cv2.imread(left_image)
    img2 = cv2.imread(right_image) 

    #bg_img = read_image("https://builderbuckets.blob.core.windows.net/builder-now-beta/builderbackground.png")





    #these are for feature transitions 
    start_point = np.array([455, 218])  
    end_point = np.array([1179, 218])   


    obj_width = 305
    obj_height = 643


    #  #create 40 copies of image with names
    # current_index = current_index_

    # file_name =  f'combined_left_image_with_name${parent_current_index}.jpg'
    # for i in range(40): 
    #     index = i + current_index_
    #     destination = f'./images/frame_{index}.jpg'
    #     shutil.copyfile(file_name, destination)
    #     current_index = current_index + 1



    #create 20 copies of image without names
    current_index = current_index_

    #create 20 copies of img1

    file_name = f'{directory_name}/combined_left_image_{parent_current_index}.jpg'
    for i in range(20): 
        index = i + current_index_
        destination = f'{directory_name}/frame_{index}.jpg'
        shutil.copyfile(file_name, destination)
        current_index = current_index + 1

    num_frames = 70
    
    #print("added images for left without text")



    temp_current_index = current_index 

    bg_img = cv2.imread(f'{directory_name}/bg_img.jpg')

    for i in range(num_frames):
        t = i / float(num_frames)  

        
        position = (1 - t) * start_point + t * end_point  

        
        img = bg_img.copy()

        
        box1 = img1[int(start_point[1]):int(start_point[1] + obj_height), int(start_point[0]):int(start_point[0] + obj_width)]
        box2 = img2[int(end_point[1]):int(end_point[1] + obj_height), int(end_point[0]):int(end_point[0] + obj_width)] 


        # corner_radius = 30
        # mask = create_rounded_mask(box1, corner_radius)

        # # Generate the rounded image
        # box1 = get_rounded_image(box1, mask) 


        # corner_radius = 30
        # mask = create_rounded_mask(box2, corner_radius)

        # # Generate the rounded image 

        # box2 = get_rounded_image(box2, mask)

        
        transition_obj = (1 - t) * box1 + t * box2 


        transition_obj_h, transition_obj_w, _ = transition_obj.shape

        ch = min(transition_obj_h, int(position[1] + obj_height ) - int(position[1])) 
        cw = min(int(position[0] + obj_width) - int(position[0]), transition_obj_w) 

        img[int(position[1]): int(position[1]) + ch, int(position[0]): int(position[0]) + cw] = transition_obj 

        
        # transition_obj = refined_alpha_blend( img[int(position[1]): int(position[1]) + ch, int(position[0]): int(position[0]) + cw], transition_obj)
        # img[int(position[1]): int(position[1]) + ch, int(position[0]): int(position[0]) + cw] = transition_obj[:, :, :3]  # Only take BGR channels, ignore alpha 

        #frame_index = 76 + i + 2 

        frame_index = temp_current_index + i 
        
        cv2.imwrite(f'{directory_name}/frame_{frame_index}.jpg', img)  

        current_index = current_index + 1



    #create 20 copies of imgage without name 

    #print("created the intermediatory frames")

    current_index_ = current_index

    file_name =  f'{directory_name}/combined_right_image_{parent_current_index}.jpg'
    for i in range(20): 
        index = i + current_index_
        destination = f'{directory_name}/frame_{index}.jpg'
        shutil.copyfile(file_name, destination) 
        current_index = current_index + 1

    current_index_ = current_index


    #print("added images for right")

    file_name =  f'{directory_name}/combined_right_image_with_name_{parent_current_index}.jpg'
    for i in range(40): 
        index = i + current_index_
        destination = f'{directory_name}/frame_{index}.jpg'
        shutil.copyfile(file_name, destination)
        current_index = current_index + 1

    #print("added images for right with name")

   

   

    return current_index


def filter_text(html_str):
    cleaned_text = re.sub(r'<style.*?>.*?</style>|<.*?>', '', html_str, flags=re.DOTALL)

    # Replace HTML entities with their associated characters
    cleaned_text = cleaned_text.replace('&nbsp;', ' ')
    cleaned_text = cleaned_text.replace('\r\n', ' ')  # Replace newline characters with a space
    cleaned_text = cleaned_text.replace('\t', ' ') 

    return cleaned_text


def put_text(combine_file_name, background, sceen_name, project_name, x_coordinate): 

    #print("### put text start")
    background = cv2.imread(background)
    pil_image = Image.fromarray(cv2.cvtColor(background, cv2.COLOR_BGR2RGB)) 
    #print("got pil image")



    #sceen_name = filter_text(sceen_name)
        
    # Load the custom font
    font_path = pkg_resources.resource_filename('video_images_creator', 'Rubik-Medium.ttf')
    title_font_path = pkg_resources.resource_filename('video_images_creator', 'Rubik-Bold.ttf')
    font_size = 59
    font = ImageFont.truetype(title_font_path, font_size)
    draw = ImageDraw.Draw(pil_image) 

    #print("loaded fonts")
    
    max_width = 450  # The maximum width for text 
    y = background.shape[0] - 600
    if x_coordinate != 455:
        lines = []
        words = sceen_name.split()
        #print("words are ", words)
        while words:
            line = ''
            #print("arg1", int(draw.textlength(line + words[0], font=font)), "- max_Width", max_width) 

            if int(draw.textlength(words[0], font=font)) > max_width:
                # Handle words that are too long
                # For now, we'll just append it to lines and continue
                lines.append(words.pop(0))
                continue
            while words and int(draw.textlength(line + words[0], font=font)) <= max_width: 
                #print("inside pop")
                line += (words.pop(0) + ' ')
            lines.append(line) 

        
        
        # Limit to 3 lines
        lines = lines[:3] 
        
        apply_indent = False 
        for i, line in enumerate(lines):
            x = x_coordinate - 450 
            line = line.strip()
            if ( x + len(line) ) >= 740 or apply_indent:
                apply_indent = True 
                x = x - 25
            draw.text((x, y + i*font_size), line.strip(), font=font, fill=(255, 255, 255))  
            #print("added text on right with row",i+1)
    else:
        x = x_coordinate + 350
        draw.text((x, y), sceen_name, font=font, fill=(255, 255, 255))  
        #print("added text on left")


    #add project name
    # if project_name:
    #     font_size = 27
    #     font = ImageFont.truetype(font_path, font_size) 
    #     draw.text((80, 40), project_name, font=font, fill=(255, 255, 255))

    # #add description
    # font_size = 30 
    # font_path = 'features/Rubik-Light.ttf'
    # font = ImageFont.truetype(font_path, font_size)
    # max_width = 580
    # lines = []
    # words = description.split()
    # while words:
    #     line = ''
    #     while words and int(draw.textlength(line + words[0], font=font)) <= max_width:
    #         line += (words.pop(0) + ' ')
    #     lines.append(line)
    
    # # Limit to 3 lines
    # lines = lines[:7]
    
    # y = background.shape[0] - 650
    # for i, line in enumerate(lines):
    #     if x_coordinate == 455:
    #         x = x_coordinate + 335
    #     else:
    #         x = x_coordinate - 600
    #     draw.text((x, y + i*font_size), line.strip(), font=font, fill=(255, 255, 255)) 



    background = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    # Save and return the modified image
    cv2.imwrite(combine_file_name, background) 

    #print("###put text end")



def create_right_to_left_movement(left_image_file_path, right_image_file_path, current_index_, directory_name, project_name, right_screen_name, left_screen_name, bg_img):
    #create images
    left_image_file_name = left_image_file_path
    right_image_file_name = right_image_file_path


    #print("inside left to right movement method")

    #images with no feature name
    parent_current_index = current_index_
    left_image = build_screen_optimised(left_image_file_name, f'{directory_name}/combined_left_image_{current_index_}.jpg', 455, directory_name, 'left')
    right_image = build_screen_optimised(right_image_file_name, f'{directory_name}/combined_right_image_{current_index_}.jpg', 1179, directory_name, 'right') 

    #print("created parent screens")

    #images with feature names
    put_text(f'{directory_name}/combined_left_image_with_name_{current_index_}.jpg', left_image, left_screen_name, project_name, 455) 
    put_text(f'{directory_name}/combined_right_image_with_name_{current_index_}.jpg', right_image, right_screen_name, project_name, 1179) 
    # left_image_with_name = build_screen(left_image_file_name, f'{directory_name}/combined_left_image_with_name_{current_index_}.jpg', 455, left_screen_name, True)
    # right_image_with_name = build_screen(right_image_file_name, f'{directory_name}/combined_right_image_with_name_{current_index_}.jpg', 1179, right_screen_name, True) 

      


    img1 = cv2.imread(left_image)
    img2 = cv2.imread(right_image) 

    #bg_img = read_image("https://builderbuckets.blob.core.windows.net/builder-now-beta/builderbackground.png")

    #these are for feature transitions 
    start_point = np.array([1179, 218])  
    end_point = np.array([455, 218])


    obj_width = 305
    obj_height = 643


    #create 40 copies of image with names
    current_index = current_index_

    file_name =  f'{directory_name}/combined_right_image_with_name_{parent_current_index}.jpg'
    for i in range(40): 
        index = i + current_index_
        destination = f'{directory_name}/frame_{index}.jpg'
        shutil.copyfile(file_name, destination)
        current_index = current_index + 1

    #print("added images for right with names")

    #create 20 copies of image without names
    current_index_ = current_index
    file_name =  f'{directory_name}/combined_right_image_{parent_current_index}.jpg'
    for i in range(20): 
        index = i + current_index_
        destination = f'{directory_name}/frame_{index}.jpg'
        shutil.copyfile(file_name, destination)
        current_index = current_index + 1

    num_frames = 70 



    temp_current_index = current_index 

    bg_img = cv2.imread(f'{directory_name}/bg_img.jpg')

    for i in range(0,num_frames):
        t = i / float(num_frames)  
        
        # Get current position 
        position = (1 - t) * start_point + t * end_point  
        
        # Create a copy of the background
        img = bg_img.copy()

        # Define object from img2
        box1 = img2[int(start_point[1]):int(start_point[1] + obj_height), int(start_point[0]):int(start_point[0] + obj_width)]
        # Define object from img1
        box2 = img1[int(end_point[1]):int(end_point[1] + obj_height), int(end_point[0]):int(end_point[0] + obj_width)]
        
        # If the transition is at the start, take the object from img2, otherwise take it from img1
        # if t <= 0.5:
        #     transition_obj = box1
        # else:
        #     transition_obj = box2  

        # corner_radius = 30
        # mask = create_rounded_mask(box1, corner_radius)

        # # Generate the rounded image
        # box1 = get_rounded_image(box1, mask)


        # corner_radius = 30
        # mask = create_rounded_mask(box2, corner_radius)

        # # Generate the rounded image
        # box2 = get_rounded_image(box2, mask)

        transition_obj = (1 - t) * box1 + t * box2

        transition_obj_h, transition_obj_w, _ = transition_obj.shape

        ch = min(transition_obj_h, int(position[1] + obj_height ) - int(position[1])) 
        cw = min(int(position[0] + obj_width) - int(position[0]), transition_obj_w) 
        
        # Add object to the current image
        img[int(position[1]): int(position[1]) + ch, int(position[0]): int(position[0]) + cw] = transition_obj

        # transition_obj = refined_alpha_blend( img[int(position[1]): int(position[1]) + ch, int(position[0]): int(position[0]) + cw], transition_obj)
        # img[int(position[1]): int(position[1]) + ch, int(position[0]): int(position[0]) + cw] = transition_obj[:, :, :3]  # Only take BGR channels, ignore alpha 

        #frame_index = 76 + i + 2 

        frame_index = temp_current_index + i 
        
        cv2.imwrite(f'{directory_name}/frame_{frame_index}.jpg', img)  

        current_index = current_index + 1



    current_index_ = current_index

    #print("added intermediatory frames")

    #create 25 copies of imgage without names

    file_name = f'{directory_name}/combined_left_image_{parent_current_index}.jpg'
    for i in range(25): 
        index = i + current_index_
        destination = f'{directory_name}/frame_{index}.jpg'
        shutil.copyfile(file_name, destination) 
        current_index = current_index + 1


    #print("added images for left")



    #create 40 copies of image with names
    current_index_ = current_index

    file_name =  f'{directory_name}/combined_left_image_with_name_{parent_current_index}.jpg'
    for i in range(40): 
        index = i + current_index_
        destination = f'{directory_name}/frame_{index}.jpg'
        shutil.copyfile(file_name, destination)
        current_index = current_index + 1

    #print("added images for left with names")


    
  
    


   

    return current_index

def refined_alpha_blend(roi, overlay):
    # Extract the alpha channel and normalize it
    alpha = overlay[:, :, 3] / 255.0
    inverse_alpha = 1.0 - alpha

    # Ensure both images have 4 channels
    if roi.shape[2] == 3:
        roi = np.dstack([roi, np.ones((roi.shape[0], roi.shape[1]), dtype="uint8") * 255])

    # Premultiply RGB channels with the alpha
    overlay_premul = overlay.copy()
    roi_premul = roi.copy()
    for c in range(3):
        overlay_premul[:, :, c] = overlay_premul[:, :, c] * alpha
        roi_premul[:, :, c] = roi_premul[:, :, c] * inverse_alpha

    # Blend the premultiplied images
    blended = overlay_premul + roi_premul
    blended[:, :, 3] = overlay[:, :, 3]  # Set the alpha channel

    return blended

def get_rounded_image(image, mask):
    # Separate the color and alpha channels from the mask
    mask_color = mask[:, :, :3]
    mask_alpha = mask[:, :, 3] if mask.shape[2] == 4 else None

    # Apply the mask to get the rounded image
    rounded_img = cv2.bitwise_and(image, mask_color)
    
    # If the image doesn't already have an alpha channel, add one
    if image.shape[2] == 3:
        rounded_img = np.dstack([rounded_img, mask_alpha if mask_alpha is not None else mask_color[:, :, 0]])
    
    return rounded_img



def create_rounded_mask(image, corner_radius):
    mask = np.zeros_like(image)
    
    # Draw 4 ellipses at the corners to make them rounded
    cv2.ellipse(mask, (corner_radius, corner_radius), (corner_radius, corner_radius), 180, 0, 90, (255,255,255), -1)
    cv2.ellipse(mask, (image.shape[1] - corner_radius, corner_radius), (corner_radius, corner_radius), 270, 0, 90, (255,255,255), -1)
    cv2.ellipse(mask, (corner_radius, image.shape[0] - corner_radius), (corner_radius, corner_radius), 90, 0, 90, (255,255,255), -1)
    cv2.ellipse(mask, (image.shape[1] - corner_radius, image.shape[0] - corner_radius), (corner_radius, corner_radius), 0, 0, 90, (255,255,255), -1)
    
    # Draw the rectangles to fill the interior parts
    cv2.rectangle(mask, (corner_radius, 0), (image.shape[1] - corner_radius, image.shape[0]), (255, 255, 255), -1)
    cv2.rectangle(mask, (0, corner_radius), (image.shape[1], image.shape[0] - corner_radius), (255, 255, 255), -1)
    
    return mask


def build_screen(screen_file, combine_file_name, x_coordinate, sceen_name, text_to_be_added):

    # Load the images
    background = read_image("https://builderbuckets.blob.core.windows.net/builder-now-beta/builderbackground.png")
    overlay = read_image(screen_file)
    mobile = read_image("https://builderbuckets.blob.core.windows.net/builder-now-beta/310x640-with-border-radius.png")

    # Resize overlay to fit inside the mobile screen
    # Assuming the visible screen area dimensions are (280, 520) for the mobile image
    screen_width, screen_height = 284, 609
    overlay = cv2.resize(overlay, (screen_width, screen_height))
    
    # Ensure mobile has an alpha channel
    if mobile.shape[2] < 4:
        mobile = np.dstack([mobile, np.ones((mobile.shape[0], mobile.shape[1]), dtype="uint8") * 255])

    # Overlay the mobile image onto the background
    m_x, m_y, m_w, m_h = x_coordinate, 150, mobile.shape[1], mobile.shape[0]
    roi = background[m_y:m_y+m_h, m_x:m_x+m_w]
    img_blend = cv2.addWeighted(roi, 1, mobile[:, :, 0:3], 1, 0)
    background[m_y:m_y+m_h, m_x:m_x+m_w, 0:3] = img_blend * (mobile[:, :, 3:] / 255.0) + background[m_y:m_y+m_h, m_x:m_x+m_w, 0:3] * (1 - mobile[:, :, 3:] / 255.0)
    
    # Overlay the screen onto the background
    # Assuming the top-left corner of the visible screen area is at position (15, 60) for the mobile image 

    corner_radius = 30
    mask = create_rounded_mask(overlay, corner_radius)

    # Generate the rounded image
    rounded_image = get_rounded_image(overlay, mask) 

    x, y = x_coordinate + 13, 150 + 15
    h_o, w_o, _ = rounded_image.shape  

    # Overlay the rounded image onto the background
    m_x, m_y, m_w, m_h = x_coordinate, 150, rounded_image.shape[1], rounded_image.shape[0]  

    if rounded_image.shape[2] < 4:
        rounded_image = np.dstack([rounded_image, np.ones((rounded_image.shape[0], rounded_image.shape[1]), dtype="uint8") * 255])


    roi = background[y:y+h_o, x:x+w_o]  

    alpha = rounded_image[:, :, 3] / 255.0
    inverse_alpha = 1.0 - alpha  


    blended_roi = refined_alpha_blend(background[y:y+h_o, x:x+w_o], rounded_image)
    background[y:y+h_o, x:x+w_o] = blended_roi[:, :, :3]  # Only take BGR channels, ignore alpha


    if text_to_be_added:
        # Convert OpenCV image to Pillow format
        pil_image = Image.fromarray(cv2.cvtColor(background, cv2.COLOR_BGR2RGB))
        
        # Load the custom font
        font_path = pkg_resources.resource_filename('video_images_creator', 'Rubik-Medium.ttf')
        font_size = 47
        font = ImageFont.truetype(font_path, font_size)
        draw = ImageDraw.Draw(pil_image)
        
        max_width = 455  # The maximum width for text
        lines = []
        words = sceen_name.split()
        while words:
            line = ''
            while words and int(draw.textlength(line + words[0], font=font)) <= max_width:
                line += (words.pop(0) + ' ')
            lines.append(line)
        
        # Limit to 3 lines
        lines = lines[:3]
        
        y = background.shape[0] - 600
        for i, line in enumerate(lines):
            if x_coordinate == 455:
                x = x_coordinate + 350
            else:
                x = x_coordinate - 400  
            draw.text((x, y + i*font_size), line.strip(), font=font, fill=(255, 255, 255))

        background = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    # Save and return the modified image
    cv2.imwrite(combine_file_name, background)
    return combine_file_name


def build_screen_optimised(screen_file, combine_file_name, x_coordinate, directory_name, position):
    overlay = read_image(screen_file) 
    screen_width, screen_height = 284, 615
    x, y = x_coordinate + 13, 220 + 15
   
    overlay = cv2.resize(overlay, (screen_width, screen_height))


    if position == 'left':
        background = cv2.imread(f'{directory_name}/combined_left_new.jpg') 
    else:
        background = cv2.imread(f'{directory_name}/combined_right_new.jpg')

    # if position == 'left': 
    #     image_path = pkg_resources.resource_filename('video_images_creator', "combined_left_new.jpg")
    #     background = cv2.imread(image_path) 
    # else:
    #     image_path = pkg_resources.resource_filename('video_images_creator', "combined_right_new.jpg")
    #     background = cv2.imread(image_path)

    corner_radius = 30
    mask = create_rounded_mask(overlay, corner_radius)

    # Generate the rounded image
    rounded_image = get_rounded_image(overlay, mask)
    h_o, w_o, _ = rounded_image.shape 
    blended_roi = refined_alpha_blend(background[y:y+h_o, x:x+w_o], rounded_image)
    background[y:y+h_o, x:x+w_o] = blended_roi[:, :, :3]  # Only take BGR channels, ignore alpha 

    cv2.imwrite(combine_file_name, background)

    return combine_file_name

def run_ffmpeg_v3(directory_name, uniq_code, temp_text_file, total_duration):
     
    main_audio_path = pkg_resources.resource_filename('video_images_creator', 'audionew.wav') 
    thanks_audio_path = pkg_resources.resource_filename('video_images_creator', 'thanks.wav') 


    jpg_files = glob.glob(os.path.join(directory_name, '*.jpg'))
    number_of_jpg_files = len(jpg_files) 
    #delay_for_thanks = floor( number_of_jpg_files / 60 ) * 1000

    delay_for_thanks = ( floor( total_duration - 3.0 ) ) * 1000

    ffmpeg_command = [
    "ffmpeg",
    "-f", "concat",   # Use the concat demuxer
    "-safe", "0",     # Allow use of absolute paths
    "-i", temp_text_file,  # Specify the input text file
    "-i", main_audio_path,
    "-i", thanks_audio_path,
    "-filter_complex", f"[2:a]adelay={delay_for_thanks}|{delay_for_thanks}[a2];[1:a][a2]amix=inputs=2:duration=longest[aout]",
    "-map", "0:v",  # Map video from the first input (image sequence)
    "-map", "[aout]",  # Map the audio output from the filtergraph
    "-vsync", "vfr",  # Use variable frame rate to avoid frame duplication,
    "-pix_fmt", "yuv420p",
    "-color_primaries", "bt709",
    "-color_trc", "bt709",
    "-colorspace", "bt709",
    "-shortest",
    f"outputs/output_{uniq_code}.mp4"      # Specify the output video file 
    ]

    #print("the delay is", delay_for_thanks)

    #print(ffmpeg_command)

    subprocess.run(ffmpeg_command)


def run_ffmpeg_v4(directory_name, uniq_code, temp_text_file, tts_output_2_channel_filename, total_duration):
     
    main_audio_path = pkg_resources.resource_filename('video_images_creator', 'audionew.wav') 
    thanks_audio_path = pkg_resources.resource_filename('video_images_creator', 'thanks.wav')
    background_audio_path = pkg_resources.resource_filename('video_images_creator', 'background_music.wav')


    jpg_files = glob.glob(os.path.join(directory_name, '*.jpg'))
    number_of_jpg_files = len(jpg_files) 
    #delay_for_thanks = floor( number_of_jpg_files / 60 ) * 1000

    delay_for_thanks = ( floor( total_duration - 3.0 ) ) * 1000

    ffmpeg_command = [
        "ffmpeg",
        "-y",
        "-f", "concat",  # Use the concat demuxer
        "-safe", "0",  # Allow use of absolute paths
        "-i", temp_text_file,  # Specify the input text file for video
        "-i", tts_output_2_channel_filename,  # First audio input
        "-stream_loop", "-1", "-i", background_audio_path,  # Loop this audio file
        "-i", thanks_audio_path,  # Third audio input
        "-filter_complex",
        "[2:a]volume=0.35[looped];"  # Lower the volume of the looped audio
        f"[3:a]adelay={delay_for_thanks}|{delay_for_thanks}[a3];"  # Delay 'thanks.wav'
        "[1:a][looped][a3]amix=inputs=3:duration=longest[aout]",  # Mix all audio inputs
        "-map", "0:v",  # Map video from the first input (image sequence)
        "-map", "[aout]",  # Map the audio output from the filtergraph
        "-vsync", "vfr",  # Use variable frame rate to avoid frame duplication
        "-pix_fmt", "yuv420p",
        "-color_primaries", "bt709",
        "-color_trc", "bt709",
        "-colorspace", "bt709",
        "-shortest",  # Stop encoding when the shortest input stream ends
        f"outputs/output_{uniq_code}.mp4"  # Specify the output video file 
    ]


    #print("the delay is", delay_for_thanks)

    #print(ffmpeg_command)

    subprocess.run(ffmpeg_command)


def run_ffmpeg_v2(directory_name, uniq_code):
    main_audio_path = pkg_resources.resource_filename('video_images_creator', 'audionew.wav') 
    thanks_audio_path = pkg_resources.resource_filename('video_images_creator', 'thanks.wav') 

    jpg_files = glob.glob(os.path.join(directory_name, '*.jpg'))
    number_of_jpg_files = len(jpg_files) 
    #delay_for_thanks = floor( number_of_jpg_files / 60 ) * 1000

    delay_for_thanks = ( floor( number_of_jpg_files / 60 ) - 2 ) * 1000

    # print(f"ffmpeg -v verbose -y -framerate 60 -i {directory_name}/frame_%d.jpg  -i {main_audio_path} -i {thanks_audio_path} -filter_complex '[2:a]adelay={delay_for_thanks}|{delay_for_thanks}[a2];[1:a][a2]amix=inputs=2:duration=longest[aout]' -map 0:v -map '[aout]' -c:v libx264 -crf 18 -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 -r 60 -c:a aac -strict experimental -shortest outputs/output_{uniq_code}.mp4")

    os.system(f"ffmpeg -v verbose -y -framerate 60 -i {directory_name}/frame_%d.jpg  -i {main_audio_path} -i {thanks_audio_path} -filter_complex '[2:a]adelay={delay_for_thanks}|{delay_for_thanks}[a2];[1:a][a2]amix=inputs=2:duration=longest[aout]' -map 0:v -map '[aout]' -c:v libx264 -preset ultrafast -crf 18 -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 -r 60 -c:a aac -strict experimental -shortest outputs/output_{uniq_code}.mp4")



def run_ffmpeg(directory_name, uniq_code): 
    
    audio_path = pkg_resources.resource_filename('video_images_creator', 'instantvideoaudio.wav') 
    os.system(f"ffmpeg -v verbose -y -framerate 60 -i {directory_name}/frame_%d.jpg -i {audio_path} -c:v libx264 -crf 18 -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 -r 60 -c:a aac -strict experimental -shortest outputs/output_{uniq_code}.mp4")


def flush_video_images(diretory_name, folder_name):
    try:
        # Use shutil.rmtree() to remove the entire folder and its contents
        shutil.rmtree(diretory_name)
        #print(f"Folder '{diretory_name}' and its contents have been deleted.")
        return f"outputs/output_{folder_name}.mp4"
    except Exception as e:
        #print(f"An error occurred: {e}")
        return f"outputs/output_{folder_name}.mp4"

def read_image(image_url):
    resp = urlopen(image_url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR) # The image object
    return image 

def ensure_required_directories_existis():
    if not os.path.exists("images"):
        try:
            os.mkdir("images")
        except Exception as e:
            print("Exception occured", e)
    if not os.path.exists("outputs"):
        try:
            os.mkdir("outputs")
        except Exception as e:
            print("Exception occured..", e)


if __name__ == "__main__": 
    project_name = "Design Process"
    image_file_paths = ["video_images_creator/features/launch.png", "video_images_creator/features/first.png","video_images_creator/features/second.png", "video_images_creator/features/third.png", "video_images_creator/features/fourth.png", "video_images_creator/features/fifth.png"] 
    feature_names = ["Splash Screen", "Search", "Dashboard", "Settings", "Profile/Bio", "Analytics" ]
    #image_file_paths = ["video_images_creator/features/launch.png", "video_images_creator/features/first.png", "video_images_creator/features/second.png"]

    build(image_file_paths, feature_names, project_name)