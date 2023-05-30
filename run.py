import os
import sys


def main():
    if (len(sys.argv) == 2 and  0 <= int(sys.argv[1]) <= 11 ):
        os.system("python ex{:02d}.py".format(int(sys.argv[1])))
    #run the tests at amd above the given number
    elif (len(sys.argv) == 3 and sys.argv[1] == "-f" and 0 <= int(sys.argv[2]) <= 11):
        for i in range(int(sys.argv[2]),12):
            os.system("cls" if os.name == "nt" else "clear")
            print("Running ex{:02d}.py".format(i))
            print("====================================")
            os.system("python ex{:02d}.py".format(i))
            print("====================================")
            input("Press ENTER to continue to the next program...")
        return
    else:
        for i in range(12):
            os.system("cls" if os.name == "nt" else "clear")
            print("Running ex{:02d}.py".format(i))
            print("====================================")
            os.system("python ex{:02d}.py".format(i))
            print("====================================")
            input("Press ENTER to continue to the next program...")

if __name__ == "__main__":
    main()