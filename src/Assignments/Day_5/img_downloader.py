import os
import time
import requests
import multiprocessing

def download_image(image_id, mode):
    """Download an image based on mode (seq or multi)"""
    directory = f"images/{mode}/"
    
    os.makedirs(directory, exist_ok=True)

    url = f"https://picsum.photos/2000/3000"
    response = requests.get(url)

    filename = os.path.join(directory, f"image_{image_id}.jpg")
    with open(filename, "wb") as f:
        f.write(response.content)
    
    print(f"Downloaded image_{image_id}.jpg to {directory}")

def download_images_sequential():
    """Download images sequentially"""
    start_time = time.time()
    
    for i in range(1, 6):
        download_image(i, "seq")
    
    end_time = time.time()
    print(f"\nSequential download time: {end_time - start_time:.2f} seconds")

def download_images_multiprocessing():
    """Download images using multiprocessing"""
    start_time = time.time()
    processes = []
    
    for i in range(1, 6):
        process = multiprocessing.Process(target=download_image, args=(i, "multi"))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()
    
    end_time = time.time()
    print(f"\nMultiprocessing download time: {end_time - start_time:.2f} seconds")



if __name__ == "__main__":
    multiprocessing.freeze_support()
    os.makedirs("images/seq", exist_ok=True)
    os.makedirs("images/multi", exist_ok=True)
    
    print("Starting sequential downloads...")
    download_images_sequential()
    
    print("\nStarting parallel downloads...")
    download_images_multiprocessing()
