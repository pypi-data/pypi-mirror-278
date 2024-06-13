_E='No GPU found.'
_D='No CPU found.'
_C='html.parser'
_B=True
_A=None
import psutil,platform,shutil,GPUtil,wmi,os,cv2,pyAesCrypt,maskpass,face_recognition,io,requests
from bs4 import BeautifulSoup
class terminal:
	def print_colored(text,color):A='reset';colors={'red':'\x1b[91m','green':'\x1b[92m','yellow':'\x1b[93m','blue':'\x1b[94m','magenta':'\x1b[95m','cyan':'\x1b[96m',A:'\x1b[0m'};return f"{colors[color]}{text}{colors[A]}"
	def move_cursor(row,col):print(f"[{row};{col}H",end='')
	def get_terminal_size():columns,rows=os.get_terminal_size(0);return columns,rows
	def clear_terminal():os.system('cls'if os.name=='nt'else'clear')
	def progress_bar(progress,total,bar_length=20):
		percent=100*(progress/float(total));bar='█'*int(percent/(100/bar_length))+'-'*(bar_length-int(percent/(100/bar_length)));print(f"\r|{bar}| {percent:.2f}%",end='\r')
		if progress==total:print()
	def blink_text(text):
		import time;blink=_B
		while _B:
			if blink:print(f"[5m{text}[0m",end='\r')
			else:print(f"{' '*len(text)}",end='\r')
			blink=not blink;time.sleep(.5)
class performance_monitor:
	def __init__():0
	class version:
		def version():"Returns the version of the operating system.\n            Example:\n            >>> version()\n            '10.0.19041'\n            ";return platform.version()
		def release():"Returns the release of the operating system.\n            Example:\n            >>> release()\n            '2004'\n            ";return platform.release()
		def system():"Returns the system of the operating system.\n            Example:\n            >>> system()\n            'Windows'\n            ";return platform.system()
	class cpu:
		def cpumodel():
			'Returns the model name of the CPU.\n            Example:\n            >>> cpumodel()\n            Intel(R) Core(TM) i5-8250U CPU @ 1.60GHz\n            '
			try:return wmi.WMI().Win32_Processor()[0].Name
			except:return _D
		def cpuusage():
			'Returns the current CPU usage as a percentage.\n            Example:\n            >>> cpuusage()\n            4.2\n            '
			try:return psutil.cpu_percent()
			except:return _D
	class gpu:
		def gpumodel():
			'Returns the model name of the GPU.\n            Example:\n            >>> gpumodel()\n            NVIDIA GeForce MX130\n            '
			try:return GPUtil.getGPUs()[0].name
			except:return _E
		def gpuusage():
			'Returns the current GPU usage as a percentage.\n            Example:\n            >>> gpuusage()\n            4.2\n            '
			try:return GPUtil.getGPUs()[0].load*100
			except:return _E
	class storage:
		def storagetotal(bytes=_A):
			'Returns the total storage space in GB.\n            If the bytes parameter is True, returns the total storage space in bytes.\n            Example:\n            >>> storagetotal()\n            100.0\n            >>> storagetotal(bytes)\n            1000000000000\n            ';total,used,free=shutil.disk_usage('/')
			if bytes:return total
			else:return f"{total//2**30} GB"
		def storageused(bytes=_A):
			'Returns the used storage space in GB.\n            If the bytes parameter is True, returns the used storage space in bytes.\n            Example:\n            >>> storageused()\n            50.0\n            >>> storageused(bytes)\n            500000000000\n            ';total,used,free=shutil.disk_usage('/')
			if bytes:return used
			else:return f"{used//2**30} GB"
		def storageleft(bytes=_A):
			'Returns the free storage space in GB.\n            If the bytes parameter is True, returns the free storage space in bytes.\n            Example:\n            >>> storageleft()\n            50.0\n            >>> storageleft(bytes)\n            500000000000\n            ';total,used,free=shutil.disk_usage('/')
			if bytes:return free
			else:return f"{free//2**30} GB"
def compare_faces(known_face_image_path,unknown_face_image_path):known_image=face_recognition.load_image_file(known_face_image_path);known_face_encoding=face_recognition.face_encodings(known_image)[0];unknown_image=face_recognition.load_image_file(unknown_face_image_path);unknown_face_encoding=face_recognition.face_encodings(unknown_image)[0];face_distance=face_recognition.face_distance([known_face_encoding],unknown_face_encoding);max_distance=1.;similarity_percent=(max_distance-face_distance[0])*1e2/max_distance;return similarity_percent
def capture_and_compare(known_face_image_path):cap=cv2.VideoCapture(0);ret,frame=cap.read();rgb_frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB);_,encoded_image=cv2.imencode('.jpg',rgb_frame);unknown_image_bytes=io.BytesIO(encoded_image);similarity_percent=compare_faces(known_face_image_path,unknown_image_bytes);cap.release();cv2.destroyAllWindows();return similarity_percent
def facereg(imagepath=_A):
	if imagepath==_A:return print('No image path provided')
	similarity_percent=capture_and_compare(imagepath);return similarity_percent
def decrypt_file_without_saving(encrypted_file_path,password):
	try:bufferSize=64*1024;decrypted_data=pyAesCrypt.decryptBytesIO(encrypted_data=encrypted_file_path,password=password,bufferSize=bufferSize);return decrypted_data
	except ValueError as e:print('Decryption failed:',str(e));return
def decrypt_file():
	encrypted_file_path='example_file.aes';password=maskpass.askpass('Enter the password for decryption\n');decrypted_data=decrypt_file_without_saving(encrypted_file_path,password)
	if decrypted_data:print('Decryption successful.')
	else:print('Decryption failed.')
def checkType(x):x_type=type(x);return x_type
def download_page(url):response=requests.get(url);response.raise_for_status();return response.text
def download_pages(urls):
	pages={}
	for url in urls:
		try:pages[url]=download_page(url)
		except requests.RequestException as e:print(f"Failed to download {url}: {e}")
	return pages
def extract_titles(html):soup=BeautifulSoup(html,_C);titles=[tag.get_text()for tag in soup.find_all('title')];return titles
def extract_links(html):soup=BeautifulSoup(html,_C);links=[a['href']for a in soup.find_all('a',href=_B)];return links
def extract_images(html):soup=BeautifulSoup(html,_C);images=[img['src']for img in soup.find_all('img',src=_B)];return images