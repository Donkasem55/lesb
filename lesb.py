import sys, os, shutil, json, stat
import pydatasm as dasm
from pathlib import Path

if os.name == "nt":
	SYSTEMCONF = "C:\\etc\\lesb.asm"

else:
	SYSTEMCONF = "/etc/lesb.asm"
#	PATH = "/opt/lesb/"
#	PATHLIB = "/opt/lesb.lib/"
#	PATHSHR = "/usr/share/"
#	userPATH = str(Path.home() / ".lesbbin") + "/"
#	userPATHLIB = str(Path.home() / ".lesblib") + "/"
#	userPATHSHR = str(Path.home() / ".local" / "share") + "/"

config = dasm.loaddatasm(SYSTEMCONF)
print(config["path"]["userconfig"])
try:
	userconfig = dasm.loaddatasm(os.path.expanduser(config["path"]["userconfig"]))
except (FileNotFoundError, KeyError):
	print("LESB: FATAL ERROR: USERCONFIG NOT FOUND")
	sys.exit(1)

try:
	PATH = userconfig["path"]["bin"]
	PATHLIB = userconfig["path"]["lib"]
	PATHSHR = userconfig["path"]["share"]
	userPATH = userconfig["userpath"]["bin"]
	userPATHLIB = userconfig["userpath"]["lib"]
	userPATHSHR = userconfig["userpath"]["share"]

except KeyError:
	print("LESB: FATAL ERROR: USERCONFIG: PATH INCOMPLETE")
	sys.exit(1)

