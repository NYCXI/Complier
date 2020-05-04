class Token:
    def __init__(self, col ,category, content):
        #col: 行 content: 内容 category: token类别
        self.col = col
        self.content = content
        self.category = category
    
    def prt(self):
        print('col:' + self.col + '\tcategory:' + self.category + '\tcontent:' + self.content)

class Production:
    VN = []
    VT = []
    S = ''
    num = 1
    def __init__(self, rule):
        #print(rule)
        l = rule.split(' ')
        self.Vnl = l[0]
        self.Vnr = []
        self.Vt = []
        self.R = []
        self.num = Production.num
        Production.num += 1
        for str in l[1:]:
            if str in Production.VN:
                self.Vnr.append(str)
                self.R.append(str)
            if str in Production.VT:
                self.Vt.append(str)
                self.R.append(str)

    def prt(self):
        print('Vnl:\t' + self.Vnl)
        print('Vnr:', end = '\t')
        for item in self.Vnr:
            print(item, end = '\t')
        print()
        print('Vt:', end = '\t')
        for item in self.Vt:
            print(item, end= '\t')
        print()

class Canonical:
    num = 0
    #项目集
    def __init__(self, dict_prod):
        self.list_set = []
        self.dict_set = {}
        self.list_set.append(Set(dict_prod['start'], 0, '#', dict_prod, []))
        self.dict_set[str('T' + str(Canonical.num))] = self.list_set[Canonical.num]
        Canonical.num += 1
        for s in self.list_set:
            for ch in Production.VN:
                new, tmp = self.goto(s, ch, dict_prod)
                #new表示goto后是否为新的状态，若 new = true 且 tmp not none 表示goto后是新的状态直接添加到列表和字典中
                #tmp = none时表示在goto后为空集，此时什么都不做
                #若 new = false 表示goto后得到的状态与已有状态相同，此时tmp给出的是已有状态的状态号，将转换此时可能需要合并同心集以及增加firstch
                if new and tmp is not None:
                    s.dict_change[ch] = str('T' + str(Canonical.num))
                    self.list_set.append(tmp)
                    self.dict_set[str('T' + str(Canonical.num))] = self.list_set[Canonical.num]
                    Canonical.num += 1
                elif not new:
                    s.dict_change[ch] = tmp
                    #此时只需要在change字典里加一条指向已有状态集的边即可
            for ch in Production.VT:
                new, tmp = self.goto(s, ch, dict_prod)
                if new and tmp is not None:
                    s.dict_change[ch] = str('T' + str(Canonical.num))
                    self.list_set.append(tmp)
                    self.dict_set[str('T' + str(Canonical.num))] = self.list_set[Canonical.num]
                    Canonical.num += 1
                    #tmp.prt()
                elif not new:
                    #print(type(tmp))
                    s.dict_change[ch] = tmp
            
        
    def goto(self, s, ch, dict_prod):
        tmp = []
        for itm in s.list_itm:
            try:
                if itm.prod.R[itm.dot] == ch:
                    tmp.append(Set(itm.prod, itm.dot + 1, itm.ch, dict_prod, []))
            except IndexError:
                pass
        if len(tmp) == 0:
            return True, None
        else:
            temp = Set('', '', '', '', tmp)
            for set_key in self.dict_set:
                #equal判断两个set是否完全相等，如果两个完全相等则什么都不做，直接返回false
                #equal2判断两个set是否需要合并超前搜索符，并进行合并
                if self.dict_set[set_key].equal(temp):
                    #self.dict_set[set_key].prt()
                    return False, set_key
            return True, temp

    def prt(self):
        for s in self.dict_set:
            print('----------')
            print('key:' + s)
            self.dict_set[s].prt()
            print('----------')

