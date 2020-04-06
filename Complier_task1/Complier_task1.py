import os
import LS_Text as ls
from Data import Production
from Data import Token
from dfa import nfa
from dfa import dfa

def rcg(line, col, dfaTable):
    list_token = []
    state = dfaTable['T0']
    content = ''
    for ch in line:
        if ch == '\n':
            if len(content) > 0:
                token = Token(col,state.StateName, content,dfaTable)
                list_token.append(token)
                content = ''
                state = dfaTable['T0']
        elif ch != ' ':
            try:
                state = dfaTable[state.dict_ChangeFun[ch].StateName]
                content += ch
            except KeyError:
                token = Token(col, state.StateName, content, dfaTable)
                list_token.append(token)
                content = ch
                state = dfaTable['T0']
                state = dfaTable[state.dict_ChangeFun[ch].StateName]
        else:
            if len(content) > 0:
                token = Token(col, state.StateName, content, dfaTable)
                list_token.append(token)
                content = ''
                state = dfaTable['T0']
        if len(line) == 1:
            token = Token(col, state.StateName, content, dfaTable)
            list_token.append(token)
    return list_token

if __name__ == '__main__':
    #设置工作目录
    os.chdir('Complier_task1\\')
    #读取产生式文件

    prodlist = ls.LoadRule('rule1.txt')

    #构造nfa表
    nfaTable = nfa(prodlist)
    #nfaTable.prt()

    #构造dfa表
    dfaTable = dfa(nfaTable)
    #dfaTable.prt()

    #根据dfa表将输入的源程序转换为token表
    lines = ls.LoadSrc('src.txt')
    list_token = []
    for index in range(len(lines)):
        tokens = rcg(lines[index], index, dfaTable.dfaTable)
        list_token.extend(tokens)
    ls.SaveToken('tokens.txt', list_token)