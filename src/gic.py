import ply.yacc as yacc
import os
from lexer import tokens
from pessoa import Pessoa
from familia import Familia


def p_grammar(p):
    """
    gedcom  	: people families

    people : people person
           | person

    person :  LEVEL POINTER INDI conteudo BEGIN

    conteudo : conteudo LEVEL restPerson
             | LEVEL restPerson
    restPerson	: singTag CONTENT

    families : families family
             | family
    family : LEVEL POINTER FAM conteudoF BEGIN
           | LEVEL POINTER FAM conteudoF TRLR
    conteudoF : conteudoF LEVEL restFams
              | LEVEL restFams

    restFams	: singTag CONTENT
    restPerson	: multTag

    singTag		: NAME
    singTag		: TITLE
    singTag		: SEX
    singTag		: REFN
    singTag		: FAMS
    singTag		: FAMC
    singTag		: DATE
    singTag		: PLACE
    multTag		: BURIAL
    multTag		: BIRTH
    singTag		: WIFE
    singTag		: HUSBAND
    singTag		: CHILD
    multTag		: DEATH
    multTag		: CHR
    """


def p_error(p):
    print("Syntax error in input!", p)
    parser.success = False
    exit()


parser = yacc.yacc()
parser.success = True


with open("test/sintaxe.txt", encoding="utf-8") as f:
    lines = f.read()
    parser.parse(lines)
    if parser.success:
        print("Yes")
    else:
        print("No")
    print("End")


