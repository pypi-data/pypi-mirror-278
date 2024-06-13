import psutil, platform, shutil, GPUtil, wmi, os, cv2, pyAesCrypt, maskpass, face_recognition, io, requests
from bs4 import BeautifulSoup


class terminal:
    def print_colored(self, text, color):
        colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'reset': '\033[0m'
        }
        return(f"{colors[color]}{text}{colors['reset']}")
    def move_cursor(self, row, col):
        print(f"\033[{row};{col}H", end="")
    def get_terminal_size(self):
        columns, rows = os.get_terminal_size(0)
        return columns, rows
    
    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    def progress_bar(self, progress, total, bar_length=20):
        percent = 100 * (progress / float(total))
        bar = '█' * int(percent / (100 / bar_length)) + '-' * (bar_length - int(percent / (100 / bar_length)))
        print(f"\r|{bar}| {percent:.2f}%", end="\r")
        if progress == total:
            print()
    def blink_text(self, text):
        import time
        blink = True
        while True:
            if blink:
                print(f"\033[5m{text}\033[0m", end="\r")
            else:
                print(f"{' ' * len(text)}", end="\r")
            blink = not blink
            time.sleep(0.5)
class performance_monitor:
    def __init__(self):
        pass
    class version:
        def version():
            """Returns the version of the operating system.
            Example:
            >>> version()
            '10.0.19041'
            """
            return platform.version()
        def release():
            """Returns the release of the operating system.
            Example:
            >>> release()
            '2004'
            """
            return platform.release()
        def system():
            """Returns the system of the operating system.
            Example:
            >>> system()
            'Windows'
            """
            return platform.system()
    class cpu:
        def cpumodel():
            """Returns the model name of the CPU.
            Example:
            >>> cpumodel()
            Intel(R) Core(TM) i5-8250U CPU @ 1.60GHz
            """
            try:
                return wmi.WMI().Win32_Processor()[0].Name
            except:
                return 'No CPU found.'
        def cpuusage():
            """Returns the current CPU usage as a percentage.
            Example:
            >>> cpuusage()
            4.2
            """
            try:
                return psutil.cpu_percent()
            except:
                return 'No CPU found.'
    class gpu():
        def gpumodel():
            """Returns the model name of the GPU.
            Example:
            >>> gpumodel()
            NVIDIA GeForce MX130
            """
            try:
                return GPUtil.getGPUs()[0].name
            except:
                return 'No GPU found.'
        def gpuusage():
            """Returns the current GPU usage as a percentage.
            Example:
            >>> gpuusage()
            4.2
            """
            try:
                return GPUtil.getGPUs()[0].load*100
            except:
                return 'No GPU found.'
    class storage():
        def __init__(self):
            self.total, self.used, self.free = shutil.disk_usage('/')
        def storagetotal(self, bytes=None):
            """Returns the total storage space in GB.
            If the bytes parameter is True, returns the total storage space in bytes.
            Example:
            >>> storagetotal()
            100.0
            >>> storagetotal(bytes)
            1000000000000
            """
            if bytes:
                return self.total
            else:
                return f'{self.total // (2 ** 30)} GB'
        def storageused(self, bytes=None):
            """Returns the used storage space in GB.
            If the bytes parameter is True, returns the used storage space in bytes.
            Example:
            >>> storageused()
            50.0
            >>> storageused(bytes)
            500000000000
            """
            if bytes:
                return self.used
            else:
                return f'{self.used // (2 ** 30)} GB'
        def storageleft(self, bytes=None):
            """Returns the free storage space in GB.
            If the bytes parameter is True, returns the free storage space in bytes.
            Example:
            >>> storageleft()
            50.0
            >>> storageleft(bytes)
            500000000000
            """
            if bytes:
                return self.free
            else:
                return f'{self.free // (2 ** 30)} GB'

def compare_faces(known_face_image_path, unknown_face_image_path):
    # Load the known face image and encode it
    known_image = face_recognition.load_image_file(known_face_image_path)
    known_face_encoding = face_recognition.face_encodings(known_image)[0]

    # Load the unknown face image and encode it
    unknown_image = face_recognition.load_image_file(unknown_face_image_path)
    unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]

    # Calculate the face distance between known and unknown face encodings
    face_distance = face_recognition.face_distance([known_face_encoding], unknown_face_encoding)
    
    # Convert face distance to similarity percentage (smaller distance = higher similarity)
    max_distance = 1.0
    similarity_percent = (max_distance - face_distance[0]) * 100.0 / max_distance
    
    return similarity_percent

def capture_and_compare(known_face_image_path):
    # Capture image from the camera
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()

    # Convert the frame to RGB (face_recognition library expects RGB images)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Convert the RGB frame to a byte stream
    _, encoded_image = cv2.imencode('.jpg', rgb_frame)
    unknown_image_bytes = io.BytesIO(encoded_image)

    # Compare faces
    similarity_percent = compare_faces(known_face_image_path, unknown_image_bytes)

    # Release the camera
    cap.release()
    cv2.destroyAllWindows()

    return similarity_percent

def facereg(imagepath=None):
    if imagepath == None:
        return print("No image path provided")
    #root = tk.Tk()
    #root.withdraw()  # Hide the main window
    #file_path = filedialog.askopenfilename(title="Select an Image File")
    similarity_percent = capture_and_compare(imagepath)
    return similarity_percent
def decrypt_file_without_saving(encrypted_file_path, password):
    try:
        bufferSize = 64 * 1024
        decrypted_data = pyAesCrypt.decryptBytesIO(
            encrypted_data=encrypted_file_path, 
            password=password, 
            bufferSize=bufferSize
        )
        return decrypted_data
    except ValueError as e:
        print("Decryption failed:", str(e))
        return None

# Example usage:
def decrypt_file():
    encrypted_file_path = "example_file.aes"  # Path to the encrypted file
    password = maskpass.askpass("Enter the password for decryption\n")
    decrypted_data = decrypt_file_without_saving(encrypted_file_path, password)
    if decrypted_data:
        print("Decryption successful.")
        # Process the decrypted data here, such as writing it to a new file or using it in-memory.
    else:
        print("Decryption failed.")
def checkType(x):
    x_type = type(x)
    return x_type


def download_page(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def download_pages(urls):
    pages = {}
    for url in urls:
        try:
            pages[url] = download_page(url)
        except requests.RequestException as e:
            print(f"Failed to download {url}: {e}")
    return pages





def extract_titles(html):
    soup = BeautifulSoup(html, 'html.parser')
    titles = [tag.get_text() for tag in soup.find_all('title')]
    return titles

def extract_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True)]
    return links

def extract_images(html):
    soup = BeautifulSoup(html, 'html.parser')
    images = [img['src'] for img in soup.find_all('img', src=True)]
    return images