def main():
	argn = 1
	try:
		os.mkdir(PATH)
	except:
		pass
	try:
		os.mkdir(PATHSHR)
	except:
		pass
	try:
		os.mkdir(PATHLIB)
	except:
		pass
	try:
		os.mkdir(userPATH)
	except:
		pass
	try:
		os.mkdir(userPATHSHR)
	except:
		pass
	try:
		os.mkdir(userPATHLIB)
	except:
		pass

	if len(sys.argv) == 1:
		print("FATAL ERROR: NO ARGUMENTS GIVEN")

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

			try:
				os.chdir(Path.home() / ".lesbcache" / "bulk")
			except FileNotFoundError:
				os.mkdir(Path.home() / ".lesbcache" / "bulk")
				os.chdir(Path.home() / ".lesbcache" / "bulk")

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

			if os.path.isfile(f"{prog}.exe") and (not os.path.isfile(prog)):
				prog = f"{prog}.exe"
			elif os.path.isfile(f"{prog}.elf") and (not os.path.isfile(prog)):
				prog = f"{prog}.elf"
			elif os.path.isfile(f"{prog}.linex") and (not os.path.isfile(prog)):
				prog = f"{prog}.linex"

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

		elif sys.argv[argn] == "-c":
			sys.stdout.write(f"\033[38;5;1m::\033[38;5;9m LESB:\033[38;5;15m CLEARING\033[38;5;13m CACHED \033[38;5;5mBULKS\033[0m\n")
			def onerr(fn, path, _):
				if os.name == "nt":
					os.chmod(path, stat.S_IWRITE)
				fn(path)

			x = Path.home() / ".lesbcache" / "bulk"
			shutil.rmtree(x, onerror=onerr)
			argn += 1

		elif sys.argv[argn] == "-I":
			sys.stdout.write(f"\033[38;5;1m::\033[38;5;9m LESB:\033[38;5;15m INSTALLING\033[38;5;13m PACKAGE: \033[38;5;5m'{sys.argv[argn+1]}'\033[0m\n")
			sys.stdout.flush()

			tmp = sys.argv[argn+1].split(".")
			p = Path.home() / ".lesbcache" / "bulk" / tmp[0] / ".".join(tmp[1:]) 
			p2 = Path.home() / ".lesbcache" / "bulk" / tmp[0] / ".".join(tmp[1:]) / sys.platform

			if os.path.isdir(p) and os.path.isdir(p2):
				try:
					try:
						for i in os.listdir(f"{p2}/usr/bin"):
							if os.path.isfile(f"{PATH}/{i}"):
								os.remove(f"{PATH}/{i}")
							elif os.path.isdir(f"{PATH}/{i}"):
								shutil.rmtree(f"{PATH}/{i}")
							
							if os.path.isfile(f"{p2}/usr/bin/{i}"):
								shutil.copy(f"{p2}/usr/bin/{i}", PATH)
							else:
								shutil.copytree(f"{p2}/usr/bin/{i}", PATH)
					except FileNotFoundError:
						pass

					try:
						for i in os.listdir(f"{p2}/usr/lib"):
							if os.path.isfile(f"{PATHLIB}/{i}"):
								os.remove(f"{PATHLIB}/{i}")
							elif os.path.isdir(f"{PATHLIB}/{i}"):
								shutil.rmtree(f"{PATHLIB}/{i}")						

							if os.path.isfile(f"{p2}/usr/lib/{i}"):
								shutil.copy(f"{p2}/usr/lib/{i}", PATHLIB)
							else:
								shutil.copytree(f"{p2}/usr/lib/{i}", PATHLIB)
					except FileNotFoundError:
						pass

					try:
						for i in os.listdir(f"{p2}/usr/share"):
							if os.path.isfile(f"{PATHSHR}/{i}"):
								os.remove(f"{PATHSHR}/{i}")
							elif os.path.isdir(f"{PATHSHR}/{i}"):
								shutil.rmtree(f"{PATHSHR}/{i}")						

							if os.path.isfile(f"{p2}/usr/share/{i}"):
								shutil.copy(f"{p2}/usr/share/{i}", PATHSHR)
							else:
								shutil.copytree(f"{p2}/usr/share/{i}", PATHSHR)
					except FileNotFoundError:
						pass



				except (PermissionError, OSError):
					try:
						for i in os.listdir(f"{p2}/usr/bin"):
							if os.path.isfile(f"{userPATH}/{i}"):
								os.remove(f"{userPATH}/{i}")
							elif os.path.isdir(f"{userPATH}/{i}"):
								shutil.rmtree(f"{userPATH}/{i}")

							if os.path.isfile(f"{p2}/usr/bin/{i}"):
								shutil.copy(f"{p2}/usr/bin/{i}", userPATH)
							elif os.path.isdir(f"{p2}/usr/bin/{i}"):
								shutil.copytree(f"{p2}/usr/bin/{i}", userPATH+"/"+i)
					except FileNotFoundError:
						pass

					try:
						for i in os.listdir(f"{p2}/usr/lib"):
							if os.path.isfile(f"{userPATHLIB}/{i}"):
								os.remove(f"{userPATHLIB}/{i}")
							elif os.path.isdir(f"{userPATHLIB}/{i}"):
								shutil.rmtree(f"{userPATHLIB}/{i}")

							if os.path.isfile(f"{p2}/usr/lib/{i}"):
								shutil.copy(f"{p2}/usr/lib/{i}", userPATHLIB)
							elif os.path.isdir(f"{p2}/usr/lib/{i}"):
								shutil.copytree(f"{p2}/usr/lib/{i}", userPATHLIB+"/"+i)
					except FileNotFoundError:
						pass

					try:
						for i in os.listdir(f"{p2}/usr/share"):
							if os.path.isfile(f"{userPATHSHR}/{i}"):
								os.remove(f"{userPATHSHR}/{i}")
							elif os.path.isdir(f"{userPATHSHR}/{i}"):
								shutil.rmtree(f"{userPATHSHR}/{i}")

							if os.path.isfile(f"{p2}/usr/share/{i}"):
								shutil.copy(f"{p2}/usr/share/{i}", userPATHSHR)
							elif os.path.isdir(f"{p2}/usr/share/{i}"):
								shutil.copytree(f"{p2}/usr/share/{i}", userPATHSHR+"/"+i)
					except FileNotFoundError:
						pass

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
			
			argn += 2

		else:
			sys.stdout.write(f"\033[38;5;1m:: FATAL\033[38;5;9m ERROR: \033[38;5;15mUNKNOWN \033[38;5;13mARGUMENT: \033[38;5;5m'{sys.argv[argn]}'\033[0m\n")
			sys.stdout.flush()
			sys.exit(1)

if __name__ == "__main__":
	main()
