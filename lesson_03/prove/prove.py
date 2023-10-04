"""
Course: CSE 251 
Lesson: L03 Prove
File:   prove.py
Author: Jake Zalesny

Purpose: Video Frame Processing

Instructions:

- Follow the instructions found in Canvas for this assignment
- No other packages or modules are allowed to be used in this assignment.
  Do not change any of the from and import statements.
- Only process the given MP4 files for this assignment
- Do not forget to complete any TODO comments.

"""

from matplotlib.pylab import plt  # load plot library
from setup import setup as ensure_assignment_is_setup
from PIL import Image
import numpy as np
import timeit
import multiprocessing as mp

# Include cse 251 common Python files
from cse251 import *

# 4 more than the number of cpu's on your computer
CPU_COUNT = mp.cpu_count() + 4

# TODO Your final video needs to have 300 processed frames.
# However, while you are testing your code, set this much lower!
FRAME_COUNT = 300

# RGB values for reference
RED = 0
GREEN = 1
BLUE = 2

def create_new_frame(image_file, green_file, process_file):
    """"
    Creates a new image file from image_file and green_file.
    
    Parameters:
        image_file (str):   The path including name of the image to place on the green screen.
        green_file (str):   The path including name of the green screen image to process.
        process_file (str): The path including name of the file to save the processed image to.
    """

    # this print() statement is there to help see which frame is being processed
    print(f'{process_file[-7:-4]}', end=',', flush=True)

    image_img = Image.open(image_file)
    green_img = Image.open(green_file)

    # Make Numpy array
    np_img = np.array(green_img)

    # Mask pixels 
    mask = (np_img[:, :, BLUE] < 120) & (np_img[:, :, GREEN] > 120) & (np_img[:, :, RED] < 120)

    # Create mask image
    mask_img = Image.fromarray((mask*255).astype(np.uint8))

    image_new = Image.composite(image_img, green_img, mask_img)
    image_new.save(process_file)


# TODO add any functions to need here
def process_frame(frames):
    image_file = rf'elephant/image{frames:03d}.png'
    green_file = rf'green/image{frames:03d}.png'
    process_file = rf'processed/image{frames:03d}.png'
    create_new_frame(image_file=image_file, green_file=green_file, process_file=process_file)


def main():
    all_process_time = timeit.default_timer()
    log = Log(show_terminal=True)

    # Make a for loop that goes to 1 cpu then 2, then 3. 
    xaxis_cpus = []
    yaxis_times = []

    # TODO Process all frames trying 1 cpu, then 2, then 3, ... to CPU_COUNT
    #      add results to xaxis_cpus and yaxis_times
    frames = range(1, FRAME_COUNT + 1)
    for processors in range(1, CPU_COUNT + 1):
        
        time = timeit.default_timer()
        xaxis_cpus.append(processors)
        
        with mp.Pool(processors) as p:
            p.map(process_frame, frames)
        
        log.write(f"Total time for {processors} processes: {timeit.default_timer() - time}")
        yaxis_times.append(timeit.default_timer() - time)


    # Sample code remove before submitting  >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # process one frame #10
    # image_number = 10

    # image_file = rf'elephant/image{image_number:03d}.png'
    # green_file = rf'green/image{image_number:03d}.png'
    # process_file = rf'processed/image{image_number:03d}.png'

    start_time = timeit.default_timer()
    # create_new_frame(image_file, green_file, process_file)
    print(f'\nTime To Process all images = {timeit.default_timer() - start_time}')
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


    log.write(f'Total Time for ALL processing: {timeit.default_timer() - all_process_time}')

    # create plot of results and also save it to a PNG file
    plt.plot(xaxis_cpus, yaxis_times, label=f'{FRAME_COUNT}')
    
    plt.title('CPU Core yaxis_times VS CPUs')
    plt.xlabel('CPU Cores')
    plt.ylabel('Seconds')
    plt.legend(loc='best')

    plt.tight_layout()
    plt.savefig(f'Plot for {FRAME_COUNT} frames.png')
    plt.show()


if __name__ == "__main__":
    ensure_assignment_is_setup()
    main()
