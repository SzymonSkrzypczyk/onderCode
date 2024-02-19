
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
In order to create an executable from the project you have to install Pyinstaller
```
pip install pyinstaller
```
Then you can create an executable by running
```
pyinstaller --paths="src" main.py -w --onefile --name <yourname> 
```
Running this command will create an executable in the dist folder
Since the project does not use any external libraries, the executable should work on any machine
