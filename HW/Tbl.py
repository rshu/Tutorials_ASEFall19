import re, sys
from Num import Num


class THE:
    sep = ","
    num = "$"
    less = "<"
    more = ">"
    skip = "?"
    doomed = r'([\n\t\r ]|#.*)'


class Mine:
    oid = 0

    def identify(self):
        Mine.oid += 1
        self.oid = Mine.oid
        return self.oid

    def __repr__(i):
        pairs = sorted([(k, v) for k, v in i.__dict__.items()
                        if k[0] != "_"])
        pre = i.__class__.__name__ + '{'
        q = lambda z: "'%s'" % z if isinstance(z, str) else str(z)
        return pre + ", ".join(['%s=%s' % (k, q(v))
                                for k, v in pairs]) + '}'


class Tbl(Mine):
    listOfRead = []  # processed output from read
    listOfRow = []  # list of row objects
    listOfCol = []  # list of col object

    def __init__(self):
        self.identify()  # oid implementation need improvement

    def read(self, file):
        for n, cell in enumerate(cells(cols(rows(string(file))))):
            print(cell)
            self.listOfRead.append(cell)  # store all processed output
            if n == 0:  # check init title list is empty
                self.listOfCol = [Col(i, t) for i, t in enumerate(cell)]
            else:
                self.listOfRow += [Row(cell, [], 0)]  # each row is a Row object

    def dump(self):
        # [print(a) for a in self.listOfRead]
        # [print(c) for c in self.listOfCol]
        # [print(r) for r in self.listOfRow]

        print("")
        print("t.cols")

        for i, element in enumerate(self.listOfCol):

            numInstance = Num()

            for _, item in enumerate(self.listOfRead[1:len(self.listOfRead)]):
                # print(item[element.pos])
                if item[element.pos] == THE.skip:
                    numInstance.__add__(0)  # use 0 for ? in hw2
                else:
                    numInstance.__add__(item[element.pos])

            print("| ", i + 1)
            print("| | add:", "Num1")
            print("| | col:", i + 1)
            print("| | hi:", numInstance.hi)
            print("| | lo:", numInstance.lo)
            print("| | m2:", "{:.3f}".format(numInstance.m2))
            print("| | mu:", "{:.3f}".format(numInstance.expect()))
            print("| | n:", len(self.listOfRead))
            print("| | oid:", element.oid)
            print("| | sd:", "{:.3f}".format(numInstance.delta()))
            print("| | txt:", element.txt)

        print("t.oid:", self.oid)

        print("t.rows:", )
        for i, element in enumerate(self.listOfRow):
            row = element.cells

            print("| ", i + 1)
            print("| | cells")
            for j in range(len(row)):
                print("| | | ", j + 1, ":", row[j])
            print("| | ", "cooked")
            print("| | dom:", element.dom)
            print("| | oid:", element.oid)


class Col(Mine):
    def __init__(self, pos=0, txt=None):
        self.identify()
        self.pos = pos
        self.txt = txt


class Row(Mine):
    def __init__(self, cells=[], cooked=[], dom=0):
        self.identify()
        self.cells = cells
        self.cooked = cooked
        self.dom = dom


def string(s):
    """read lines from a string"""
    for line in s.splitlines():
        yield line


def rows(src):
    """convert lines into lists, killing whitespace
    and comments. skip over lines of the wrong size"""
    linesize = None
    for n, line in enumerate(src):
        line = re.sub(THE.doomed, '', line.strip())
        if line:
            line = line.split(THE.sep)  # breakup a string and add the data to a string array
            if linesize is None:
                linesize = len(line)
            if len(line) == linesize:
                yield line
            else:
                print("E> skipping line %s" % n, file=sys.stderr)  # To print to STDERR


def cols(src):
    """skip columns whose name contains '?'"""
    usedCol = None
    for cells in src:
        # usedCol = usedCol or [n for n, cell in enumerate(cells) if not THE.skip in cell]
        if usedCol is None:
            usedCol = [n for n, cell in enumerate(cells) if not THE.skip in cell]
        yield [cells[n] for n in usedCol]


def cells(src):
    """convert strings into their right types"""
    one = next(src)
    fs = [None] * len(one)  # [None, None, None, None]
    yield one  # the first line

    def ready(n, cell):
        if cell == THE.skip:
            return cell  # skip over '?'
        fs[n] = fs[n] or prep(one[n])  # ensure column 'n' compiles
        return fs[n](cell)  # compile column 'n'

    for _, cells in enumerate(src):
        # print("cells:", cells)
        yield [ready(n, cell) for n, cell in enumerate(cells)]


def prep(x):
    """return something that can compile strings"""

    def num(z):
        f = float(z)
        i = int(f)
        return i if i == f else f

    # --------------------------------------------------------
    for c in [THE.num, THE.less, THE.more]:
        if c in x:
            return num


def main():
    file = """
    $cloudCover, $temp, ?$humid, <wind,  $playHours
    100,        68,    80,    0,    3   # comments
    0,          85,    85,    0,    0

    0,          80,    90,    10,   0
    60,         83,    86,    0,    4
    100,        70,    96,    0,    3
    100,        65,    70,    20,   0
    70,         64,    65,    15,   5
    0,          72,    95,    0,    0
    0,          69,    70,    0,    4
    ?,          75,    80,    0,    ?
    0,          75,    70,    18,   4
    60,         72,
    40,         81,    75,    0,    2
    100,        71,    91,    15,   0
    """

    tbl = Tbl()
    tbl.read(file)
    tbl.dump()

    file2 = """
    outlook, ?$temp,  <humid, wind, !play
    rainy, 68, 80, FALSE, yes # comments
    sunny, 85, 85,  FALSE, no
    sunny, 80, 90, TRUE, no
    overcast, 83, 86, FALSE, yes
    rainy, 70, 96, FALSE, yes
    rainy, 65, 70, TRUE, no
    overcast, 64, 65, TRUE, yes
    sunny, 72, 95, FALSE, no
    sunny, 69, 70, FALSE, yes
    rainy, 75, 80, FALSE, yes
    sunny, 75, 70, TRUE, yes
    overcast, 72, 90, TRUE, yes
    overcast, 81, 75, FALSE, yes
    rainy, 71, 91, TRUE, no
    """


if __name__ == "__main__":
    main()
