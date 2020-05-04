import os
from Data import Token
from Data import Production

def LoadToken(TokenPath):
    with open(TokenPath, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        list_tokens = []
        for line in lines:
            try:
                strs = line.split('\t')
                col = strs[0][strs[0].find(':') + 1:]
                category = strs[1][strs[1].find(':') + 1:]
                content = strs[2][strs[2].find(':') + 1 : -1]
                token = Token(col, category, content)
                list_tokens.append(token)
            except IndexError:
                break
        return list_tokens

def LoadRules(rulepath):
    with open(rulepath, mode='r', encoding='utf-8') as file:
        lines = file.readlines()
        rules = []
        #从文件中读取字符串并转换为AbC型的右线性产生式
        for line in lines:
            if line[0] == '#':
                rules.append(line)
            elif line[0] is not '\t':
                Vnl = line[0:-2]
            else:
                if line[-1] == '\n':
                    str = Vnl
                    for ch in line[1:-1].split(' '):
                        str = str + ' ' + ch
                else:
                    str = Vnl
                    for ch in line[1:].split(' '):
                        str = str + ' ' + ch
                rules.append(str)
        #将得到的产生式生成production对象返回
        list_prod = []
        dict_prod = {}
        #print(len(rules))
        for rule in rules:
            if rule[0] == '#':
                if rule[1] == 'N':
                    Production.VN = rule[3:-1].split(' ')
                elif rule[1] == 'T':
                    Production.VT = rule[3:-1].split(' ')
                elif rule[1] == 'S':
                    Production.S = rule[3]
            else:
                prod = Production(rule)
                list_prod.append(prod)
                if prod.Vnl in dict_prod:
                    dict_prod[prod.Vnl].append(prod)
                else:
                    dict_prod[prod.Vnl] = [prod]
                #prod.prt()
        
        #加入 S'->S 
        list_prod.insert(0, Production('start ' + Production.S))
        dict_prod['start'] = Production('start ' + Production.S)

        return list_prod, dict_prod
