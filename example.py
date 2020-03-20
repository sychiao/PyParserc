from pyparser import Parser, Token, TokenParserGen, LexGen

@Parser
def val(toks):
  return val(toks)

@Parser
def expr(toks):
  return expr(toks)

@Parser
def setstmt(toks):
  return setstmt(toks)

@Parser
def VParser(toks):
  return VParser(toks)

@Parser
def item(toks):
  return item(toks)

@Parser
def compoundstmt(toks):
  return compoundstmt(toks)

lex = LexGen("Hello").\
  add_rule("NUM",r"[0-9]+").\
  add_rule("WHILE",r"while").\
  add_rule("DO",r"do").\
  add_rule("END",r"end").\
  add_rule("VAR",r"[a-z]+").\
  add_rule("AOP",r"\+|-").\
  add_rule("MOP",r"\*|/").\
  add_rule("SEMI",r";").\
  add_rule("SET",r":=")

AOP = TokenParserGen(Token("AOP"))
MOP = TokenParserGen(Token("MOP"))
SET = TokenParserGen(Token("SET"))
VAR = TokenParserGen(Token("VAR"))
NUM = TokenParserGen(Token("NUM"))
WHILE = TokenParserGen(Token("WHILE"))
SEMI = TokenParserGen(Token("SEMI"))
DO = TokenParserGen(Token("DO"))
END = TokenParserGen(Token("END"))

val = VAR/NUM
item = val*MOP*item/val
expr = item*AOP*expr/item
setstmt = VAR*SET*expr
whilestmt = WHILE*expr*DO*compoundstmt*END
stmt = setstmt/whilestmt
compoundstmt = stmt*SEMI*compoundstmt/stmt

item.setname("Item")
expr.setname("Expr")
setstmt.setname("SetStmt")
whilestmt.setname("WhileStmt")
compoundstmt.setname("CompoundStmt")

res, rest = compoundstmt(lex("a:=a+b+2*c;while a do b:=1;c:=2 end"))

print("rest:", rest)
print("result:\n", res)