import re

a = open("ask.py", encoding="utf-8").read()
fixed = re.sub(r'(\S)(def (?:clean|check|ask_llm|ask)\()', r'\1\n\n\2', a)
fixed = re.sub(r'(\S)(if __name__ == "__main__":)', r'\1\n\n\2', fixed)
open("ask.py", "w", encoding="utf-8").write(fixed)
print("ask.py repaired")