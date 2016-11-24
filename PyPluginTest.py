import string



class CMyClass:

    def HelloWorld(self):
        print 'HelloWorld'



class SecondClass:

    def invoke(self,obj):

        obj.HelloWorld()



def HelloWorld(strName1):

    return "Hello "+strName1

def Add(a, b, c):

    return a + b + c



def AddMult(a, b):

    """

    """

    print "in FunctionAddMult..."

    print a

    print b

    return a + b, a * b



def StringToUpper(strSrc):

    return string.upper(strSrc)

def NewsCollect(sUrl):
    return sUrl + "  success !!!!"