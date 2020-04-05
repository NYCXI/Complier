import LS_Text as ls
from Data import Production
from dfa import nfa
from dfa import dfa

if __name__ == '__main__':
    prodlist = ls.LoadRule('rule1.txt')

    nfaTable = nfa(prodlist)
    nfaTable.prt()

    print('dfatable:')
    dfaTable = dfa(nfaTable)
    dfaTable.prt()

    