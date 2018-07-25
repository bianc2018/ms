#-* -coding:GBK -* -
#����ע��ģ��
from LEX import LEX
from copy import deepcopy
import shelve
debug = 0
class LR: 
    def __init__(self,end = '#~'):
        self.lrtable = {} #s:{i:(s��r��g,state or T->asd)}
        self.Def = [] #����ʽ [A,0,abc] A->.abc
        self.vt = [] #�ս��
        self.vn = [] #���ս��
        self.code = {}#id:tag

        #coding ����
        self.end = 1001 #������
        self.start= 1002 #��ʼ��
        self.code = {self.end:end}#id:tag
        
        self.isi = 0
    def init(self,flag,db=None,LL=None): #���ݲ���ʽ ������
        if flag =="s":
            m_sf = shelve.open(db)
            self.lrtable = m_sf["LR"]["lrt"]
            self.Def = m_sf["LR"]["Def"]
            self.vt = m_sf["LR"]["vt"]
            self.vn = m_sf["LR"]["vn"]
            self.code = m_sf["LR"]["code"]
            m_sf.close()
        else:
            self.coding(LL,db)
            self.init_lrtable_slr()
        self.isi = 1
        pass
    def save(self,db):
        LRDATA = {"lrt":self.lrtable,"Def":self.Def,"vt":self.vt,"vn":self.vt,"code":self.code}
        m_sf = shelve.open(db)
        m_sf["LR"] = LRDATA
        m_sf.close()
        pass
    def coding(self,Lex,path):
        ids = 1005
        #�����Ŀ��ʶ�� ����ʽ
        Lex.update("->",'DEF',ids)
        ids+=1
        Lex.update("|",'DEF',ids)
        ids+=1
        Lex.update("~@",'DEF',ids)
        ids+=1
        Lex.update("~$",'DEF',ids)
        ids+=1
        Lex.update("@",'DEF',ids) #�����ս��
        ids+=1

        s = file(path,'r+')
        lines = s.readlines()
        s.close()
        #����Ϊ��λ���дʷ�����
        line_no = 1
        for line in lines:
            #print line_no,'\t',line
            l = Lex.getToken(line,line_no) #(id value tag row col) �����
            line_no+=1
            #����
            if l[0][1] == "@":
                #print l
                size = len(l)
                for i in range(1,size):
                    if l[i][1] == "NUM":
                        Lex.update(l[i+1][1],'DEF',Lex.NUM)
                    if l[i][1] == "ID":
                        Lex.update(l[i+1][1],'DEF',Lex.ID)
                    if l[i][1] == "CONST":
                        Lex.update(l[i+1][1],'DEF',Lex.CONST)
            elif l[0][1] == '~$':
                #print "start:",l
                self.code.update({self.start:l[1][1]})
                self.vn.append(self.start)
                Lex.update(l[1][1],'VN',self.start)
            elif l[0][1] == '~@':#���ս��
                size = len(l)
                for i in range(1,size):
                    if l[i][1] != self.decode(self.start):
                        self.code.update({ids:l[i][1]})
                        self.vn.append(ids)
                        Lex.update(l[i][1],'VN',ids)
                        ids+=1
            elif l[0][2] == "VN" and l[1][1] == '->': #����ʽ
                A = int(l[0][0])
                i = 2
                size =len(l)
                while i<size :
                    B=[A,0] #0��ʾ .������Ԫ�� size+1 ΪA->.B
                    #print 'i',i,size, l[i]
                    while l[i][1] != '|':
                        if l[i][2] !='VN' and int(l[i][0]) not in self.vt:
                            self.code.update({int(l[i][0]):l[i][1]})
                            self.vt.append(int(l[i][0]))
                        B.append(int(l[i][0]))
                        i+=1
                        if i>=size:
                            break
                    i+=1
                    self.Def.append(B)
        self.vt.append(self.end) #����ս��

        if debug:
            print "VT:",
            for t in self.vt:
                print self.decode(t),
            print ""
            print "VN:",
            for n in self.vn:
                print self.decode(n),
            print ""
        pass
    #��հ�
    def closure(self,m_def,I):
        m_I =[]
        m_I +=I
        flag = True
        while flag:
            flag = False
            for i in I:#����ʽ [A,-1,abc] A->.abc
                A = m_def[i]
                size = len(A)-2
                if A[1] !=size and A[A[1]+2] in self.vn:
                    ds = len(m_def)
                    for d in range(1,ds):
                        if A[A[1]+2] == m_def[d][0] and m_def[d][1] == 0 and d not in m_I:
                            m_I.append(d)
                            flag = True
            I = m_I
        return m_I
        pass
    def Getfirst(self,m_def):
        first = {} #{vn:[,,,]}
        f = {}#{vn:true}
        #��ʼ��
        for vn in self.vn:
            first.update({vn:[]})
            f.update({vn:True})
        for d in m_def:
                index = d[2]
                A = d[0]
                if index in self.vn:
                    f[A] = False
                if index not in first[A] and index!=A:
                    first[A].append(index)
        flag = True
        while flag:
            for A in first:
                if f[A] == True:
                    continue
                for index in first[A]:
                    #print self.decode(A),self.decode(index)
                    if index in self.vn:
                        if f[index] == True:
                            for other in first[index]:
                               if other not in first[A]:
                                   first[A].append(other)
                            first[A].remove(index)
                            #print "ADD"
                            #self.print_F({A:first[A]})
            flag = False
            for A in self.vn:
                if f[A] == True:
                    continue
                f[A] = True
                for index in first[A]:
                    if index in self.vn:
                        if debug:
                            print "vn",self.decode(index)
                            self.print_F({A:first[A]})
                        f[A] = False
                        flag = True
                        #raw_input()
                        break;
        #��ʼ��
        return first
        pass
    def Getfollow(self,first,m_def):
        follow = {} #{vn:[,,,]}
        for vn in self.vn:
            follow.update({vn:[]})
        follow.update({-2:[self.end]})
        flag = True
        while flag:
            flag = False
            for d in m_def:
                size = len(d)
                #first
                for i in range(2,size-1):
                    if d[i] in self.vn:
                        if d[i+1] in self.vt:
                            if d[i+1] not in follow[d[i]]:
                                follow[d[i]].append(d[i+1])
                                flag = True
                        else:
                            for j in first[d[i+1]]:
                                if j not in follow[d[i]]:
                                    follow[d[i]].append(j)
                                    flag = True
                #follow
                if d[size-1] in self.vn:
                    for j in follow[d[0]]:
                        if j not in follow[d[size-1]]:
                            follow[d[size-1]].append(j)
                            flag = True
        return follow
        pass
    def init_lrtable_slr(self):
        #�ķ���չ
        self.code.update({-2:"S'"})
        self.vn.append(-2)
        m_def = [[-2,0,self.start],[-2,1,self.start]]
        if debug:
            print "��չ�ķ�"
            self.print_def(m_def+self.Def)
        #�г�LR(0)������Ŀ
        for i in self.Def:
            size = len(i)-2
            for j in range(0,size+1):
                i[1] = j
                if i not in m_def:
                    m_def.append(deepcopy(i))
        #print "��Ŀ��"
        #self.print_def(m_def)
        #��first follow��
        ff = self.Def+[[-2,0,self.start]]
        first = self.Getfirst(ff)
        if debug:
            print "first:"
            self.print_F(first)
        follow = self.Getfollow(first,ff)
        if debug:
            print "follow:"
            self.print_F(follow)
        #��հ�
        I = [[0]] #I[0] ״̬0 ��������Ŀ
        num = 0
        I[num] = self.closure(m_def,I[num])
        
        while True:
            #raw_input()
            if not debug:
                print num,
                self.print_I(m_def,I[num])
            go = {} #{S:[id...]}
            for d in I[num]:
                A = m_def[d]
                size = len(A)-2
                if A[1] !=size and (d+1) not in I[num]:#��2 A->B B 2��ʼ
                    if A[A[1]+2] not in go.keys():
                        go.update({A[A[1]+2]:[d+1]})
                    else:
                        go[A[A[1]+2]].append(d+1)
            #print go
            for g in go:
                K = self.closure(m_def,go[g])
                if K not in I:
                    I.append(K)
                    #print "GOTO(",num,self.code[g],")",len(I)-1
            num=num+1
            if num>=len(I):
                break
        #Goto={} #()=
        #��ʼ��LR��0��������
        #acc 1 S'->S
        #N = None #��
        #R = ['r',[]] #��Լ
        #S = ['s',0]   #�ƽ�
        #ACC=['a']
        for row in range(0,len(I)):
            rows = {}
            for colt in self.vt:
                rows.update({colt:None})
            for coln in self.vn:
                rows.update({coln:None})
            self.lrtable.update({row:deepcopy(rows)})
        #����LR(0)��
        for i in range(0,len(I)): #I[i] ״̬i��������Ŀ
            go = {} #{S:[id...]}
            #print I[i]
            for d in I[i]:
                A = m_def[d]
                size = len(A)-2
                if d == 1:
                    self.lrtable[i][self.end] = ['a']
                elif A[1] ==size:
                    R = ['r',m_def[d]]
                    for j in self.vt:
                        if j in follow[A[0]]:
                            if self.lrtable[i][j] == None:
                                self.lrtable[i][j] = R
                            else:
                                r= self.lrtable[i][j]
                                ds = m_def.index(r[1])
                                if d>ds:
                                    self.lrtable[i][j] = R
                else:
                    if A[A[1]+2] not in go.keys(): #.��
                        go.update({A[A[1]+2]:[d+1]})
                    else:
                        go[A[A[1]+2]].append(d+1)
            for g in go:
                for j in range(0,len(I)):
                    if go[g][0] in I[j]:
                        #print i,self.decode(g),"->",j
                        s = self.lrtable[i][g]
                        #self.lrtable[i][g] = ["s",j]
                        if s==None:
                            self.lrtable[i][g] = ["s",j]
                        else:
                            if s[0] =="r":
                                ds = m_def.index(s[1])
                                if go[g][0]>ds:
                                    self.lrtable[i][g] = ["s",j]
        #print "I"
        #for num in range(0,len(I)):
        #   print num,
        #   self.print_I(m_def,I[num])
        #self.print_r0()
        pass
    def analysis_exec(self,tokens): #�������
        if self.isi == 0:
            print "LRδ��ʼ��"
            return NULL
        stack = [(0,self.end,("end",-1))] #state tag value
        tokens+=[(self.end,self.decode(self.end),"END",-1,-1)] #��ӽ����� (id value tag row col) �����
        t_s = len(tokens)
        #print tokens
        #�����-(��Լ��ǩ,[])
        execs = []
        e = 0
        t=0
        while t<t_s:#(id value tag row col) �����
            top = stack[-1] #ȡջ��Ԫ��
            token = tokens[t]#ȡԪ��
            if debug:
                print "--------------:input-token",token
                #print stack
                print "s:",
                for s in stack:
                    print str(s[0]).center(5," "),
                print "\nt:",
                for s in stack:
                    print self.decode(s[1]).center(5," "),
                print "\nv:",
                for s in stack:
                    print str(s[2][0]).center(5," "),
                print "\nv:",
                for s in stack:
                    print str(s[2][1]).center(5," "),
                print ""
            #print top
            #print token
            if token[0] not in self.vt :
                print "ERROR:NOT FIND",token[0],self.decode(token[0]),"in","rows:",token[3],"cols:",token[4]
                return None
            tcell = self.lrtable[top[0]][token[0]] #��LR�� tab(pre-state,iput-id)
            #print "about:",top[0],token[0],tcell
            if tcell==None:#�գ�ʧ��
                print "������󣺲���Ҫ",token[1],"rows:",token[3],"cols:",token[4]
                return None
            elif tcell[0] == 'a':#acc �ɹ�
                return execs
            elif tcell[0] == 's':#�ƽ� 
                if  token[2]=="ID" or token[2]=="OP" or token[2]=="TYPE" or token[2]=="CONST":
                    stack_top = (tcell[1],token[0],(token[2],token[1]))
                elif token[2]=="NUM":
                    stack_top = (tcell[1],token[0],(token[2],int(token[1])))
                else:
                    stack_top = (tcell[1],token[0],("NONE",token[1]))
                stack.append(stack_top)
                if debug:
                    print "�ƽ�:",top[0],self.decode(token[0]),"->",tcell[1]
                t=t+1
            elif tcell[0] == 'r': #��Լ
                v = tcell[1]
                p = []
                for i in range(len(v)-1,1,-1): #
                    if v[i] == stack[-1][1]:
                        value = stack.pop()
                        if value[2][0]!="NONE":
                            p.append(value[2]) #ȡֵ\
                    else:
                        self.print_def([v])
                        print "ERROR:��Լʧ��-",v,"need:",self.decode(v[i]),"top:",self.decode(stack[-1][1])
                        return False
                p.reverse()
                execs.append((self.decode(v[0]),p))
                if debug:
                    print "��Լ:",
                    self.print_def([v])
                #GOTO
                top = stack[-1]
                tcell = self.lrtable[top[0]][v[0]]
                if tcell==None:
                    print "ERROR:GOTOʧ��-",top[0],self.decode(v[0])
                    return None
                if debug:
                    print "GOTO:",top[0],self.decode(v[0]),"->",tcell[1]
                stack.append((tcell[1],v[0],(self.decode(v[0]),e)))
                e=e+1
        return execs
        pass
    def encode(self,value): #tag->id
        for key in self.code:
            if value == self.code[key]:
                return key
        return None
    def decode(self,key):#id ->tag
        if key in self.code.keys():
            return self.code[key]
        return None
    def print_def(self,d):
        num = 0
        for A in d:
            print num,A[1],self.decode(A[0]),'->',
            num+=1
            size = len(A)
            for i in range(2,size):
                if i-2 == A[1]:
                    print '.',
                print self.decode(A[i]),
            if A[1] == size-2:
                print '.',
            print ''
    def print_code(self):
        for i in self.code:
            print str(i).center(10,' '),str(self.code[i]).center(10,' ')
    def print_I(self,m_def,I):
        print "I"
        for d in I:
            A = m_def[d]
            print d,A[1],self.decode(A[0]),'->',
            size = len(A)
            for i in range(2,size):
                if i-2 == A[1]:
                    print '.',
                print self.decode(A[i]),
            if A[1] == size-2:
                print '.',
            print ''
    def print_table(self):
        print "slr:".center(10," "),
        for c in self.lrtable[0]:
                print self.code[c].center(10," "),
        print ""
        for r in self.lrtable:
            print str(r).center(10," "),
            for c in self.lrtable[r]:
                k = self.lrtable[r][c]
                s = ''
                if k==None:
                    s=""
                elif k[0]=='s':
                    s=k[0]+str(k[1])
                elif k[0]=='r':
                    s=k[0]+":"+self.decode(k[1][0])+'->'
                    size = len(k[1])
                    for i in range(2,size):
                        s+=self.decode(k[1][i])
                elif k[0] == 'a':
                    s=k[0]
                print s.center(10," "),
                
            print "\n"
    def print_r0(self):
        for r in self.lrtable:
            print str(r).center(10," "),
            ic=0
            for c in self.lrtable[r]:
                print self.code[c],":",
                k = self.lrtable[r][c]
                s = ''
                if k==None:
                    s=""
                elif k[0]=='s':
                    s=k[0]+str(k[1])
                elif k[0]=='r':
                    s=k[0]+":"+self.decode(k[1][0])+'->'
                    size = len(k[1])
                    for i in range(2,size):
                        s+=self.decode(k[1][i])
                elif k[0] == 'a':
                    s=k[0]

                print s.center(15," "),
                ic+=1
                if ic==8:
                    print "\n",str(r).center(10," "),
                    ic=0
            print "\n"
    def print_F(self ,f):
        for vn in f:
            print self.decode(vn),"->",
            for i in f[vn]:
                print self.decode(i),
            print ""
if __name__ == '__main__':
    lex = LEX() #�ʷ�������ʵ��
    lex.init("s","data")
    lr = LR()
    ll = LEX()
    ll.init("s","data")
    lr.init("t","LRset.txt",ll)
    lr.save("data")
    #lr.print_table()
    while True:
        l = [] #�����
        script = raw_input(">") #��ȡָ��
        if len(script)==0:
            continue
        elif script[0]!='@': #�����Ǵ���
            l += lex.getToken(script) #�ʷ�����
        else:
            path = script[1:] #�������ļ�·������Ƭ��ȡ�ļ�·��
            s = file(path,'r+')
            lines = s.readlines()
            s.close()

            line_no = 1
            for line in lines:
                l += lex.getToken(line,line_no)
                line_no+=1
        print "@SLR(1):"
        E = lr.analysis_exec(l)
        if E==None:
            continue
        for e in range(0,len(E)):
            print e,E[e]