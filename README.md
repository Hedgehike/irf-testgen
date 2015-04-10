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

V means valid, I means invalid and E means contains non-terminating errors. Support for E is experimental currently.
The script generates test cases, which are all possible variations of input parameters, where a variation contains a maximum of 1 invalid cases.
The output gets printed to the standart output.
