import sys


class DKA:
    def __init__(self, states, symbols, accept_states, start_state, transition_function):
        self.states = states
        self.symbols = symbols
        self.accept_states = accept_states
        self.start_state = start_state
        self.transition_function = transition_function
        self.marked_pairs, self.unmarked_pairs = set(), set()

    def discard_unreachable(self):
        reachable_states = {self.start_state}
        added_states = True
        while added_states:
            added_states = False
            for state in reachable_states.copy():
                for symbol in self.symbols:  # inverted the logic to avoid seemingly endless identations
                    if tuple([state, symbol]) not in self.transition_function: continue
                    if self.transition_function[tuple([state, symbol])] in reachable_states: continue
                    reachable_states.add(self.transition_function[tuple([state, symbol])])
                    added_states = True

        for unreachable_state in self.states.difference(reachable_states):
            self.states.remove(unreachable_state)

    def mark_pairs(self):
        for st1 in self.states:
            for st2 in self.states:
                if st1 == st2: continue  # only different states pass this statement
                if (st1 in self.accept_states) != (st2 in self.accept_states):  # different acceptedness
                    self.marked_pairs.add(tuple(sorted([st1, st2])))
                else:
                    self.unmarked_pairs.add(tuple(sorted([st1, st2])))

    # def

    def print_states(self):
        strprnt = "Stanja: "
        for state in self.states:
            strprnt += f"{state}, "
        strprnt = strprnt[:-2]
        print(strprnt)


def main():
    states = set(sys.stdin.readline().strip().split(","))
    symbols = set(sys.stdin.readline().strip().split(","))
    accept_states = set(sys.stdin.readline().strip().split(","))
    start_state = sys.stdin.readline().strip()
    transition_function = dict([(
        tuple((x.split("->")[0]).split(",")),
        x.split("->")[1].strip())
        for x in sys.stdin.readlines()]
    )
    dka = DKA(states, symbols, accept_states, start_state, transition_function)
    print("Prije discardanja unreachable stanja", end=" ")

    dka.print_states()
    dka.discard_unreachable()

    print("Poslije discardanja unreachable stanja", end=" ")
    dka.print_states()
    dka.mark_pairs()


if __name__ == '__main__':
    main()
