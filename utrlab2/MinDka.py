import sys


class DKA:
    def __init__(self, dka_definition):
        self.states = dka_definition[0]
        self.symbols = dka_definition[1]
        self.accept_states = dka_definition[2]
        self.start_state = dka_definition[3]
        self.transition_function_dict = dka_definition[4]
        self.marked_pairs, self.pairs, self.pair_lists, self.merged_states = set(), set(), dict(), []

    # parses input, returns dka_parameters list
    @staticmethod
    def parse_input():
        dka_definition = []
        for _ in range(3):
            dka_definition.append(set(sys.stdin.readline().strip().split(",")))
        dka_definition.append(sys.stdin.readline().strip())
        dka_definition.append(dict([(
            tuple((x.split("->")[0]).split(",")),
            x.split("->")[1].strip())
            for x in sys.stdin.readlines()]
        ))  # key is tuple (state, symbol), value is string
        return dka_definition

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

    def mark_trivially_nonequivalent(self):
        unmarked_pairs = set()
        for st1 in self.states:
            for st2 in self.states:
                if st1 == st2: continue  # only different states pass this statement
                if (st1 in self.accept_states) != (st2 in self.accept_states):  # different acceptedness
                    self.marked_pairs.add(tuple(sorted([st1, st2])))
                else:
                    unmarked_pairs.add(tuple(sorted([st1, st2])))
        self.pairs = self.marked_pairs.union(unmarked_pairs)
        for pair in self.pairs:
            self.pair_lists.update({pair: []})
        self.fill_dict()

    # also adds the state whose list we're checking
    def get_new_markings_from_list(self, tuple_states):
        returning_set = set()
        returning_set.add(tuple_states)
        for pair_to_check in self.pair_lists[tuple_states]:
            returning_set = returning_set.union(self.get_new_markings_from_list(pair_to_check))
        return returning_set

    def minimize(self):
        self.discard_unreachable()
        self.mark_trivially_nonequivalent()
        for pair in self.pairs.difference(self.marked_pairs):
            for symbol in self.symbols:
                delta_pair = tuple(sorted([self.transition(pair[0], symbol), self.transition(pair[1], symbol)]))
                if delta_pair not in self.marked_pairs: continue
                if pair not in self.marked_pairs:
                    added_from_list = self.get_new_markings_from_list(pair)
                    self.marked_pairs = self.marked_pairs.union(added_from_list)
                else:
                    for symb2 in self.symbols:
                        if self.transition(pair[0], symb2) == self.transition(pair[1], symb2): continue
                        self.pair_lists[
                            tuple(sorted([self.transition(pair[0], symb2), self.transition(pair[1], symb2)]))].add(pair)
        self.merged_states = self.pairs.difference(self.marked_pairs)
        for state in self.merged_states:
            if state[1] in self.states.copy():
                self.states.remove(state[1])

        for state in self.merged_states:
            if self.start_state in state:
                self.start_state = state[0]

    def get_states(self):
        strprnt = ""
        for state in sorted(list(self.states)): strprnt += f"{state},"
        return strprnt[:-1]

    def print_dka(self):
        print(self.get_states())
        out = ""
        for symbol in sorted(list(self.symbols)):
            out += symbol + ","
        print(out[:-1])
        out = ""
        for state in sorted(list(self.accept_states.intersection(self.states))):
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
    dka = DKA(DKA.parse_input())
    dka.minimize()
    dka.print_dka()


if __name__ == '__main__':
    main()
