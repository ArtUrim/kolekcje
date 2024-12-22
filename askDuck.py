# coding: utf-8
import ddgr

def getRes( isbn : str ):
    ddgr.DdgCmd.colors = None
    opt=ddgr.parse_args( ['site:lubimyczytac.pl', isbn, '--json', '-r' 'pl-pl'] )
    r=ddgr.DdgCmd( opt, ddgr.USER_AGENT )
    r.fetch()
    if r.results:
        return r.results[0]

    return None


if __name__ == "__main__":
    ISBNs = [
            "9788324008605",
            "9788375154535",
            "9788389499561",
            "9788395159046",
            "9780486440620" ]
    res = []
    for i in ISBNs:
        r = getRes( i )
        if r:
            res.append(r)
