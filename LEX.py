#-* -coding:GBK -* -
#����ע��ģ��
#lex �ʷ�������
import sys
import shelve
import os
tag = ['ID','RES','NUM','OP','DEF',"NOTE","DEL","TYPE","CONST","EXTEND"]
default_set = "./LEXset.txt"
class LEX:
    def __init__(self):
        self.pts = {} #value (tag,id)
        self.ID  = 0
        self.NUM  = 0
        self.CONST = 0
        self.isi = 0
        self.constv="\""
    #��ʼ��
    def init(self,type,sf):
        if type == "s":
            m_sf = shelve.open(sf)
            self.pts = m_sf["LEX"]["pts"]
            self.ID = m_sf["LEX"]["ID"]
            self.NUM = m_sf["LEX"]["NUM"]
            self.CONST = m_sf["LEX"]["CONST"]
            self.constv=m_sf["LEX"]["CONSTV"]
            m_sf.close()
        else: 
            #��ȡ�����ļ�
            set = file(sf,'r+')
            lines = set.readlines()
            set.close()
            #���ж�ȡ
            for line in lines:
                line = line.replace('\n','') #���Ի��з�
                if len(line)==0 or line[0] == '#':#���л�ע���в�����
                    continue
                else:
                    v = line.split(' ') #��һ���ո񻮷��ַ��� tag id value
                    if v[0] in tag: # v[0]Ϊ���
                        if v[0] == 'ID':
                            self.ID = int(v[1])
                        elif v[0] == 'NUM':
                            self.NUM = int(v[1])
                        elif v[0] == 'CONST':
                            self.CONST = int(v[1])
                            self.constv = v[2]
                            self.pts.update({v[2]:(v[0],int(v[1]))})
                        else:
                            self.pts.update({v[2]:(v[0],int(v[1]))})
                    else:
                        print "ERROR: NOT FIND TAG:",ord(v[0]) #����
        self.isi = 1
    #�ʷ�����
    def getToken(self,script,row = 1):
        if self.isi==0:
            print "LEXδ��ʼ��������\n"
            return None
        Token = [] #(id value tag row col) �����
        script = script.replace('\n','')
        size = len(script)
        i = 0
        while i<size:
            if script[i] == ' ' or script == '\t' : #���Կո��tab
                i+=1
                continue
            else:
                s ='' #�ַ�tag
                if script[i] == self.constv:
                    i+=1
                    while i <size:
                        if script[i] == self.constv:
                            i+=1
                            break
                        else:
                            s+=script[i]
                            i+=1
                    Token.append((self.CONST,s,'CONST',row,i-len(s)))
                elif self.ischar(script[i]): #����ĸ��ͷ��ֱ��������ĸ������
                    s+=script[i]
                    i+=1
                    while i<size:
                        if self.ischar(script[i]) or self.isint(script[i]): #��ʶ��
                            s+=script[i]
                            i+=1
                        else:
                            break
                    if s in self.pts.keys(): #�Ǳ�����
                        v = self.pts[s]
                        Token.append((int(v[1]),s,v[0],row,i-len(s)))
                    else:#�����Ǳ�ʶ��
                        Token.append((self.ID,s,'ID',row,i-len(s)))
                elif self.isint(script[i]):#�����ֿ�ͷ��ֱ����������
                    s+=script[i]
                    i+=1
                    while i<size:
                        if self.isint(script[i]):
                            s+=script[i]
                            i+=1
                        else:
                            break
                    Token.append((self.NUM,int(s),'NUM',row,i-len(s)))
                else:
                    j = i
                    s+=script[j]
                    j+=1
                    while j<size: #�����ǵ�
                        if not self.isint(script[j]) and not self.ischar(script[j]):
                            s+=script[j]
                            j+=1
                        else:
                            break
                    #print s
                    while len(s) != 0:
                        if s in self.pts.keys():
                            v = self.pts[s]
                            if v[0] == "NOTE":
                                return Token
                            Token.append((int(v[1]),s,v[0],row,j-len(s)))
                            
                            i =j
                            break
                        s= s[:-1] #sȥ����β
                        j=j-1
                        #print s
                    #print s,i,j,size
                    if len(s)==0:
                        print "ERROR NOT DEFINE:",ord(script[i]),script[i],'row',row,'cols',i,'at',script[:i]
                        return None
                        i+=1
                
                
                if len(Token)>=2:
                    L = Token[-2]
                    F = Token[-1]
                    ext = []
                    if L[2] == "EXTEND":
                        if F[2] == "CONST":
                            if os.path.exists(F[1]) == False:
                                print "not find",F[1]
                                return None
                            f = open(F[1],"r+")
                            lines = f.readlines()
                            f.close()
                            for line in lines:
                                ext += self.getToken(line,-1)
                            Token.pop()
                            Token.pop()
                            Token+=ext
                        else:
                            print "EXTEND ",L[1],"need file:"
                            return None
        return Token #���ؽ��

    def ischar(self,c):
        c = c.upper()
        if ord('A')<=ord(c)<=ord('Z'):
            return True
        else:
            return False
    def isint(self,c):
        if ord('0')<=ord(c)<=ord('9'):
            return True
        else:
            return False
    def update(self,value,tag,id):
        self.pts.update({value:(tag,id)})
    def ptable(self):
        size = len(self.pts)
        for pt in self.pts:
            print self.pts[pt][0],self.pts[pt][1],pt
        print 'ID',self.ID,'_'
        print 'NUM',self.NUM,'_'
    def save(self,sf):
         m_sf = shelve.open(sf)
         LEXDATA={"pts":self.pts,"ID":self.ID,"NUM":self.NUM,"CONST":self.CONST,"CONSTV":self.constv}
         m_sf["LEX"] = LEXDATA
         m_sf.close()
#���Ե�Ԫ
if __name__ == "__main__":
    lex = LEX() #�ʷ�������ʵ��
    lex.init("t","LEXset.txt")
    lex.save("data")
    lex.ptable()
    while True:
        l = [] #�����
        script = raw_input(">") #��ȡָ��
        if script[0]!='@': #�����Ǵ���
            l += lex.getToken(script) #�ʷ�����
        else:
            path = script[1:] #�������ļ�·������Ƭ��ȡ�ļ�·��
            s = file(path,'r+')
            lines = s.readlines()
            s.close()
            #����Ϊ��λ���дʷ�����
            print "@CODE:"
            line_no = 1
            for line in lines:
                print line_no,'\t',line,
                l += lex.getToken(line,line_no)
                line_no+=1
        #��ӡ���
        print "\n@LEX:"
        print "id".center(10,' '),"value".center(10,' '),"tag".center(10,' '),"rows".center(10,' '),"col".center(10,' '),'\n'
        for i in l:
                print str(i[0]).center(10,' '),str(i[1]).center(10,' '),str(i[2]).center(10,' '),str(i[3]).center(10,' '),str(i[4]).center(10,' ')

