import subprocess

def run(program_list]):
    for program in program_list:
        subprocess.call(['python', program])
        print("Finished:" + program)