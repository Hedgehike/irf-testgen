# irf-testgen
##Usage
`tests.py --script [script-to-test.py] --lang [powershell|python] --test [testfile.txt]`

Test files have a basic syntax as follows:
```
#param_name
value1,[V|I|E]
value2,[V|I|E]
#param_name2
values...
```

V means valid, I means invalid and E means contains non-terminating errors. At the moment, the E setting is used to count the number of lines output by the script that contain `ERROR`, in upper case.
The script generates test cases, which are all possible variations of input parameters, where a variation contains a maximum of 1 invalid cases.

Invalid cases are checked by getting the return code of the tested script. In PowerShell, a thrown exception will return a nonzero code, while in python you are encouraged to set it yourself by calling sys.exit(0|1) at the end of your script.
The output gets printed to the standart output.
