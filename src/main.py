import os, sys
from parse_target import ClassTarget


def readfile(self, filename):
    content = None
    try:
        if not os.path.exists(filename):
            print(f'File {filename} does not exist.')
        else:
            with open(filename, mode='r') as f:
                content = f.read().splitlines()
    except Exception as ex:
        print(f'File {filename} failed to open.')
        raise ex
    return content


class Remapper:
    def __init__(self, file688=None, targetfile=None):
        self.file688 = file688
        self.targetfile = targetfile

    def doRemapping(self):
        self.f688 = Class688()
        self.ftarget = ClassTarget()
        self.f688data = readfile(self.file688)
        self.targetdata = readfile(self.targetfile)
        self.f688dict = self.f688.parse(self.f688data)
        self.targetdict = self.ftarget.parse(self.f688data)
        output = "this is a dummy output"
        return output


class Class688:
    def parse(self, text):
        self.registerdict = {}
        state = 'START'
        nextstate = state
        for index in range(len(text)):
            line = text[index].split()

            state = nextstate
            if state == "START":
                if 'Register Files' in text[index]:
                    nextstate = "GETREG"

            elif state == "GETREG":
                if 'Bits' in text[index]:
                    reg_name = line[1]
                    nextstate = "GETBITS"
                elif line == []:
                    nextstate = "GETREG"
                else:
                    self.captureRegisterName(line)

            elif state == "GETBITS":
                if 'Bits' in line:
                    reg_name = line[1]
                    nextstate = "GETBITS"
                elif 'RAM' in text[index]:
                    nextstate = "DONE"
                elif line == [] or ';' in text[index]:
                    nextstate = "GETBITS"
                else:
                    self.captureRegisterBits(line, reg_name)

            elif state == "DONE":
                return self.registerdict

    def captureRegisterBits(self, lineList, regName):
        bit_name = lineList[0]
        bit_value = lineList[2]
        self.registerdict[regName].append(bit_name)
        self.registerdict[regName].append(bit_value)

    def captureRegisterName(self, lineList):
        try:
            reg_name = lineList[0]
            reg_addr = lineList[2]
            if reg_name in self.registerdict.keys():
                # TODO test this exception handling
                raise Exception(f'Duplicate register name found')
            self.registerdict[reg_name] = [reg_addr, ]
            return
        except Exception as ex:
            raise ex

if __name__ == '__main__':
    args = sys.argv[1:]
    try:
        dump = args[2]
    except Exception:
        dump = "dump.txt"
    mapper = Remapper(args[0], args[1])
    outfile = mapper.doRemapping()
    with open(dump, mode='w') as f:
        f.write(outfile)
