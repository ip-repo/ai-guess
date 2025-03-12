import shutil
import sys
import os
import os
import sys
import subprocess
import shutil
import winreg as reg
from source.pyfiles import helpers

class Install:
	"""
	A class to manage the installation process of the program.
	"""
	def __init__(self,program_name: str="guess") -> None:
		self.script_path = "\\".join(os.path.abspath(__file__).split("\\")[:-1])
		self.c_files_path = self.script_path + "\\source\\cfiles\\"
		self.py_files_path = self.script_path + "\\source\\pyfiles\\"
		self.source_path = os.path.join(self.script_path, "source")
		self.program_name = None
		


		print("#" * helpers.get_terminal_width())
		print("Setting installation files")
		print("#" * helpers.get_terminal_width())
		self.set_program_name(program_name=program_name)
		print(f"Installing {self.program_name} ....")
		print(f"Location of installation files: {self.script_path}")
		print(f"Location of installation source folder: {self.source_path}")
		print(f"Location of installation python files: {self.py_files_path}")
		print(f"Location of installation c files: {self.c_files_path}")
		print("#" * helpers.get_terminal_width())
	
	def set_program_name(self, program_name) -> None:
		"""
		Sets the program name for the installation process.

		Args:
			program_name (str): The name of the program to be installed.

		Returns:
			None
		"""
		self.program_name = program_name

	def check_dependencies(self, program: str) -> None:
		"""
		Checks if the specified program is installed and available in the system's PATH.
		Prints an error message and exits if the program is not installed.
		Prints the program's path if it is available.
		Args:
			program (str): The name of the program to check for availability.
		sys.exit: Exits the program if the specified program is not found.
		Returns:
			None
		"""
		program_path = shutil.which(program)
		if program_path is None:
			message = f"Error: {program} is not installed. Please install {program} and try again."
			print(message)
			print("#" * helpers.get_terminal_width())
			sys.exit(1)
		message = f"{program} is available at: {program_path}"
		print(message)
		
	def set_installtion_path(self) -> None:
		"""
		Prompts the user to input an installation path, creates the directory if it does not exist,
		and prints the program's name and installation path.
			- Accepts user input for the installation path.
			- Creates the directory at the specified installation path if it does not already exist.
			- Prints the program name and installation path to the console.
		
		self.install_path (str): The path where the program will be installed.

		Returns:
			None
		"""
		self.install_path = input("Enter the installation path: ").strip() 
		os.makedirs(self.install_path, exist_ok=True)
		message = f"Program Name: {self.program_name}"
		print(message)
		message = f"Install Path: {self.install_path}"
		print(message)
		
	def create_top_folder(self) -> None:
		"""
		Creates the top-level folder for the program within the installation path.

		The folder name is derived from the program's name and the installation path. 
		If the folder already exists, it does nothing (using the exist_ok=True parameter).
			- Creates a directory at the specified location.
			- Prints the full path of the created program folder.

		self.top_folder (str): The path of the newly created top-level program folder.

		Returns:
			None
		"""
		self.top_folder = os.path.join(self.install_path, self.program_name)
		os.makedirs(self.top_folder, exist_ok=True)
		message = f"Program Folder: {self.top_folder}"
		print(message)
	
	def create_bin_folder(self) -> None:
		"""
		Creates the 'bin' folder within the top-level program directory.

		The folder is named 'bin' and is located inside the top folder associated 
		with the program. If the folder already exists, no action is taken due 
		to the use of the `exist_ok=True` parameter.
			- Creates a 'bin' directory at the specified location.
			- Prints a message indicating the path of the created 'bin' folder.
		self.bin_folder (str): The full path of the newly created 'bin' folder.

		Returns:
			None
		"""
		self.bin_folder = os.path.join(self.top_folder, "bin")
		os.makedirs(self.bin_folder, exist_ok=True)
		message = f"Created Bin Folder: {self.bin_folder}"
		print(message)
		
	def create_info_folder(self) -> None:
		"""
		Creates an 'info' folder within the top-level program directory.

		The folder is named 'info' and is located inside the top folder associated 
		with the program. If the folder already exists, no action is taken due 
		to the use of the `exist_ok=True` parameter.
			- Creates an 'info' directory at the specified location.
			- Prints a message indicating the path of the created 'info' folder.
		self.info_folder (str): The full path of the newly created 'info' folder.

		Returns:
			None
		"""
		self.info_folder = os.path.join(self.top_folder, "info")
		os.makedirs(self.info_folder, exist_ok=True)
		message = f"Created Info Folder: {self.info_folder}"
		print(message)
	
	def complie_c_file(self,file_name: str, post_fix: str="") -> None:
		"""
		Compiles a C source file into an executable using GCC.

		This method compiles a specified C file located in the C files directory 
		and outputs the compiled executable to the bin folder. The name of the 
		executable is determined by the program name and an optional postfix.

		- Runs the GCC compiler via subprocess.
			- Outputs the compiled executable to the bin folder.
			- Prints messages indicating the source file and the location of the 
			compiled executable.

		Args:
			file_name (str): The name of the C file to compile (with extension).
			post_fix (str, optional): A string appended to the executable's name. 
									Defaults to an empty string.

		Returns:
			None
		"""
		exe_name = f"{self.program_name}{post_fix}.exe"
		output_path = os.path.join(self.bin_folder, exe_name)
		subprocess.check_call(["gcc", os.path.join(self.c_files_path, file_name), "-o", output_path])
		
		message = f"Compiled {self.c_files_path}\\{file_name}\nPath: {self.bin_folder}\\{exe_name}"
		print(message)
	
	def add_bin_to_path(self, bin_folder) -> None:
		try:
			# Open the Environment key in the current user's registry
			with reg.OpenKey(reg.HKEY_CURRENT_USER, "Environment", 0, reg.KEY_ALL_ACCESS) as key:
				try:
					current_path, _ = reg.QueryValueEx(key, "Path")
				except FileNotFoundError:
					# Handle cases where the Path variable doesn't exist yet
					current_path = ""

				if bin_folder not in current_path:
					updated_path = current_path + ";" + bin_folder if current_path else bin_folder
					reg.SetValueEx(key, "Path", 0, reg.REG_SZ, updated_path)

		except FileNotFoundError:
			# If the Path variable or key doesn't exist, create it
			with reg.CreateKey(reg.HKEY_CURRENT_USER, "Environment") as key:
				reg.SetValueEx(key, "Path", 0, reg.REG_SZ, bin_folder)
			
	def compile_py_file(self,file_name: str, post_fix: str="", exe_name:str=None) -> None:
		"""
		Compiles a Python script into an executable using PyInstaller.

		Args:
			file_name (str): The name of the Python file to compile.
			post_fix (str, optional): An optional string to append to the generated executable name. Defaults to an empty string.
			exe_name (str, optional): The name of the output executable file. 
									If not provided, it defaults to "<program_name><post_fix>.exe".

		Returns:
			None
		"""
		pyinstaller_path = shutil.which("pyinstaller")
		if exe_name == None:
			exe_name = f"{self.program_name}{post_fix}.exe"
		source_file = os.path.join(self.py_files_path, file_name)
		print(source_file)
		output_path = os.path.join(self.bin_folder, exe_name)
		print(output_path)
		subprocess.check_call([pyinstaller_path, "--onefile", source_file])
		dist_exe = os.path.join(self.script_path, "dist", os.path.splitext(file_name)[0] + ".exe")
		print(dist_exe)
		shutil.move(dist_exe, output_path)
		message = f"Compiled {self.py_files_path}\\{file_name}\nPath: {self.bin_folder}\\{exe_name}"
		print(message)      
	
