#-* -coding:GBK -* -
#����ע��ģ��
from LEX import LEX
from LR import LR
from EXEC import EXEC
import shelve
import os
# @ run Path
# @ complie path -o dist
# @ init
version = "MScript@20180613.1"
if __name__ == '__main__':
    lex = LEX() #�ʷ�������ʵ��
    lex.init("s","data")
    lr = LR()
    lr.init("s","data")
    #lr.print_table()
    ex = EXEC()
    attr={} #����ջ
    while True:
        script = raw_input(">") #��ȡָ��
        if len(script)==0:
            continue
        elif script[0]!='@': #�����Ǵ���
            l = lex.getToken(script) #�ʷ�����
            if l == None:
                continue
            E = lr.analysis_exec(l)
            if E==None:
                continue
            #for e in range(0,len(E)):
                #print e,E[e]
            rt = ex.run(E,-1,attr) 
        else:
            path = script[1:] #�������ļ�·������Ƭ��ȡ�ļ�·��
            l = lex.getToken(path) #�ʷ�����
            if l[0][1] == "runt":
                if os.path.exists(l[1][1]) == False:
                    print "not find",l[1][1]
                    continue
                s = shelve.open(l[1][1])
                if s["Version"]!=version:
                    print "����汾��һ�£���ǰ:",version,",��Ҫ:",s["Version"]
                    continue
                if s.has_key("Code"):
                    rt = ex.run(s["Code"])
                    print "\n���н���������:",rt
            elif l[0][1] == "run":
                if os.path.exists(l[1][1]) == False:
                    print "not find",l[1][1]
                    continue
                s = file(l[1][1],'r+')
                lines = s.readlines()
                s.close()
                line_no = 1
                Tokens = []
                for line in lines:
                    T = lex.getToken(line,line_no)
                    if T==None:
                        print "ERROR:dont KNOW"
                    Tokens+=T
                    line_no+=1
                E = lr.analysis_exec(Tokens)
                if E!=None:
                    rt = ex.run(E)
                    print "\n���н���������:",rt
                else:
                    continue
            elif l[0][1] == "complie":
                if os.path.exists(l[1][1]) == False:
                    print "not find",l[1][1]
                    continue
                s = file(l[1][1],'r+')
                lines = s.readlines()
                s.close()
                line_no = 1
                Tokens = []
                for line in lines:
                    T = lex.getToken(line,line_no)
                    if T==None:
                        print "ERROR:dont KNOW"
                    Tokens+=T
                    line_no+=1
                E = lr.analysis_exec(Tokens)
                if E==None:
                    continue
                t = shelve.open(l[2][1])
                t["Code"] = E
                t["Version"] = version
                t.close()
                print "Complie Over!"
            elif l[0][1] == "clear":
                attr={}
                print "����ջ�����"
            elif l[0][1] == "print":
                if os.path.exists(l[1][1]) == False:
                    print "not find",l[1][1]
                    continue
                s = shelve.open(l[1][1])
                print "Version:",s["Version"]
                print "Code:"
                E = s["Code"]
                if E!=None:
                    for e in range(0,len(E)):
                        print e,E[e]
                else:
                    continue