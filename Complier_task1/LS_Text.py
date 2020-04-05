import os
from Data import Production

def LoadSrc(text_path):
    with open(text_path, mode='r', encoding='utf-8') as file:
        lines = file.readlines()
        return lines

def LoadRule(rule_path):
    with open(rule_path, mode='r', encoding='utf-8') as file:
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
                    str = Vnl + ' ' + line[1:-1]
                else:
                    str = Vnl + ' ' + line[1:]
                rules.append(str)
        #将得到的产生式生成production对象返回
        prodlist = []
        print(len(rules))
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
                prodlist.append(prod)
                #prod.prt()
        return prodlist

def Store(token_path, lines):
    file = open(token_path, mode='w', encoding='utf-8')
    for line in lines:
        file.write(line)
    file.close()