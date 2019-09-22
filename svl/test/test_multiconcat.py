# SET "PYTHONPATH=C:\{path}\svl"
import svl.parser as svlparser

svlstr = """

Reuse
    a = "a"
    b = "b"

ElA
    attrA = "#Reuse.a##Reuse.b#"
    attrB = "#Reuse.b##Reuse.a#"

ElB
    attrA = "#Reuse.a##Reuse.b#"
    attrB = "#Reuse.b##Reuse.a#"

"""

def main():
    elements = svlparser.parse(svlstr)
    verifyStack = ["ElA", "ElB"]
    verifiedCnt = 0
    try:
        for el in elements:
            if el.name in verifyStack:
                if el.get('attrA') == 'ab':
                    if el.get('attrB') == 'ba':
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
