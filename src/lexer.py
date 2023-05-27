import ply.lex as lex
import re
import json

level = 0  # nivel
comm_level = 0  #
indi_level = 0  #

name = ""  # nome da pessoa
pointer = ""  # pointer para uma pessoa
dic = dict()  # dicionario que associa o pointer ao nome da pessoa


def t_error(t):
    #print("erro" + t.value)
    t.lexer.skip(1)



#    states = [
#         ("pessoa", "exclusive"),
#         ("familia", "exclusive")
#    ]
#
tokens = [

    "LEVEL",

    "BIRTH",
    "DEATH",
    "MAR",  # casamento
    "BURIAL",

    "POINTER",

    "CONTENT",
    "MULTITAG",

    "CONT",
    "CHAN",
    "FAM",
    "INDI",
    "CHR",
    "GEDC",
    "BEGIN",
    "START_FILE",
    "END_FILE"
]

# expressoes tokens e estados

t_ANY_ignore = r"\t\s"

t_BEGIN = r"\n(?=0\ @[IF])"

t_ANY_CHR = r"CHR"

t_ANY_BIRTH = "BIRT"
t_ANY_DEATH = "DEAT"
t_ANY_BURIAL = r"BURI"
t_ANY_MAR = r"MARR"
t_ANY_GEDC = r"GEDC"
t_CHAN = r"CHAN"

t_CONT = r"CONT"



t_START_FILE = r"0\ HEAD"
t_END_FILE = r"0\ TRLR"


t_LEVEL = r"\d"


def t_CONTENT(t):
    r"""(_?[A-Z]{3,15}|@[^IF][^@\n]+?@)[\ \t]([^\n]+)"""
    return t


def t_ANY_INDI(t):
    r"INDI"
    return t


def t_FAM(t):
    r"FAM\b"
    return t


def t_MULTITAG(t):
    r'[A-Z]{3,15}(?=\n)'
    return t


t_ANY_POINTER = r"\@[IF][^@]+?\@"


lexer = lex.lex()

if __name__ == "__main__":

    with open("test/familias_reais.ged.txt", 'r') as f:
        lines = f.readlines()
        for line in lines:
            lexer.input(line)
            for token in lexer:
                print(f"{token.type:<10} | {token.value:<50}")