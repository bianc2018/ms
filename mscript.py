#-* -coding:GBK -* -
#中文注释模板
#-* -coding:GBK -* -
#中文注释模板
from LEX import LEX
from LR import LR
from EXEC import EXEC
if __name__ == '__main__':
    lex = LEX() #词法分析器实例
    ll = LEX()
    lr = LR(ll)
    ex = EXEC()

    while True:
        l = [] #结果集
        script = raw_input(">") #获取指令
        if len(script)==0:
            continue
        elif script[0]!='@': #输入是代码
            l += lex.getToken(script) #词法分析
        else:
            path = script[1:] #输入是文件路径，切片提取文件路径
            s = file(path,'r+')
            lines = s.readlines()
            s.close()
            line_no = 1
            for line in lines:
                l += lex.getToken(line,line_no)
                line_no+=1
        print "@SLR1:"
        E = lr.analysis_exec(l)
        if E==None:
            continue
        for e in range(0,len(E)):
            print e,E[e]
        rt = ex.run(E)
        print "RETURN ：",rt 