import sys


class DKA:
    def __init__(self, states, symbols, accept_states, start_state, transition_function):
        self.states = states
        self.symbols = symbols
        self.accept_states = accept_states
        self.start_state = start_state
        self.transition_function_dict = transition_function
        self.marked_pairs, self.unmarked_pairs, self.pairs = set(), set(), set()
        self.pair_lists = dict()
        self.merged_states = []

    def transition(self, state, symbol):
        return self.transition_function_dict[tuple([state, symbol])]

    def discard_unreachable(self):
        reachable_states = {self.start_state}
        added_states = True
        while added_states:
            added_states = False
            for state in reachable_states.copy():
                for symbol in self.symbols:  # inverted the logic to avoid seemingly endless identations
                    if tuple([state, symbol]) not in self.transition_function_dict: continue
                    if self.transition_function_dict[tuple([state, symbol])] in reachable_states: continue
                    reachable_states.add(self.transition_function_dict[tuple([state, symbol])])
                    added_states = True

        for unreachable_state in self.states.difference(reachable_states):
            self.states.remove(unreachable_state)
            for key in self.transition_function_dict.copy().keys():
                if unreachable_state in key:
                    self.transition_function_dict.pop(key)

    def fill_dict(self):
        for pair in self.pairs:
            self.pair_lists.update({pair: set()})

    def update_all_pairs(self):
        self.pairs = self.marked_pairs.union(self.unmarked_pairs)
        for pair in self.pairs:
            self.pair_lists.update({pair: []})
        self.fill_dict()

    def mark_pairs_initial(self):
        for st1 in self.states:
            for st2 in self.states:
                if st1 == st2: continue  # only different states pass this statement
                if (st1 in self.accept_states) != (st2 in self.accept_states):  # different acceptedness
                    self.marked_pairs.add(tuple(sorted([st1, st2])))
                else:
                    self.unmarked_pairs.add(tuple(sorted([st1, st2])))
        self.update_all_pairs()

    # also adds the state whose list we're checking
    def get_new_markings_from_list(self, tuple_states):
        returning_set = set()
        returning_set.add(tuple_states)
        for pair_to_check in self.pair_lists[tuple_states]:
            returning_set = returning_set.union(self.get_new_markings_from_list(pair_to_check))
        return returning_set

    def marking_pairs(self):
        self.mark_pairs_initial()
        for pair in self.unmarked_pairs.copy():
            for symbol in self.symbols:
                if tuple(sorted([self.transition(pair[0], symbol),
                                 self.transition(pair[1], symbol)])) in self.marked_pairs and pair not in self.marked_pairs:
                    added_from_list = self.get_new_markings_from_list(pair)
                    self.marked_pairs = self.marked_pairs.union(added_from_list)
                else:
                    for symb2 in self.symbols:
                        if self.transition(pair[0], symb2) == self.transition(pair[1], symb2): continue
                        self.pair_lists[
                            tuple(sorted([self.transition(pair[0], symb2), self.transition(pair[1], symb2)]))].add(pair)

        states_out = self.states
        self.merged_states = self.pairs.difference(self.marked_pairs)
        for state in self.merged_states:
            if state[1] in states_out:
                states_out.remove(state[1])

        for state in self.merged_states:
            if self.start_state in state:
                self.start_state = state[0]

    def get_states(self):
        strprnt = ""
        for state in self.states: strprnt += f"{state},"
        return strprnt[:-1]

    def print_output(self):
        print(self.get_states())
        out = ""
        for symbol in self.symbols:
            out += symbol + ","
        print(out[:-1])
        out = ""
        for state in self.accept_states.intersection(self.states):
            out += state + ","
        print(out[:-1])
        print(self.start_state)
        transition_final = ""
        for elem in self.transition_function_dict.items():
            transition_final += elem[0][0] + "," + elem[0][1] + "->" + elem[1] + " "
        transition_final.strip()
        for swap in self.merged_states:
            transition_final = transition_final.replace(swap[1], swap[0])
        transition_final = sorted(list(set(transition_final.strip().split(" "))))
        for trans in transition_final:
            print(trans)


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
    dka.discard_unreachable()
    dka.mark_pairs_initial()
    dka.marking_pairs()
    dka.print_output()


if __name__ == '__main__':
    main()
