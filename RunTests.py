import os
import subprocess

tests_dir = './testovi'
subdirs = [f.path for f in os.scandir(tests_dir) if f.is_dir()]
subdirs = [os.path.abspath(f) for f in subdirs]
subdirs = sorted(subdirs)

ignore_list = ["12_27_rek", "35_lokal_arr", "42_dekl_vise_varijabli", "e_", "10_29_for"]
new_subdirs = []
for dir in subdirs:
    ignore = False
    for elem in ignore_list:
        if elem in dir:
            ignore = True
    if not ignore:
        new_subdirs.append(dir)

subdirs = new_subdirs

temp_file_name = os.path.join(os.getcwd(), 'out.txt')
# frisc_file_name = os.path.join(os.getcwd(), 'a.frisc')

N = 80
n_total_tests = 0
n_passed_tests = 0

for dir in subdirs:
    print("*"*N)
    print(f"Currently testing: {dir}")
    c_file_name = os.path.join(dir, 'test.c')
    in_file_name = os.path.join(dir, 'test.in')
    out_file_name = os.path.join(dir, 'test.out')

    with open(c_file_name, 'r') as c_file, open(in_file_name, 'r') as in_file, open(out_file_name, 'r') as out_file:
        c_file_as_string = c_file.read()
        in_file_as_string = in_file.read()
        out_file_as_string = out_file.read().rstrip()

        print("-"*N)
        print("C file:")
        print("-"*N)
        print(c_file_as_string)
        print("-"*N)

        temp_file = open(temp_file_name, 'w+')
        # frisc_file = open(frisc_file_name, "w+")

        subprocess.run([f"cat {in_file_name} | python3 GeneratorKoda.py"], shell=True, stdout=subprocess.DEVNULL)
        subprocess.run([f"cat a.frisc | node main.js"], shell=True, stdout=temp_file, stderr=subprocess.DEVNULL)

        with open(temp_file_name, 'r') as output:
            processor_output = output.read().rstrip()

        test_passing = processor_output == out_file_as_string
        
        print(f"Processor output: {processor_output}")
        print(f"Expected processor output: {out_file_as_string}")
        print(f"Test passing?: {test_passing}")
        print("*"*N + "\n")

        n_passed_tests += int(test_passing)
        n_total_tests += 1

print(f"Passed tests: {n_passed_tests}/{n_total_tests}")




    
    
