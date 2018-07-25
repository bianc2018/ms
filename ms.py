#-* -coding:GBK -* -
#中文注释模板
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
    lex = LEX() #词法分析器实例
    lex.init("s","data")
    lr = LR()
    lr.init("s","data")
    #lr.print_table()
    ex = EXEC()
    attr={} #数据栈
    while True:
        script = raw_input(">") #获取指令
        if len(script)==0:
            continue
        elif script[0]!='@': #输入是代码
            l = lex.getToken(script) #词法分析
            if l == None:
                continue
            E = lr.analysis_exec(l)
            if E==None:
                continue
            #for e in range(0,len(E)):
                #print e,E[e]
            rt = ex.run(E,-1,attr) 
        else:
            path = script[1:] #输入是文件路径，切片提取文件路径
            l = lex.getToken(path) #词法分析
            if l[0][1] == "runt":
                if os.path.exists(l[1][1]) == False:
                    print "not find",l[1][1]
                    continue
                s = shelve.open(l[1][1])
                if s["Version"]!=version:
                    print "编译版本不一致，当前:",version,",需要:",s["Version"]
                    continue
                if s.has_key("Code"):
                    rt = ex.run(s["Code"])
                    print "\n运行结束，返回:",rt
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
                    print "\n运行结束，返回:",rt
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
                print "参数栈已清空"
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