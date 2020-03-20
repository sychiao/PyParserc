import re
from typing import List, Tuple

class Token:
  def __init__(self, tok, s="pattern"):
    self.tok = tok
    self.value = s
  def __repr__(self):
    return f"<{self.tok}|{self.value}>"
  def __eq__(self, other):
    return self.tok == other.tok

class LexGen:
  def __init__(self, name):
    self.name = name
    self.patterns = list()
  def add_rule(self, name, pattern):
    self.patterns.append((name,pattern))
    return self
  def __call__(self, s):
    if s:
      for name, pattern in self.patterns:
        if res := re.match(pattern, s):
          return [Token(name,s[res.start():res.end()])] + self.__call__(s[res.end():])
      else:
        return [] + self.__call__(s[1:])
    else:
      return []

class NamedTuple:
  def __init__(self, name, data):
    self.name = name
    self.data = data
  def __repr__(self):
    return f"{self.name}({self.data})"

class Parser:
  def __init__(self, func):
    self.func = func
    self.name = None
  def __call__(self, toks:List[Token]) -> Tuple[Tuple, List[Token]]:
    pat, rest =  self.func(toks)
    if self.name and pat:
      return NamedTuple(self.name, pat), rest
    return pat, rest
  def __mul__(self, other):
    return ConcatParserGen(self, other)
  def __truediv__(self, other):
    return UnionParserGen(self, other)
  def setname(self, name):
    self.name = name
    return self

def TokenParserGen(tok) -> Parser:
  def TokenParser(toks):
    if len(toks) == 0:
      return None, toks
    elif toks[0] == tok:
      return toks[0], toks[1:]
    else:
      return None, toks
  return Parser(TokenParser)

def UnionParserGen(ParserA:Parser, ParserB:Parser)-> Parser:
  def UnionParser(toks):
    res, rest = ParserA(toks)
    if res:
      return res, rest 
    res, rest = ParserB(toks)
    if res:
      return res, rest 
    return None, toks
  return Parser(UnionParser)

def ConcatParserGen(ParserA:Parser, ParserB:Parser)->Parser:
  def ConcatParser(toks):
    resA, restA = ParserA(toks)
    if resA:
      resB, restB = ParserB(restA)
      if resB:
        return (resA, resB), restB
    return None, toks
  return Parser(ConcatParser)