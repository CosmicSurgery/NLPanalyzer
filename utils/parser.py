import re

def startsWithAuthor(s):
   patterns = [
        r'Angelita 🦧:',
        r'Louisa \(HSK\):',
        r'🧀 🧀 🧀:',
        r'Kira Arlt \(HSK\):',
        r'Tiziana \(Couchsurf\):',
        r'Mr. S:',
        r'G-dizzle:',
        r'Good Ol\' Kyle:',
        r'([\w]+):',                        # First Name
        r'([\w]+[\s]+[\w]+):',              # First Name + Last Name
        r'([\w]+[\s]+[\w]+[\s]+[\w]+):',    # First Name + Middle Name + Last Name
        r'([+]\d{2} \d{5} \d{5}):',         # Mobile Number (India)
        r'([+]\d{2} \d{3} \d{3} \d{4}):',   # Mobile Number (US)
        r'([+]\d{2} \d{4} \d{7})'           # Mobile Number (Europe)
   ] 
   pattern = '^' + '|'.join(patterns)
   result = re.match(pattern, s)
   if result:
      return True
   return False


    