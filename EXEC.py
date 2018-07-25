#-* -coding:GBK -* -
#����ע��ģ��
from LEX import LEX
from LR import LR
debug = 0
class EXEC:
    def __init__(self):
        self.attr = {} #����ջid��value,type
        self.func = {"CONST":self.CONST,
                     "RETURN":self.RETURN,
                     "OUT":self.OUT,
                     "IN":self.IN,
                     "MAIN":self.MAIN,
                     "CODE":self.CODE,
                     "WHILE":self.WHILE,
                     "IF":self.IF,
                     "FOR":self.FOR,
                     "A":self.A,
                     "E":self.E,
                     "I":self.I,
                     "ID":self.ID,
                     "NUM":self.NUM,
                     "FUNC":self.FUNC,
                     "EXFUNC":self.EXFUNC,
                     "LE":self.LE
                     }
        self.rt=None
        self.qcode = None
        pass
    def init(self):
        self.attr = {} #����ջid��value,type
        self.rt=None
        self.qcode = None
    def run(self,execs,p=-1,attr=None):
        if attr==None:
            self.attr={}
            self.rt=None
            self.qcode = None
        else:
            self.attr=attr
        self.execs = execs
        if p ==-1:
            size = len(execs)
            return self.MAIN(size-1)
        return self.MAIN(p)
    def MAIN(self,p):
        #print p;
        node = self.execs[p]
        if self.qcode!=None:
            return None
        if node[0]!="MAIN":
            print "ERROR:������ļ�:MAIN",node[0],p
            self.qcode = -1
            return None
        if debug:
            print "MAIN:",p,"qcode:",self.qcode
        for n in node[1]:
            self.func[n[0]](n[1])
        return self.rt
    def FUNC(self,p):
        node = self.execs[p]
        if self.qcode!=None:
            return None
        if node[0]!="FUNC":
            print "ERROR:������ļ�:FUNC",node[0]
            self.qcode = -1
            return None
        if debug:
            print "FUNC:",p,"qcode:",self.qcode
        if len(node[1])==2:
            funcname = node[1][0][1]
            begin = node[1][1][1]
            self.attr.update({funcname:[begin,"func",[]]})
            return 
        funcname = node[1][0][1]
        
        begin = node[1][2][1]
        par=[]
        next=node[1][1][1];
        while True:
            List = self.execs[next]
            if List[0] =="LIST":
                next = List[1][0][1]
            elif List[0] == "LISTL":
                if len(List[1])==2:
                    par+=[List[1][1][1]]
                    next = List[1][0][1]
                else:
                    par +=[List[1][0][1]]
                    break
        #print "par",par
        par.reverse()
        #print "par_r",par
        self.attr.update({funcname:[begin,"func",par]})
        return
    def EXFUNC(self,p):
        node = self.execs[p]
        if self.qcode!=None:
            return None
        if node[0]!="EXFUNC":
            print "ERROR:������ļ�:EXFUNC",node[0]
            self.qcode = -1
            return None
        if debug:
            print "EXFUNC:",p,"qcode:",self.qcode
        func_attr = {}
        exfunc = EXEC()
        funcname = node[1][0][1]
        begin = 0
        var = []
        if funcname in self.attr.keys():
            begin = self.attr[funcname][0]
        else:
            print "����",funcname,"δ����"
            self.qcode = -6
            return None
        if len(node[1])==2:
            next=node[1][1][1];
            while True:
                List = self.execs[next]
                #print List
                if List[0] =="EXLIST":
                    next = List[1][0][1]
                elif List[0] == "EXLISTL":
                    if len(List[1])==2:
                        var +=[self.func[List[1][1][0]](List[1][1][1])]
                        next = List[1][0][1]
                    else:
                        var +=[self.func[List[1][0][0]](List[1][0][1])]
                        break
        #print "var",var
        var.reverse()
        #print "var_r",var
        #print "attr",self.attr
        par = self.attr[funcname][2]
        if len(var)!=len(par):
            print "������",funcname,"�������ԣ���Ҫ",len(par),"����",len(var)
            self.qcode = -7
            return None
        for i in range(0,len(par)):
            func_attr.update({par[i]:[var[i][0],var[i][1]]})
        #��������
        for a in self.attr:
            if a not in func_attr:
                func_attr.update({a:self.attr[a]})
        #print "ִ��",funcname
        rt = exfunc.run(self.execs,begin,func_attr)
        #print "����",funcname,rt
        if debug:
            print "EXFUNC:",funcname
            print "���������"
            print func_attr
            for f in func_attr:
                print f,func_attr[f][0],func_attr[f][1]
            print "retrun",rt
        return rt
    def CODE(self,p):
        if self.qcode!=None:
            return
        node = self.execs[p]
        if node[0]!="CODE":
            print "ERROR:������ļ���CODE",node[0]
            self.qcode=-1
            return None
        if debug:
            print "CODE:",p,"qcode:",self.qcode
        if debug:
            print "CODE",p,"node",node
        if len(node[1])==0:
            return None
        self.func[node[1][0][0]](node[1][0][1])
    #WHILE->while(B){CODE} //while�ṹ
    def WHILE(self,p):
        if self.qcode!=None:
            return
        node = self.execs[p]
        if node[0]!="WHILE":
            print "ERROR:������ļ���WHILE",node[0]
            self.qcode=-1
            return None
        if debug:
            print "WHILE:",p,"qcode:",self.qcode
        b = node[1][0][1]
        c = node[1][1][1]
        while(self.E(b)[0]):
            self.MAIN(c)
    #IF->if(B){CODE}|if(B){CODE}else {CODE}//if�ṹ
    def IF(self,p):
        if self.qcode!=None:
            return
        node = self.execs[p]
        if node[0]!="IF":
            print "ERROR:������ļ���IF",node[0]
            self.qcode=-1
            return None
        if debug:
            print "IF:",p,"qcode:",self.qcode
        if len(node[1])==2:
            b = node[1][0][1]
            c1 = node[1][1][1]
            e = self.E(b);
            if e[0]:
                self.MAIN(c1)
        else:
            b = node[1][0][1]
            c1 = node[1][1][1]
            c2 = node[1][2][1]
            e = self.E(b);
            #print e
            if e[0]:
                self.MAIN(c1)
            else:
                self.MAIN(c2)
        pass
    #FOR->for(i;j,j,j){CODE}//for�ṹ i ��ʼ j ���� j ���� j (ID,IDname)
    def FOR(self,p):
        if self.qcode!=None:
            return
        node = self.execs[p]
        if node[0]!="FOR":
            print "ERROR:������ļ���FOR",node[0]
            self.qcode=-1
            return None
        if debug:
            print "FOR:",p,"qcode:",self.qcode
        i = node[1][0][1] #����
        s = self.func[node[1][1][0]](node[1][1][1])
        e = self.func[node[1][2][0]](node[1][2][1])
        d = self.func[node[1][3][0]](node[1][3][1])
        c = node[1][4][1]
        #print s,e,d
        if i in self.attr.keys():
            for self.attr[i][0] in range(s[0],e[0],d[0]):
                self.MAIN(c)
        else:
            print "ERROR������",i,"δ����!"
    #A->i=E;
    def A(self,p):
        if self.qcode!=None:
            return
        node = self.execs[p]
        if node[0]!="A":
            print "ERROR:������ļ� A",node[0]
            self.qcode=-1
            return None
        if debug:
            print "A:",p,"qcode:",self.qcode
        i = node[1][0][1]
        e = node[1][1][1]
        v = self.attr[i] = self.func[node[1][1][0]](e)
        if i in self.attr.keys():
            self.attr[i] = v
        else:
            self.attr.updata({i:v})
        pass
    #B->B or B|B and B|not B|(B)|I==I|I<=I|I>=I|I<I|I>I|I!=I|I //����
    def E(self,p):
        if self.qcode!=None:
            if debug:
                print "qcode:",self.qcode
            return
        node = self.execs[p]
        if node[0]!="E":
            print "ERROR:������ļ� E",node[0]
            self.qcode=-1
            return None
        if debug:
            print "E:",p,"qcode:",self.qcode,node
        if len(node[1])==1:
            v= self.func[node[1][0][0]](node[1][0][1])
            if v:
                #print "v",v,node[1][0][0],node[1][0][1]
                return v
            else:
                if node[1][0][0] == "EXFUNC":
                    return None
                print "line 262 ",p,"None:",v
                self.qcode=-4;
                return None
        elif len(node[1])==2:
            op = node[1][0][1] 
            i = node[1][1][1]
            if op=="not":
                v = self.func[node[1][0][0]](i)
                if v[1]!="CONST":
                    return not self.func[node[1][0][0]](i)
                else:
                    print "�����ַ���������",op,"����"
                    self.qcode=-4
                    return None;
        else:
            i = node[1][0][1]
            op = node[1][1][1]
            j = node[1][2][1]
            left = self.func[node[1][0][0]](i)
            right = self.func[node[1][2][0]](j)
            if left[1] != right[1]:
                print "����",left[1],op,right[1]
                self.qcode=-4
                return None
            #print self.attr
            #print "op::",i,op,j,type(left),type(right),node[1][0][0],node[1][2][0]
            if op=="+":
                var = left[0] + right[0]
            elif op == "-":
                var = left[0] - right[0]
            elif op == "*":
                var = left[0] * right[0]
            elif op == "/":
                var = left[0] / right[0]
            elif op=="and":
                var = left[0] and right[0]
            elif op == "or":
                var = left[0] or right[0]
            elif op == "<":
                var = left[0] < right[0]
            elif op == ">":
                var = left[0] > right[0]
            elif op == ">=":
                var = left[0] >= right[0]
            elif op == "<=":
                var = left[0] <= right[0]
            elif op == "==":
                var = left[0] == right[0]
            elif op == "!=":
                var = left[0] != right[0]
            else:
                print "ERROR��δ���������",op
                self.qcode=-3
                return None;
            return [var,left[1]]
        pass
    def I(self,p):
        if self.qcode!=None:
            return
        node = self.execs[p]
        if node[0]!="I":
            print "ERROR:������ļ� I",node[0]
            self.qcode=-1
            return None
        if debug:
            print "I:",p,"qcode:",self.qcode
        ps = node[1][0][0]
        return self.func[ps](node[1][0][1])
        pass
    def IN(self,p):
        if self.qcode!=None:
            return
        node = self.execs[p]
        if node[0]!="IN":
            print "ERROR:������ļ� IN",node[0]
            self.qcode=-1
            return None
        if debug:
            print "IN:",p,"qcode:",self.qcode
        i = node[1][0][1]
        if i in self.attr.keys():
            c= raw_input()
            if self.attr[i][1] !="CONST":
                self.attr[i][0] = int(c)
            else:
                self.attr[i][0] = c
        else:
            print "ERROR������",i,"δ����!"
            self.qcode=-2
        pass
    def OUT(self,p):
        if self.qcode!=None:
            return
        node = self.execs[p]
        if node[0]!="OUT":
            print "ERROR:������ļ� OUT",node[0]
            self.qcode=-1
            return None
        if debug:
            print "OUT:",p,"qcode:",self.qcode
        i = node[1][0][0]
        j = node[1][0][1]
        #print "i:",i,"j:",j
        output = self.func[i](j)
        if output:
            print output[0],
        else:
            print "None"
    def RETURN(self,p):
        if self.qcode!=None:
            return
        node = self.execs[p]
        if node[0]!="RETURN":
            print "ERROR:������ļ� RETURN",node[0]
            self.qcode=-1
            return None
        if debug:
            print "RETURN:",p,"qcode:",self.qcode
        if len(node[1])==0:
            self.qcode = 0
        else:
            self.rt = self.func[node[1][0][0]](node[1][0][1])
            self.qcode = 0
    def NUM(self,p):
        if self.qcode!=None:
            return
        if debug:
            print "NUM:",p
        return [p,"NUM"]
    def CONST(self,p):
        if self.qcode!=None:
            if debug:
                print "qcode:",qcode
            return None
        if debug:
            print "CONST:",p,"qcode:",self.qcode
        return [p,"CONST"]
    def ID(self,p):
        if self.qcode!=None:
            return None
        if debug:
            print "ID:",p,"qcode:",self.qcode
        if p in self.attr.keys():
            return self.attr[p]
        else:
            print "ERROR������",p,"δ����!"
            self.qcode=-1
            return None
    def LE(self,p):
        if self.qcode!=None:
            if debug:
                print "qcode:",qcode
            return None
        if debug:
            print "CONST:",p,"qcode:",self.qcode
        print ""
if __name__ == "__main__":
    lex = LEX() #�ʷ�������ʵ��
    lex.init("s","data")
    lr = LR()
    lr.init("s","data")
    #lr.print_table()
    ex = EXEC()
    attr={} #����ջ
    s = file("1",'r+')
    lines = s.readlines()
    s.close()
    line_no = 1
    Tokens = []
    for line in lines:
        T = lex.getToken(line,line_no)
        if T==None:
            print "ERROR:dont KNOW"
            break
        Tokens+=T
        line_no+=1
    E = lr.analysis_exec(Tokens)
    if E!=None:
        for e in range(0,len(E)):
            print e,E[e]
        rt = ex.run(E)
        print "���н���������:",rt