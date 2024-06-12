</div>
<div align="center">
  <img src="https://github.com/SamthinkGit/aiuda/assets/92941012/f11c765b-b405-4184-b152-b2275dbb49c7" alt="aiuda logo" width=700>
</div>

<div align="center">
  <h3>
    <a href="https://medium.com/@sebastianmayorquin_74267/943bde3d196a" style="color:blue; text-decoration:underline;">
      🛠️ Quickstart Guide
    </a>
  </h3>
</div>

# Aiuda: AI-Powered Tools for Python Development

**aiuda** is a Python library that leverages AI to enhance your programming workflow. Inspired by tools like [icecream](https://github.com/gruns/icecream) and PDB, Aiuda provides advanced pretty-printing, formatting, and various utility functions, all powered by AI via [LangChain](https://www.langchain.com/). Whether you need to print objects more effectively, get AI assistance in debugging, or analyze variables, Aiuda has you covered.

## Features ✨

- **Advanced Pretty-Printing:** Enhance the readability of your objects with AI-powered pretty-printing.
- **AI-Assisted Debugging (In progress):** Leverage AI to debug and analyze your code more effectively.
- **Utility Functions (In progress):** A collection of AI-driven utility functions to streamline your daily Python programming tasks.

## Installation 🚀

You can install **aiuda** using pip:

```powershell
pip install aiuda
```

> Note: You can install the last-last version (maybe unstable) by cloning and using pip install directly in the repo :D

## Usage 🛠️

```python
from aiuda import aiuda

# Suppose we have a complex object, sometimes the str() method is not clear
my_dict = {'name': 'Alice', 'age': 30, 'city': 'Wonderland'}

print(my_dict)  # meh
aiuda.tree(my_dict)  # better :D
```
```powershell
>>> print(my_dict)
{'name': 'Alice', 'age': 30, 'city': 'Wonderland'}

>>> aiuda.tree(prompt)
[aiuda][tree]
(name: dict)
├─.name: 'Alice'
├─.age: 30
└─.city: 'Wonderland'
```

## License 📄

Aiuda is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
