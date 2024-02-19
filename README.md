
# OnderCode Interpreter

It's basically a fun project that I have done in my free time, it interprets a simple pseudocode called "Ondercode" and allows user to track script's progress

## Authors

- [@SzymonSkrzypczyk](https://github.com/SzymonSkrzypczyk)


## Contributing

Z.Onderka PHD since it's "his" pseudocode or rather something he has taught us to use


## Usage/Examples

To initialize the Interpreter(a and b are variables from input)
```
c = Interpreter(TEMP_NWP_PATH, debug=False, a=6, b=4)
```
To display variables and interpretation steps present in the script at the moment
```
print(c.variables)
print(c.steps)
```
To execute the script
```
c()
print(c.variables)
```

