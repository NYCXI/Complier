import os
import LS_Text as ls
from Data import Canonical
from Data import Action
from Data import Goto
from Data import Token
from Data import Production

def Analyze(tokens, action, goto):
    step = 1
    stack_sig = []
    stack_state = []
    #stack_src = []
    #用列表代替栈
    #stack_sig.append('#')
    stack_state.append('T0')
    tokens.append(Token(0, '#', '#'))
    while len(tokens) > 0:
        token = tokens.pop(0)
        print('sig: ' + str(stack_sig) + '  state: ' + str(stack_state) + '  ch: ' + token.category, end = '  ')
        try:
            tmp = action.dict_action[stack_state[-1]][token.category]
        except KeyError:
            print('wrong at:' + str(token.col) + '  content: ' + token.content + '  category: ' + token.category)
            break
        
        if type(tmp) == str:
            if token.category == '#' and len(stack_sig) == 1:
                print('接受')
            else:
                print('移进')
                stack_state.append(tmp)
                stack_sig.append(token.category)
        else:
            print('规约')
            k = len(tmp.R)
            del stack_sig[-k:]
            stack_sig.append(tmp.Vnl)
            del stack_state[-k:]
            try:
                stack_state.append(goto.dict_goto[stack_state[-1]][tmp.Vnl])
            except KeyError:
                print('wrong at:' + str(token.col) + '  content: ' + token.content + '  category: ' + token.category)
                break
            except IndexError:
                print(len(stack_state))
                #print(stack_state[-1])
                print(tmp.Vnl)
                break
            tokens.insert(0, token)
    
    if Production.S in stack_sig and len(stack_sig) == 1:
        print('yes')
    else:
        print('no')


if __name__ == '__main__':
    os.chdir('Complier_task2\\')

    #读取token和二型文法
    list_token = ls.LoadToken('src\\tokens.txt')
    list_prod, dict_prod= ls.LoadRules('src\\2_rule.txt')
    
    #构造项目集规范族
    NormGrp = Canonical(dict_prod)
    NormGrp.prt()

    #构造action表
    action = Action(NormGrp, dict_prod)
    #action.prt()

    #构造goto表
    goto = Goto(NormGrp)
    #goto.prt()

    Analyze(list_token, action, goto)