#-* -coding:GBK -* -
#����ע��ģ��
#-* -coding:GBK -* -
#����ע��ģ��
from LEX import LEX
from LR import LR
from EXEC import EXEC
if __name__ == '__main__':
    lex = LEX() #�ʷ�������ʵ��
    ll = LEX()
    lr = LR(ll)
    ex = EXEC()

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
        print "@SLR1:"
        E = lr.analysis_exec(l)
        if E==None:
            continue
        for e in range(0,len(E)):
            print e,E[e]
        rt = ex.run(E)
        print "RETURN ��",rt 