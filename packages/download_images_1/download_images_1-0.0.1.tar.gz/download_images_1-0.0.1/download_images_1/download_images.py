import os
import requests
from PIL import Image
from io import BytesIO
from datetime import datetime
from tqdm.notebook import tqdm

def download_images(urls, dest, image_name):
    # Ensure the destination directory exists
    os.makedirs(dest, exist_ok=True)
    
    # Create a progress bar
    with tqdm(total=len(urls), desc="Downloading images", unit="image", dynamic_ncols=True) as pbar:
        for index, url in enumerate(urls, start=1):
            try:
                # Fetch the image via HTTP GET request
                response = requests.get(url)
                response.raise_for_status()  # Check for bad status codes
                
                # Get the binary data of the image
                img_data = response.content
                
                # Convert binary data to file-like object in memory using BytesIO
                img_file = BytesIO(img_data)
                
                # Open the image 
                img = Image.open(img_file)
                
                # Generate unique file name
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]  # Truncate microseconds to milliseconds
                file_name = f'{image_name}_{timestamp}.jpg'
                save_path = os.path.join(dest, file_name)
                
                # Checking for existing file name
                while os.path.exists(save_path):
                    print(f'File {file_name} already exists.')
                    action = input("""What do you want to do now:\n
                    s: Skip\n
                    m: Modify filename\n
                    u: Use timestamp for uniqueness\n
                    Choice: """)
                    
                    if action == 's':
                        print(f'Skipping {file_name}')
                        break
                    elif action == 'm':
                        file_name = input('Enter new filename (without extension): ') + '.jpg'
                        save_path = os.path.join(dest, file_name)
                    elif action == 'u':
                        timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]  # Update timestamp
                        file_name = f'{image_name}_{timestamp}.jpg'
                        save_path = os.path.join(dest, file_name)
                    else:
                        print('Invalid choice, please choose again.')
                
                if os.path.exists(save_path):
                    pbar.update(1)  # Update progress bar even if skipping
                    continue  # Skip saving if the file already exists and user chose to skip

                # Save the image
                img.save(save_path)
                print(f'Successfully downloaded and saved {file_name}')
                pbar.update(1)  # Update progress bar after successful save
                
            except requests.exceptions.RequestException as e:
                print(f'Failed to download {url}: {e}')
                pbar.update(1)  # Update progress bar even if there's an error
            
            except IOError as e:
                print(f'Failed to process {url}: {e}')
                pbar.update(1)  # Update progress bar even if there's an error
