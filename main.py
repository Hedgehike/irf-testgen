__author__ = 'Peter'

import itertools
import subprocess
import string
import argparse
import os
import re


def generate_powershell_case(p, script):
    case = ""
    expected = ""
    invalid_count = 0
    for elem in p:
        if 'I' in elem.split(',')[1]:
            invalid_count += 1
    if invalid_count == 1:
        expected = "Exception"
    if invalid_count <= 1:
        for elem in p:
            if "none" not in elem.split(',')[0]:
                case += elem.split(',')[0] + ' '
        return [script + case, expected, invalid_count]
    else:
        return None


def generate_python_case(p, script):
    case = []
    expected = ""
    invalid_count = 0
    error_count=0
    for elem in p:
        if 'I' in elem.split(',')[1]:
            invalid_count += 1
        elif 'E' in elem.split(',')[1]:
            error_count += int(elem.split(',')[1][1:])
    if invalid_count == 1:
        expected = "Exception"
    elif error_count > 0:
        expected = "Error " + error_count.__str__()
    if invalid_count <= 1:
        for elem in p:
            if "none" not in elem.split(',')[0]:
                case = case + elem.split(',')[0].split(' ')
        case = [script] + case
        return [case, expected, invalid_count]
    else:
        return None


def main():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    template = string.Template("""

[Test case $index]
Input:       $input
Output:      $output
Expected:    $expected
Passed:      $passed

            """)
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--test", help="The location of the file containing the input parameters", default="tests.txt")
    parser.add_argument("-l", "--lang", help="The language of the script. Currently supported: powershell, python", default="python")
    parser.add_argument("-s", "--script", help="The script to be executed.", required=True)
    args = parser.parse_args()

    with open(args.test) as f:
        lines = f.readlines()
        current_list = []
        master = []
        current_param = ""
        for line in lines:
            if line[0] == '#':
                if len(current_list):
                    master.append(current_list)
                current_param = line[1:-1]
                current_list = []
            else:
                if line[:-1] == "none":
                    current_list.append("")
                elif ' ' in line:
                    current_list.append("-" + current_param + " \"" + line.replace(",", '",'))
                else:
                    current_list.append("-" + current_param + " " + line[:-1])
        master.append(current_list)
    cases = []
    for p in itertools.product(*master):
        if args.lang == "powershell":
            case = generate_powershell_case(p, args.script)
        elif args.lang == "python":
            case = generate_python_case(p, args.script)
        if case is not None:
            cases.append(case)
    index = 0
    for c in cases:
        out = ""
        exception = False
        try:
            # out = ""
            if args.lang == "python":
                out = subprocess.check_output(['python3'] + c[0])
            elif args.lang == "powershell":
                out = subprocess.check_output(['powershell.exe', c[0]])
        except subprocess.CalledProcessError as e:
            out = e.output
            exception = True
        finally:
            # text = template.replace('%index', index.__str__()).replace('%input', c[0]).replace('%expected', c[1])\
            # .replace("%output", out.__str__())\
            #     .replace("%passed", (c[1] == "Exception" and exception or c[1] != "Exception" and not exception).__str__())

            # IF we look for a specified number of errors
            m = re.search(r"Error (\d+)", c[1])

            if c[1] == "Exception":
                passed = exception
            elif m is not None:
                passed = (len(re.findall("ERROR", out.decode("utf-8"))) == int(m.group(1)))
            else:
                passed = not exception
            mapping = {
                "index": index.__str__(),
                "input": " ".join(c[0]),
                "expected": c[1],
                "output": "\n"+out.decode("utf-8"),
                "passed": passed.__str__()
            }
            text = template.substitute(mapping)
            index += 1
            print(text)


if __name__ == "__main__":
    main()