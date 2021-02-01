r"""__  __                               _             __          __
   / /_/ /_  ___  ____ _____ _____ ___  (_)___  ____ _/ /_  ____  / /_
  / __/ __ \/ _ \/ __ `/ __ `/ __ `__ \/ / __ \/ __ `/ __ \/ __ \/ __/
 / /_/ / / /  __/ /_/ / /_/ / / / / / / / / / / /_/ / /_/ / /_/ / /_
 \__/_/ /_/\___/\__, /\__,_/_/ /_/ /_/_/_/ /_/\__, /_.___/\____/\__/
               /____/                        /____/
"""


# A class for the input grammar
class Grammar:
    # Init function for the class
    def __init__(self, P, SS, NT, T, Fi, Fo):
        # Initialize all the attributes
        self.productions = P
        self.startSymbol = SS
        self.NT = NT
        self.T = T
        self.first = Fi
        self.follow = Fo

    # A function to get first of all non terminals
    def getFirst(self):
        print(self.productions)
        for _ in self.NT:
            # Union of present value to the computed value
            self.first[_] |= self.__getFirst(_)

    # A private function to get the first of a given input
    def __getFirst(self, inp):
        # Initialize a temporary set
        temp1 = set()
        # If the input is 'epsilon'
        if inp == '' or inp == '~':
            # Add epsilon
            temp1 = {'~'}
        # If the input is a terminal
        elif inp in self.T:
            # Add the terminal
            temp1 = {inp}
        # If the input is a non terminals
        elif inp in self.NT:
            # Loop through all its productions
            for _ in self.productions[inp]:
                if _ == inp:
                    break
                # Get the first of each production
                temp2 = self.__getFirst(_)
                temp1 = temp1 | temp2
        # Else
        else:
            pos = 1
            # Get the first of the first inp
            temp2 = self.__getFirst(inp[0])
            # If there exist an epsilon in the first
            if '~' in temp2:
                # While there is an epsilon
                while '~' in temp2:
                    temp1 = temp1 | (temp2 - {'~'})
                    # if the next input is epsilon
                    if inp[pos:] == '':
                        temp1 = temp1 | {'~'}
                        break
                    # If the next input is a terminal
                    elif inp[pos:] in self.T:
                        temp1 = temp1 | {inp[pos:]}
                        break
                    # Get the first of the non terminal
                    temp2 = self.__getFirst(inp[pos:])
                    temp1 = temp1 | temp2 - {'~'}
                    # Increment the position of the pointer
                    pos += 1
            # If epsilon does not exist in the first
            else:
                temp1 = temp1 | temp2
        # Return the set
        return temp1

    # A function to get follow of all non terminals
    def getFollow(self):
        for _ in self.NT:
            # Union of present value to the computed value
            self.follow[_] |= self.__getFollow(_)

    # A private function to get the follow of a given input
    def __getFollow(self, inp):
        # Initialize an empty set
        temp1 = set()
        # If the input is a start symbol
        if inp == self.startSymbol:
            # Add '$' to it
            temp1 = temp1 | {'$'}
        # Loop through each production
        for i, j in self.productions.items():
            # Loop through each transition
            for x in j:
                # Loop through each character
                for _ in x:
                    # If the non terminal exists in RHS
                    if _ == inp:
                        # Get the following string
                        strF = x[x.index(inp) + 1:]
                        # If the following string is not empty
                        if strF != '':
                            # Get the first of it
                            temp2 = self.__getFirst(strF)
                            # If epsilon is not in the first
                            if '~' not in temp2:
                                temp1 = temp1 | temp2
                            # Else
                            else:
                                temp1 = temp1 | temp2 - {'~'}
                                # Get the follow of the non terminal in the LHS
                                temp1 = temp1 | self.__getFollow(i)
                        # If the string is empty
                        else:
                            if i != inp:
                                # Get the follow of the non terminal in the LHS
                                temp1 = temp1 | self.__getFollow(i)
                            else:
                                continue
        # Return the set
        return temp1
