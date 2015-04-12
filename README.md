# irf-testgen
##Usage
`tests.py --script [script-to-test.py] --lang [powershell|python] --test [testfile.txt]`

Test files have a basic syntax as follows:
```
#param_name
value1,(V|I|E\d+)
value2,(V|I|E\d+)
#param_name2
values...
```

Example input:
```
#s
machnies.csv,V
invalid.csv,I
nonterminating.csv,E3
#i
none,V
1111,V
```

V means valid, I means invalid and E means contains non-terminating errors. At the moment, the E setting is used to count the number of lines output by the script that contain `ERROR`, in upper case. The test passes, if the number matches that given in the input file.

Setting `none` as the input of a given parameter will be translated into omitting said parameter.

The script generates test cases, which are all possible variations of input parameters, where a variation contains a maximum of 1 invalid cases.

Invalid cases are checked by getting the return code of the tested script. In PowerShell, a thrown exception will return a nonzero code, while in python you are encouraged to set it yourself by calling sys.exit(0|1) at the end of your script.
The output gets printed to the standart output.
