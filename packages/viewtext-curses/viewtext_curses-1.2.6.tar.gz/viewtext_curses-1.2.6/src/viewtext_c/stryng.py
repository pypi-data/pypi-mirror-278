from unicodedata import east_asian_width

def display_w(str: str) -> int:
  """Returns the display width of str assuming utf-8 encoding"""
  return sum((2 if (east_asian_width(c) in "WF") else 1) for c in str)
