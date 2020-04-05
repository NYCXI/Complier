from Data import StateNode
from Data import Production
from Data import dfaNode

class nfa:
    def __init__(self, prodlist):
        endNode = StateNode('endNode', True)
        self.tabledic = {'endNode':endNode}
        for prod in prodlist:
            if prod.Vnl not in self.tabledic:
                if prod.Vnl == Production.S:
                    node = StateNode(prod.Vnl, False, True)
                else:
                    node = StateNode(prod.Vnl)
                self.tabledic[prod.Vnl] = node
            if prod.Vnr is not '':
                if prod.Vnr in self.tabledic:
                    self.tabledic[prod.Vnl].appendChangeFun(prod.Vt, prod.Vnr)
                else:
                    if prod.Vnr == Production.S:
                        node = StateNode(prod.Vnr, False, True)
                    else:
                        node = StateNode(prod.Vnr)
                    self.tabledic[prod.Vnr] = node
                    self.tabledic[prod.Vnl].appendChangeFun(prod.Vt, prod.Vnr)
            else:
                self.tabledic[prod.Vnl].appendChangeFun(prod.Vt, "endNode")
    
    def prt(self):
        print('nfatable:')
        print('state\t' + 'ch\t' + 'nextstate\t' + 'isStart\t' + "isEnd\t")
        for item in self.tabledic:
            print(self.tabledic[item].StateName, end='\t')
            for it in self.tabledic[item].ChangeFun:
                print(it, end = '\t')
                for i in self.tabledic[item].ChangeFun[it]:
                    print(i,end = '\t')
            print(self.tabledic[item].isStart, end = '\t')
            print(self.tabledic[item].isEnd, end = '\t')
            print()
            print()


class dfa:
    def __init__(self, nfaTable):
        self.dfaTable = {}
        self.closure1(nfaTable, [nfaTable.tabledic[Production.S]])
        i = 0
        while i < len(self.dfaTable):
            for T in list(self.dfaTable)[i:]:
                i += 1
                self.move(nfaTable,self.dfaTable[T])
            print('i: ' + str(i) + '\tii: ' + str(len(self.dfaTable)) + '\ttotNode: ' + str(dfaNode.sub))

    def closure1(self, nfaTable, Start):
        nstateslist = Start.copy()
        for item in Start:
            try:
                nstateslist.append(item.ChangeFun['@'])
            except KeyError:
                pass
        node = dfaNode(nstateslist, nfaTable)
        self.dfaTable[node.StateName] = node
        dfaNode.sub += 1

    #计算clousre闭包。并判断得到的闭包集合是否已经存在，如果存在则指建立转换关系，如果不存在，建立新的的dfa节点并添加到dfatable中
    def closure(self, nfaTable, move_list, Tstate, ch):
        nstateslist = move_list.copy()
        for item in move_list:
            try:
                if type(item.ChangeFun['@']) is list:
                    for i in item.ChangeFun['@']:
                        #print(type(i))
                        if nfaTable.tabledic[i] not in nstateslist:
                            nstateslist.append(nfaTable.tabledic[i])
                else:
                    if nfaTable.tabledic[item.ChangeFun['@']] not in nstateslist:
                        nstateslist.append(nfaTable.tabledic[item.ChangeFun['@']])
            except KeyError:
                pass

        isExist = False
        for item in self.dfaTable:
            if self.dfaTable[item].isSame(nstateslist):
                self.dfaTable[Tstate.StateName].dict_ChangeFun[ch] = self.dfaTable[item]
                isExist = True
        if not isExist:
            node = dfaNode(nstateslist, nfaTable)
            self.dfaTable[Tstate.StateName].dict_ChangeFun[ch] = node
            self.dfaTable[node.StateName] = node
            dfaNode.sub += 1
    
    #计算move(T,ch)，并直接计算move(T,ch)的闭包 方便添加节点建立节点间转换关系。
    def move(self, nfaTable, Tstate):
        for ch in Production.VT:
            move_list = []
            for state in Tstate.list_nstates:
                try:
                    #move_list.append(state.ChangeFun[ch])
                    #print(type(state))
                    if type(state) is str:
                        print(state)
                    for item in state.ChangeFun[ch]:
                        if nfaTable.tabledic[item] not in move_list:
                            move_list.append(nfaTable.tabledic[item])
                except KeyError:
                    pass
            if len(move_list) > 0:
                self.closure(nfaTable, move_list, Tstate, ch)

    def prt(self):
        file = open('out.txt',mode='w', encoding='utf-8')
        '''
        for item in self.dfaTable:
            print('state: ' + self.dfaTable[item].StateName, end = '\n')
            print('nstates:', end = '\n\t')
            for item1 in self.dfaTable[item].list_nstates:
                print(item1.StateName, end = '\t')
            print('\nChangeFun:')
            for item1 in self.dfaTable[item].dict_ChangeFun:
                print('\tch:' + str(item1) + '\t node:' + str(self.dfaTable[item].dict_ChangeFun[item1].StateName))
            print('isStart:' + str(self.dfaTable[item].isStart) + '\tisEnd:' + str(self.dfaTable[item].isEnd))
            print()
            print()
        '''
        for item in self.dfaTable:
            file.write('state: ' + self.dfaTable[item].StateName + '\n')
            file.write('nstates:' + '\n\t')
            for item1 in self.dfaTable[item].list_nstates:
                file.write(item1.StateName + '\t')
            file.write('\nChangeFun:\n')
            for item1 in self.dfaTable[item].dict_ChangeFun:
                file.write('\tch:' + str(item1) + '\t node:' + str(self.dfaTable[item].dict_ChangeFun[item1].StateName) + '\n')
            file.write('isStart:' + str(self.dfaTable[item].isStart) + '\tisEnd:' + str(self.dfaTable[item].isEnd) + '\n')
            file.write('\n')
        file.close()