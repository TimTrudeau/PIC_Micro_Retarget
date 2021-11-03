
class ClassTarget:

    def parse(self, text):
        self.registerdict = {}
        state = 'START'
        nextstate = state
        for index in range(len(text)):
            line = text[index].split()

            state = nextstate
            if state == "START":
                if 'PIC' in text[index]:
                    self.targetname = line[1]
                elif 'Register:' in text[index]:
                    nextstate = "GETREG"

            elif state == "GETREG":
                reg_name = self.captureRegisterName(line)
                nextstate = "GETBITS"

            elif state == "GETBITS":
                try:
                    lstr = line[0].split('_')
                except IndexError:
                    continue
                if '* Bit Access Macros' in text[index]:
                    nextstate = "DONE"
                elif 'Register:' in text[index]:
                        nextstate = "GETREG"
                elif lstr[0].isalnum():
                    self.captureRegisterBits(line, reg_name)
                else:
                    nextstate = "GETBITS"


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
                raise Exception(f'Duplicate register name found')
            self.registerdict[reg_name] = [reg_addr, ]
            return reg_name
        except Exception as ex:
            raise ex
