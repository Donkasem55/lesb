import sys, os, shutil, json
from pathlib import Path

if os.name == "nt":
	PATH = "C:\\Program Files\\lesbbin\\"
	PATH = "C:\\Program Files\\lesblib\\"
	userPATH = str(Path.home() / ".lesbbin") + "\\"
	userPATHLIB = str(Path.home() / ".lesblib") + "\\"

else:
	PATH = "/opt/lesb/"
	PATHLIB = "/opt/lesb.lib/"
	userPATH = str(Path.home() / ".lesbbin") + "/"
	userPATHLIB = str(Path.home() / ".lesblib") + "/"

def main():
	argn = 1
	if not os.path.isdir(PATH):
		try:
			os.mkdir(PATH)
		except:
			pass
	if not os.path.isdir(userPATH):
		try:
			os.mkdir(userPATH)
		except:
			pass

	while argn < len(sys.argv):
		if sys.argv[argn] == "-y":
			sys.stdout.write("\033[38;5;1m:: LESB:\033[38;5;9m SYNCING \033[38;5;15mMASTER \033[38;5;13mBULK \033[38;5;5mREPOSITORY\033[0m\n")
			sys.stdout.flush()

			d = os.getcwd()
			try:
				os.chdir(Path.home() / ".lesbcache")
			except FileNotFoundError:
				os.mkdir(Path.home() / ".lesbcache")
				os.chdir(Path.home() / ".lesbcache")

			if "masterbulkrepo" not in os.listdir():
				try:
					if sys.argv[argn+1].startswith("-"):
						os.system("git clone https://github.com/rainecubed/masterbulkrepo.git")
					else:
						os.system(f"git clone https://github.com/{sys.argv[argn+1]}")
				except IndexError:
					os.system("git clone https://github.com/rainecubed/masterbulkrepo.git")

			os.chdir("masterbulkrepo")
			os.system("git pull")

			os.chdir(d)
			argn += 1

		elif sys.argv[argn] == "-b":
			sys.stdout.write(f"\033[38;5;1m:: LESB:\033[38;5;9m SYNCING \033[38;5;15mPACKAGE \033[38;5;13mBULK \033[38;5;5m'{sys.argv[argn+1]}'\033[0m\n")
			sys.stdout.flush()

			d = os.getcwd()
			try:
				os.chdir(Path.home() / ".lesbcache")
			except FileNotFoundError:
				os.mkdir(Path.home() / ".lesbcache")
				os.chdir(Path.home() / ".lesbcache")

			with open("masterbulkrepo/repo.json") as f:
				r = json.load(f)

			os.chdir("bulk")

			if sys.argv[argn+1] not in r:
				sys.stdout.write(f"\033[38;5;1m:: FATAL\033[38;5;9m ERROR: \033[38;5;15mUNKNOWN \033[38;5;13mBULK \033[38;5;5m'{sys.argv[argn+1]}'\033[0m\n")
				sys.stdout.flush()
				os.chdir(d)
				sys.exit(1)

			if sys.argv[argn+1] not in os.listdir():
				os.system(f"git clone {r[sys.argv[argn+1]]}")

			os.chdir(sys.argv[argn+1])
			os.system("git pull")

			os.chdir(d)
			argn += 2

		elif sys.argv[argn] == "-R":
			sys.stdout.write(f"\033[38;5;1m::\033[38;5;9m LESB:\033[38;5;15m RUNNING\033[38;5;13m PACKAGE: \033[38;5;5m'{sys.argv[argn+1]}'\033[0m\n")
			sys.stdout.flush()

			args = f"{PATH}{sys.argv[argn+1]}"
			prog = f"{PATH}{sys.argv[argn+1]}"
			if not os.path.isfile(args):
				args = f"{userPATH}{sys.argv[argn+1]}"
				prog = f"{userPATH}{sys.argv[argn+1]}"
			for i in range(argn+2, len(sys.argv)):
				if sys.argv[i].startswith("-"):
					break
				else:
					args += " "
					args += sys.argv[i]

			d = os.getcwd()

			if os.path.isfile(prog):
				_ = os.system(args)
			else:
				sys.stdout.write(f"\033[38;5;1m:: FATAL\033[38;5;9m ERROR: \033[38;5;15mUNKNOWN \033[38;5;13mPROGRAM \033[38;5;5m'{sys.argv[argn+1]}'\033[0m\n")
				sys.stdout.flush()
				os.chdir(d)
				sys.exit(1)
			
			os.chdir(d)

			argn += 1
			argn += len(args.split(" "))

		elif sys.argv[argn] == "-I":
			sys.stdout.write(f"\033[38;5;1m::\033[38;5;9m LESB:\033[38;5;15m INSTALLING\033[38;5;13m PACKAGE: \033[38;5;5m'{sys.argv[argn+1]}'\033[0m\n")
			sys.stdout.flush()

			tmp = sys.argv[argn+1].split(".")
			p = Path.home() / ".lesbcache" / "bulk" / tmp[0] / ".".join(tmp[1:]) 
			p2 = Path.home() / ".lesbcache" / "bulk" / tmp[0] / ".".join(tmp[1:]) / sys.platform

			if os.path.isdir(p) and os.path.isdir(p2):
				try:
					for i in os.listdir(f"{p2}/usr/bin"):
						if os.isfile(f"{PATH}/{i}") 
							os.remove(f"{PATH}/{i}")
						elif os.isdir(f"{PATH}/{i}"):
							shutil.rmtree(f"{PATH}/{i}")
						
						if os.isfile(f"{p2}/usr/bin/{i}"):
							shutil.copy(f"{p2}/usr/bin/{i}", PATH)
						else:
							shutil.copytree(f"{p2}/usr/bin/{i}", PATH)

					for i in os.listdir(f"{p2}/usr/lib"):
						if os.isfile(f"{PATHLIB}/{i}") 
							os.remove(f"{PATHLIB}/{i}")
						elif os.isdir(f"{PATHLIB}/{i}"):
							shutil.rmtree(f"{PATHLIB}/{i}")						

						if os.isfile(f"{p2}/usr/lib/{i}"):
							shutil.copy(f"{p2}/usr/lib/{i}", PATHLIB)
						else:
							shutil.copytree(f"{p2}/usr/lib/{i}", PATHLIB)

				except PermissionError:
					for i in os.listdir(f"{p2}/usr/bin"):
						if os.isfile(f"{userPATH}/{i}") 
							os.remove(f"{userPATH}/{i}")
						elif os.isdir(f"{userPATH}/{i}"):
							shutil.rmtree(f"{userPATH}/{i}")

						if os.isfile(f"{p2}/usr/bin/{i}"):
							shutil.copy(f"{p2}/usr/bin/{i}", userPATH)
						else:
							shutil.copytree(f"{p2}/usr/bin/{i}", userPATH)

					for i in os.listdir(f"{p2}/usr/lib"):
						if os.isfile(f"{userPATHLIB}/{i}") 
							os.remove(f"{userPATHLIB}/{i}")
						elif os.isdir(f"{userPATHLIB}/{i}"):
							shutil.rmtree(f"{userPATHLIB}/{i}")

						if os.isfile(f"{p2}/usr/lib/{i}"):
							shutil.copy(f"{p2}/usr/lib/{i}", userPATHLIB)
						else:
							shutil.copytree(f"{p2}/usr/lib/{i}", userPATHLIB)

			elif os.path.isdir(p):
				sys.stdout.write(f"\033[38;5;1m:: FATAL ERROR:\033[38;5;9m PACKAGE \033[38;5;15m'{sys.argv[argn+1]}' \033[38;5;13mUNSUPPORTED \033[38;5;5mBY PLATFORM\033[0m\n")
				sys.stdout.flush()
				os.chdir(d)
				sys.exit(1)

			else:
				sys.stdout.write(f"\033[38;5;1m:: FATAL\033[38;5;9m ERROR: \033[38;5;15mUNKNOWN \033[38;5;13mPACKAGE \033[38;5;5m'{sys.argv[argn+1]}'\033[0m\n")
				sys.stdout.flush()
				os.chdir(d)
				sys.exit(1)
			
			argn += 3

		else:
			sys.stdout.write(f"\033[38;5;1m:: FATAL\033[38;5;9m ERROR: \033[38;5;15mUNKNOWN \033[38;5;13mARGUMENT: \033[38;5;5m'{sys.argv[argn]}'\033[0m\n")
			sys.stdout.flush()
			sys.exit(1)

if __name__ == "__main__":
	main()