if __name__ == "__main__":
	program_name = "guess"
	ins = Install(program_name=program_name)
	print("Checking dependencies")
	print("#" * helpers.get_terminal_width())
	ins.check_dependencies(program="python")
	ins.check_dependencies(program="pyinstaller")
	ins.check_dependencies(program="gcc")
	print("#" * helpers.get_terminal_width())
	print("Setting installation path ...")
	print("#" * helpers.get_terminal_width())
	ins.set_installtion_path()
	print("#" * helpers.get_terminal_width())
	print("Creating program folders...")
	print("#" * helpers.get_terminal_width())
	ins.create_top_folder()
	ins.create_bin_folder()
	ins.create_info_folder()
	print("#" * helpers.get_terminal_width())
	print("Preparing EXE files")
	print("#" * helpers.get_terminal_width())
	#
	c_file_to_compile = "models.c"
	post_fix = "-mo"
	ins.complie_c_file(file_name=c_file_to_compile, post_fix=post_fix)
	print()
	py_file_to_compile = "guess.py"
	post_fix = "-gate"
	ins.compile_py_file(file_name=py_file_to_compile, post_fix=post_fix)
	print()
	print("#" * helpers.get_terminal_width())
	print("Adding Path to C files")
	print("#" * helpers.get_terminal_width())
	output = []
	with open(os.path.join(ins.c_files_path, "singelCall.c"), "r") as file:
		for line in file.read().split("\n"):
			if "*installPath" in line:
				output.append(f'    char *installPath = "{ins.bin_folder.replace("\\","\\\\")}\\\\{ins.program_name}-gate.exe";')
			else:
				output.append(line)
	with open(os.path.join(ins.c_files_path, "singelCall1.c"), "w") as file:
		file.write("\n".join(output))
	print("#" * helpers.get_terminal_width())
	print("Preparing EXE files")
	print("#" * helpers.get_terminal_width())
	c_file_to_compile = "singelCall1.c"
	post_fix = "-mo"
	ins.complie_c_file(file_name= c_file_to_compile, post_fix=post_fix)
	print()

	with open(f"{ins.py_files_path}list_model_exe_path.py", "w") as file:
		file.write(f"list_models_path = '{ins.bin_folder.replace("\\","\\\\")}\\\\{ins.program_name}-mo.exe'")

	ins.compile_py_file(file_name="set_model.py",post_fix="-sm")
	print(ins.info_folder)
	with open(f"{ins.info_folder}\\\\sys_message.txt", "w") as file:
		file.write(helpers.SYSTEM_MESSAGE)

	not_allowed = ["nomic-embed-text:latest","llama3.2-vision:latest"]

	with open(f"{ins.info_folder}\\\\not_allowed.txt", "w") as file:
		file.write("\n".join(not_allowed))

	os.system(f"{ins.bin_folder.replace("\\","\\\\")}\\\\{ins.program_name}-sm.exe NONE")
	print("#" * helpers.get_terminal_width())
	print(f"Info folder located at: {ins.info_folder}")
	print("#" * helpers.get_terminal_width())
	ins.add_bin_to_path(os.path.normpath(ins.bin_folder))
	print(f"Adding bin to PATH: {ins.bin_folder}")
	print("Make sure the bin folder in PATH!")
	print("#" * helpers.get_terminal_width())

	
	build_folder = os.path.join(ins.script_path, "build")
	dist_folder = os.path.join(ins.script_path, "dist")

	spec_file_1 = os.path.join(ins.script_path, os.path.splitext("guess.py")[0] + ".spec")
	spec_file_2 = os.path.join(ins.script_path, os.path.splitext("set_model.py")[0] + ".spec")
	c_file = os.path.join(ins.c_files_path, "singelCall1.c")
	
	#clean up
	if os.path.exists(build_folder):
		shutil.rmtree(build_folder)
	if os.path.exists(dist_folder):
		shutil.rmtree(dist_folder)
	if os.path.exists(spec_file_1):
		os.remove(spec_file_1)
	if os.path.exists(spec_file_2):
		os.remove(spec_file_2)
	if os.path.exists(c_file):
		os.remove(c_file)
		
		

	
