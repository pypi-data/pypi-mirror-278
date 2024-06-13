O='No GPU found.'
N='No CPU found.'
K='html.parser'
J='/'
I='\r'
E=True
D=None
A=print
import psutil as P,platform as F,shutil as G,GPUtil as L,wmi,os,cv2 as B,pyAesCrypt as Q,maskpass as R,face_recognition as C,io,requests as M
from bs4 import BeautifulSoup as H
class W:
	def print_colored(C,color):B='reset';A={'red':'\x1b[91m','green':'\x1b[92m','yellow':'\x1b[93m','blue':'\x1b[94m','magenta':'\x1b[95m','cyan':'\x1b[96m',B:'\x1b[0m'};return f"{A[color]}{C}{A[B]}"
	def move_cursor(B,col):A(f"[{B};{col}H",end='')
	def get_terminal_size():A,B=os.get_terminal_size(0);return A,B
	def clear_terminal():os.system('cls'if os.name=='nt'else'clear')
	def progress_bar(D,total,bar_length=20):
		E=total;B=bar_length;C=100*(D/float(E));F='█'*int(C/(100/B))+'-'*(B-int(C/(100/B)));A(f"\r|{F}| {C:.2f}%",end=I)
		if D==E:A()
	def blink_text(C):
		import time;B=E
		while E:
			if B:A(f"[5m{C}[0m",end=I)
			else:A(f"{' '*len(C)}",end=I)
			B=not B;time.sleep(.5)
class X:
	def __init__():0
	class version:
		def version():return F.version()
		def release():return F.release()
		def system():return F.system()
	class cpu:
		def cpumodel():
			try:return wmi.WMI().Win32_Processor()[0].Name
			except:return N
		def cpuusage():
			try:return P.cpu_percent()
			except:return N
	class gpu:
		def gpumodel():
			try:return L.getGPUs()[0].name
			except:return O
		def gpuusage():
			try:return L.getGPUs()[0].load*100
			except:return O
	class storage:
		def storagetotal(bytes=D):
			A,B,C=G.disk_usage(J)
			if bytes:return A
			else:return f"{A//2**30} GB"
		def storageused(bytes=D):
			B,A,C=G.disk_usage(J)
			if bytes:return A
			else:return f"{A//2**30} GB"
		def storageleft(bytes=D):
			B,C,A=G.disk_usage(J)
			if bytes:return A
			else:return f"{A//2**30} GB"
def S(known_face_image_path,unknown_face_image_path):B=C.load_image_file(known_face_image_path);D=C.face_encodings(B)[0];E=C.load_image_file(unknown_face_image_path);F=C.face_encodings(E)[0];G=C.face_distance([D],F);A=1.;H=(A-G[0])*1e2/A;return H
def T(known_face_image_path):A=B.VideoCapture(0);H,C=A.read();D=B.cvtColor(C,B.COLOR_BGR2RGB);I,E=B.imencode('.jpg',D);F=io.BytesIO(E);G=S(known_face_image_path,F);A.release();B.destroyAllWindows();return G
def Y(imagepath=D):
	B=imagepath
	if B==D:return A('No image path provided')
	C=T(B);return C
def U(encrypted_file_path,password):
	try:B=64*1024;C=Q.decryptBytesIO(encrypted_data=encrypted_file_path,password=password,bufferSize=B);return C
	except ValueError as D:A('Decryption failed:',str(D));return
def Z():
	B='example_file.aes';C=R.askpass('Enter the password for decryption\n');D=U(B,C)
	if D:A('Decryption successful.')
	else:A('Decryption failed.')
def a(x):A=type(x);return A
def V(url):A=M.get(url);A.raise_for_status();return A.text
def b(urls):
	C={}
	for B in urls:
		try:C[B]=V(B)
		except M.RequestException as D:A(f"Failed to download {B}: {D}")
	return C
def c(html):A=H(html,K);B=[A.get_text()for A in A.find_all('title')];return B
def d(html):A=H(html,K);B=[A['href']for A in A.find_all('a',href=E)];return B
def e(html):A=H(html,K);B=[A['src']for A in A.find_all('img',src=E)];return B