# Installing Kivy

These instructions assume you are using the Visual Studio Code IDE with the Python extension enabled, and that your selected Python version is Python 3.8 or later.

## Check Python scripts can run in IDE

Open the file ```lesson-01/code/main.py``` in an editor window and towards the top right of the editor window there should be a green arrow.  Click on the arrow and this will run the Python script, opening a new terminal window.  You should expect to see and error message as the Kivy library has not been installed.

## Install Kivy

Following these instructions will install Kivy in your existing Python installation. If you have multiple copies of Python installed, or if you use Python for other purposes then you
might want to consider creating a "virtual environment", see <https://kivy.org/doc/stable/gettingstarted/installation.html#installation-canonical> for more details.

```sh
python -m pip install kivy[full] kivy_examples
```

Note that ```python``` might be ```python3``` or even a full path, for example on my system it is ```/usr/bin/python3```.  The simplest way to determine what it should be on your system is to check that you have selected the correct version of Python in VS Code.  If the Python extension is enabled the selected Python version is shown towards the bottom left of the IDE window. Click on this and all available versions will be shown along with the full path to the Python interpreter.

On Linux the examples are install in ```~/.local/share/kivy-examples``` for a user install.

## Running the first example

Now try running ```lesson-01/code/main.py``` again.  This time a window should pop up.  If if does then your Kivy install is working, if it doesn't then you'll need to investigate further, see <https://kivy.org/doc/stable/gettingstarted/installation.html> for help.

## Next steps

This first example application is from <https://kivy.org/doc/stable/guide/basic.html#quickstart> and on that page you'll find some suggestions for customizing the application.

### lesson-02

In the next lesson you'll build a simple game.