class Set:
    #项目集合
    def __init__(self, prod, dot, firstch, dict_prod, list_set):
        self.list_itm = []
        self.dict_change = {}
        if len(list_set) == 0:
            self.list_itm.append(Itm(prod, dot, firstch))
            for itm in self.list_itm:
                try:
                    if itm.prod.R[itm.dot] in Production.VN:
                        #print(itm.prod.R[itm.dot])
                        for prod in dict_prod[itm.prod.R[itm.dot]]:
                            try:
                                tmp = Itm(prod, 0, self.first(itm.prod.R[itm.dot+1], firstch, dict_prod))
                            except IndexError:
                                tmp = Itm(prod, 0, self.first('#', firstch, dict_prod))
                            if not tmp.exist(self.list_itm):
                                self.list_itm.append(tmp)
                except IndexError:
                    pass
                #print(len(self.list_itm))
        else:
            for s in list_set:
                for itm in s.list_itm:
                    if itm.exist(self.list_itm):
                        pass
                    else:
                        self.list_itm.append(itm)

    def first(self, ch1, ch2, dict_prod):
        if ch1 in Production.VT:
            return ch1
        elif ch1 in Production.VN:
            list_ch = []
            res = []
            for prod in dict_prod[ch1]:
                if prod.R[0] in Production.VT:
                    list_ch.append(prod.R[0])
                elif prod.R[0] in Production.VN:
                    list_ch.extend(self.df(prod.R[0], dict_prod))
            for ch in list_ch:
                if ch not in res:
                    res.append(ch)
                    
            if len(list_ch) == 0:
                return ch2
            else:
                return res
        else:
            return ch2
        
    def df(self, ch, dict_prod):
        chs = []
        for prod in dict_prod[ch]:
            if prod.R[0] in Production.VT:
                chs.append(prod.R[0])
            elif prod.R[0] in Production.VN:
                chs.extend(self.df(prod.R[0], dict_prod))
        return chs

    def equal(self, tmp):
        #判断两个set是否相同并同时进行超前搜索符的合并
        isequal = True
        for itm1 in self.list_itm:
            if not itm1.exist(tmp.list_itm):
                isequal = False
                return isequal
        for itm1 in tmp.list_itm:
            if not itm1.exist(self.list_itm):
                isequal = False
                return isequal
        self.merge(tmp)
        return isequal
        
    def merge(self, tmp):
        
        for itm in self.list_itm:
            for itm1 in tmp.list_itm:
                if itm.dot == itm1.dot and itm.prod == itm1.prod:
                    for ch in itm1.ch:
                        #print(type(ch))
                        if ch not in itm.ch:
                            itm.ch.append(ch)
        
    def prt(self):
        print('list_itm:', end = '\n')
        for itm in self.list_itm:
            itm.prt()
        print('dict_change:')
        for key in self.dict_change:
            print('\t' + str(key) + '   ' + self.dict_change[key])
        print()

class Itm:
    #项目集中的每个项目 S->·S,#
    def __init__(self, prod, dot ,firstch):
        self.dot = dot
        self.prod = prod
        self.ch = []
        if type(firstch) == str:
            self.ch.append(firstch)
        elif type(firstch) == list:
            self.ch.extend(firstch)

    def exist(self, list_itm):
        exi = False
        for itm in list_itm:
            if self.dot == itm.dot and self.prod == itm.prod:
                exi = True
                for ch in self.ch:
                    if ch not in itm.ch:
                        itm.ch.append(ch)
                break
        return exi

    def prt(self):
        print('---',end = ' ')
        print('\t' + self.prod.Vnl + '->', end = '')
        for i in range(len(self.prod.R) + 1):
            if i == self.dot:
                print('*', end = '')
            try:
                print(self.prod.R[i], end = '')
            except IndexError:
                pass
        print(' , ', end = '')
        for ch in self.ch:
            print(ch, end = '/')
        print()

class Action:
    def __init__(self, canon, dict_prod):
        self.dict_action = {}
        #dict_action:dict{'state':dict{'ch':'state'}}
        for state in canon.dict_set: #state = set
            self.dict_action[state] = {}
            for dic in canon.dict_set[state].dict_change:
                if dic in Production.VT:
                    self.dict_action[state][dic] = canon.dict_set[state].dict_change[dic]
            for itm in canon.dict_set[state].list_itm:
                if itm.prod.Vnl == 'start' and itm.dot == len(itm.prod.R):
                    self.dict_action[state]['#'] = '@'
                elif itm.dot == len(itm.prod.R):
                    for ch in itm.ch:
                        self.dict_action[state][ch] = itm.prod
    
    def getAction(self, state, ch):
        return self.dict_action[state][ch]

    def prt(self):
        for state in self.dict_action:
            print(state + ' :')
            for key in self.dict_action[state]:
                try:
                    print('key: ' + key + '  state: ' + self.getAction(state, key))
                except TypeError:
                    print('key: ' + key + '     r:  ' + str(self.dict_action[state][key].num))
            print()
        
class Goto:
    def __init__(self, canon):
        self.dict_goto = {}
        #dict_goto:dict{'state':dict{'ch','state'}}
        for state in canon.dict_set:
            self.dict_goto[state] = {}
            for dic in canon.dict_set[state].dict_change:
                if dic in Production.VN:
                    self.dict_goto[state][dic] = canon.dict_set[state].dict_change[dic]
    
    def getGoto(self, state, ch):
        return self.dict_goto[state][ch]

    def prt(self):
        for state in self.dict_goto:
            print(state + ' :')
            for key in self.dict_goto[state]:
                print('key: ' + key + '  state: ' + self.getGoto(state, key))
            print()