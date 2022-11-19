valid = ["🟧", "⬛", "🟦", "🟨","🟩","⬜"]
def WordleToRaw(wordle:str):
    """
    Convert a Wordle string (the copy paste) to a Raw Wordle Point List (RWPL)

    .. versionadded:: 1.0

    Returns
    -------
    list[list[int]]:
        A RWPL, stored as one list per guess, with each item in the guess being a point (0: none, 1: wrong pos, 2: correct)
    """
    cout: list[list[int]] = []
    val = 0
    for d in wordle.split("\n"):
        cout.append([])
        for i in d:
            if not i in valid:
                continue
            if i == valid[0] or i == valid[4]:
                cout[val].append(2)
            if i == valid[2] or i == valid[3]:
                cout[val].append(1)
            if i == valid[1] or i == valid[5]:
                cout[val].append(0)
        val += 1
    return cleanup(cout)
def cleanup(li:list[list[int]]):
    #remove empty items in the list
    for m in range(0,10):
        for i in li:
            if not i:
                li.remove(i)
    return li
def CalculateScore(RWPL: list[list[int]]):
    """
    Convert a Raw Wordle Point List (RWPL) to a Modified Raw Wordle Point List (MRWPL)

    .. versionadded:: 1.0

    Returns
    -------
    list[list[int]]:
        A MRWPL, based of a RWPL; just with the values replaced to the score
    """
    #for each square
    cout: list[list[int]] = []
    gyrados = 6
    for listDex, listItem in enumerate(RWPL):
        gyrados -= 1
        cout.append([])
        for scoreItem in listItem:
            cout[listDex].append(scoreItem * (6 - listDex))
    cout.append([gyrados*7])
    return cout
def LineFix(MRWPL: list[list[int]], Wordle:str):
    """
    Convert a Modified Raw Wordle Point List (MRWPL) and a Wordle to a formatted end string

    .. versionadded:: 1.0

    Returns
    -------
    str:
        A neat string; with the guesses on one side and score at the end.
    """
    mpt = "🟧"
    Wordle = Wordle.split("\n")
    Wordle: list[str] = Wordle
    cout = ""
    deldex = []
    egg: list[int] = []
    for dex, i in enumerate(Wordle):
        marked = True
        for txt in i:
            if txt in valid:
                marked = False
                if txt == "🟩":
                    mpt = "🟩"
                elif txt == "🟧":
                    mpt = "🟧"
        if marked:
            deldex.append(dex)
    for fo, i in enumerate(deldex):
        Wordle.remove(Wordle[i-fo])
    Wordle.append(mpt*5)
    Wordle.append(mpt*5)
    Wordle.append(mpt*5)
    Wordle.append(mpt*5)
    for p in MRWPL:
        egg.append([sum(p)])
    for enum, i in enumerate(egg):
        cout += Wordle[enum]
        cout += "  "
        cout += str(i[0])
        cout += "\n"
    cout += "Final score "
    cout += str(cool(MRWPL))
    return cout
def cool(cnvd: list[list[int]]):
    lite = 0
    for i in cnvd:
        for m in i:
            lite += m
    return lite
def Main(wordle:str):
    Converted = WordleToRaw(wordle)
    foo = CalculateScore(Converted)
    return LineFix(foo, wordle)
if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument('--file', type=str, default=False,
                   help='Path to a file with a wordle; UTF-16 LE only!')
    p.add_argument('--interactive', type=bool, default=True,
                   help='Enable interactive mode')
    args = p.parse_args()
    if args.file:
        with open(args.file) as f:
            print(Main(f.read()))
    if args.interactive:
        Exited = False
        print("Welcome to Wordle Scorer")
        while not Exited:
            print("\n"*3)
            print("Commands:\nr {file}: Read a file and print it's score (UTF-16 LE ONLY!). \np: Paste in a wordle\ne: Exit")
            command = input(">> ")
            print("\n"*2)
            vl = ["r", "p", "e"]
            if command.split(" ")[0] in vl:
                if command.split(" ")[0] == vl[0]:
                    try:
                        with open(command.split(" ")[1].strip(), "rb") as f:
                            print(Main(f.read().decode("UTF-16 LE")))
                    except:
                        print("File is not there/not encoded in UTF-16 LE")
                if command.split(" ")[0] == vl[1]:
                    print("Paste in the wordle; it might look corrupted, but it works! (type 'end' to end input mode):")
                    ap = ""
                    c = ""
                    while ap != "end":
                        ap = input(">")
                        if ap != "end":
                            c += ap
                            c += "\n"
                    print(Main(c))
                if command.split(" ")[0] == vl[2]:
                    Exited = True
            else:
                print("Invalid Command")
                    
