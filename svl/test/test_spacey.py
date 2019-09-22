# SET "PYTHONPATH=C:\{path}\svl"
from svl import parser as svlparser

svlstr = """

ElA

        attrA        =        "a"        

        attrB        =        "b"        

ElB

        attrA        =        "a"        

        attrB        =        "b"        

"""

def main():
    elements = svlparser.parse(svlstr)
    verifyStack = ["ElA", "ElB"]
    verifiedCnt = 0
    try:
        for el in elements:
            if el.name in verifyStack:
                if el.get('attrA') == 'a':
                    if el.get('attrB') == 'b':
                        verifiedCnt += 1
    except:
        import sys
        print("EXCEPTION")
        print("Unexpected error:", sys.exc_info())
        print("FAIL")
        return
    if len(verifyStack) != verifiedCnt:
        print("FAIL")
    else:
        print("PASS")
if __name__ == '__main__':
    main()
