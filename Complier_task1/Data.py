class Production:
    #从文件中读取产生式之后转换为Production结构。
    #Production包含产生式左部、右部a、右部A。
    VN = []
    VT = []
    S = ''
    def __init__(self, str):
        l = str.split(' ')
        self.Vnl = l[0]
        self.Vt = l[1]
        try:
            self.Vnr = l[2]
        except IndexError:
            self.Vnr = ''

    def prt(self):
        #打印函数
        print("Vnl:" + self.Vnl + " Vt:" + self.Vt + " Vnr:" + self.Vnr)

class StateNode:
    def __init__(self, name, end = False, start = False):
        #状态名、转换函数（字典嵌套列表）、初始节点、终态节点
        self.StateName = name
        self.ChangeFun = {}
        self.isEnd = end
        self.isStart = start
    
    def appendChangeFun(self, ch, StateName):
        if ch in self.ChangeFun:
            self.ChangeFun[ch].append(StateName)
        else:
            self.ChangeFun[ch] = [StateName]

class dfaNode:
    sub = 0
    def __init__(self, nstateslist, nfaTable):
        self.StateName = 'T' + str(dfaNode.sub)
        self.dict_ChangeFun = {}
        self.list_nstates = nstateslist
        if nfaTable.tabledic[Production.S] in self.list_nstates:
            self.isStart = True
        else:
            self.isStart = False
        if nfaTable.tabledic['endNode'] in self.list_nstates:
            self.isEnd = True
        else:
            self.isEnd = False

    def isSame(self, nstates):
        tmp1 = self.list_nstates.copy()
        tmp2 = nstates.copy()
        for item in self.list_nstates:
            if item in nstates:
                try:
                    tmp1.remove(item)
                    tmp2.remove(item)
                except ValueError:
                    pass
        if len(tmp1) == 0 and len(tmp2) == 0:
            return True
        else:
            return False

class Token:
    def __init__(self, col, category, content, dfaTable):
        self.col = col
        self.content = content
        self.category = category
        for item in dfaTable:
            #print(type(item))
            if category == item:
                cates = [Category.dict_category[dfaTable[item].list_nstates[0].StateName]]
                for nstate in dfaTable[item].list_nstates[1:]:
                    if nstate.StateName == 'endNode':
                        continue
                    if Category.dict_category[nstate.StateName] not in cates:
                        cates.append(Category.dict_category[nstate.StateName])
                if len(cates) == 1:
                    if cates[0] == '标识符':
                        if content in Category.tuple_keyword:
                            cates[0] = '关键字'
                    self.category = cates[0]
                else:
                    if '关键字' in cates and '标识符' in cates:
                        if content in Category.tuple_keyword:
                            self.category = '关键字'
                        else:
                            self.category = '标识符'
                    elif '运算符' in cates and '限定符' in cates:
                        self.category = '限定符'
                    else:
                        self.category = 'unsure'

    def prt(self):
        print('col:' + str(self.col + 1) + '\tcategory:' + str(self.category) + '\tcontent:' + str(self.content))

class Category:
    tuple_category = ('关键字', '标识符', '常量', '运算符', '限定符')
    tuple_keyword = ('auto', 'break', 'case', 'char', 'const', 'continue',
                    'default', 'double', 'else', 'enum', 'extern', 'float',
                    'for', 'goto', 'int', 'long', 'register', 'return',
                    'short', 'signed', 'sizeof', 'struct', 'switch', 'typedef',
                    'union', 'unsighed', 'void', 'include', 'enum', 'inline',
                    'while', 'false', 'true', 'do', 'class',)
    dict_category = {'关键字':tuple_category[0],
                    '标识符':tuple_category[1],
                    '常数':tuple_category[2],
                    '整形常量':tuple_category[2],
                    '整数':tuple_category[2],
                    '小数点':tuple_category[2],
                    '小数':tuple_category[2],
                    '科学计数':tuple_category[2],
                    '指数符':tuple_category[2],
                    '指数':tuple_category[2],
                    '复数':tuple_category[2],
                    '实部':tuple_category[2],
                    '虚部':tuple_category[2],
                    '字符串':tuple_category[2],
                    '转义字符':tuple_category[2],
                    '限定符':tuple_category[4],
                    '运算符':tuple_category[3],}
    
    def __init__(self):
        pass