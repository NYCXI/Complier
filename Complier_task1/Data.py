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