load "io.ms"
//ÇóºÍ0...i
func sum(i)
{
    s = 0;
    j = 0;
    for(j;0,i,1)
    {
        s=s+j+1;
        output(s);
        output("=");
        output(s-j);
        output("+");
        output(j);
        output("+1");
        LINEEND;
    }
    return s;
}