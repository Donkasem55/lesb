import sys, os, shutil, json
from pathlib import Path

if os.name == "nt":
	PATH = "C:\\Program Files\\lesbbin\\"
	userPATH = str(Path.home() / ".lesbbin") + "\\"
else:
	PATH = "/opt/lesb/"
	userPATH = str(Path.home() / ".lesbbin") + "/"

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
			sys.stdout.write(f"\033[38;5;1m::\033[0m LESB: CLONING BULK: {sys.argv[argn+1]}\n")
			sys.stdout.flush()

			d = os.getcwd()
			try:
				os.chdir(Path.home() / ".lesbcache")
			except FileNotFoundError:
				os.mkdir(Path.home() / ".lesbcache")
				os.chdir(Path.home() / ".lesbcache")

			with open("masterbulkrepo/repo.json") as f:
				r = json.load(f)

			if sys.argv[argn+1] not in r:
				sys.stdout.write(f"\033[38;5;1m:: FATAL\033[38;5;9m ERROR: \033[38;5;15mUNKNOWN \033[38;5;13mBULK \033[38;5;5m'{sys.argv[argn+1]}'\033[0m\n")
				sys.stdout.flush()
				os.chdir(d)
				sys.exit(1)

			os.chdir(d)
			argn += 1

		elif sys.argv[argn] == "-R":
			sys.stdout.write(f"\033[38;5;1m::\033[0m LESB: RUNNING PROGRAM: {sys.argv[argn+1]}\n")
			sys.stdout.flush()

			args = f"{PATH}{sys.argv[argn+1]}"
			prog = f"{PATH}{sys.argv[argn+1]}"
			if not os.path.isfile(args):
				args = f"{userPATH}{sys.argv[argn+1]}"
				prog = f"{userPATH}{sys.argv[argn+1]}"
			for i in range(argn+2, len(sys.argv)):
				if i.startswith("-"):
					break
				else:
					args += sys.argv[i]
					args += " "

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

		else:
			sys.stdout.write(f"\033[38;5;1m:: FATAL\033[38;5;9m ERROR: \033[38;5;15mUNKNOWN \033[38;5;13mARGUMENT: \033[38;5;5m'{sys.argv[argn]}'\033[0m\n")
			sys.stdout.flush()
			sys.exit(1)

if __name__ == "__main__":
	main()
