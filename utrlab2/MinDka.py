import sys


class DKA:
    def __init__(self, dka_definition):
        self.states = dka_definition[0]
        self.symbols = dka_definition[1]
        self.accept_states = dka_definition[2]
        self.start_state = dka_definition[3]
        self.transition_function_dict = dka_definition[4]
        self.marked_pairs, self.pairs, self.pair_lists, self.merged_states = set(), set(), dict(), set()
        self.states_to_remove = set()

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
            for state in sorted(list(reachable_states.copy())):
                for symbol in sorted(list(self.symbols)):  # inverted the logic to avoid seemingly endless identations
                    if tuple([state, symbol]) not in self.transition_function_dict: continue
                    if self.transition_function_dict[tuple([state, symbol])] in reachable_states: continue
                    reachable_states.add(self.transition_function_dict[tuple([state, symbol])])
                    added_states = True

        for unreachable_state in sorted(list(self.states.difference(reachable_states))):
            self.states.remove(unreachable_state)
            for key in self.transition_function_dict.copy().keys():
                if unreachable_state in key:
                    self.transition_function_dict.pop(key)

    def minimize_transition_function(self):
        # modify values
        for key in sorted(self.transition_function_dict):
            if self.transition_function_dict.get(key) in self.states_to_remove:
                for par in sorted(self.merged_states):
                    if self.transition_function_dict[key] != par[1]: continue
                    self.transition_function_dict[key] = par[0]
                    # print(f"par[0]: {par[0]} i par1 {par[1]}")  # TODO zasš svi idu u q0
        for key in sorted(self.transition_function_dict):
            if key[0] in self.states_to_remove:
                self.transition_function_dict.pop(key)

    def fill_dict(self):
        for pair in sorted(list(self.pairs)):
            self.pair_lists.update({pair: set()})

    def mark_trivially_nonequivalent(self):
        unmarked_pairs = set()
        liststanja = sorted(list(self.states))
        for st1 in liststanja:
            for st2 in liststanja:
                if st1 == st2: continue  # only different states pass this statement
                if (st1 in self.accept_states) != (st2 in self.accept_states):  # different acceptedness
                    self.marked_pairs.add(tuple(sorted([st1, st2])))
                else:
                    unmarked_pairs.add(tuple(sorted([st1, st2])))
        self.pairs = self.marked_pairs.union(unmarked_pairs)
        for pair in sorted(list(self.pairs)):
            self.pair_lists.update({pair: []})
        self.fill_dict()

    # also adds the state whose list we're checking
    def get_new_markings_from_list(self, tuple_states):
        returning_set = set()
        returning_set.add(tuple_states)
        for pair_to_check in sorted(list(self.pair_lists[tuple_states])):
            returning_set = returning_set.union(self.get_new_markings_from_list(pair_to_check))
        return returning_set
    
    # TODO za auditorne.txt izgubis q1, iako bi trebao biti u outputu -> fixed
    # TODO zasto nisam oznacio q0q1? -> fixed
    def minimize(self):
        self.discard_unreachable()
        self.mark_trivially_nonequivalent()
        for pair in sorted(list(self.pairs.difference(self.marked_pairs))):
            for symbol in sorted(list(self.symbols)):
                delta_pair = tuple(sorted([self.transition(pair[0], symbol), self.transition(pair[1], symbol)]))
                if delta_pair in self.marked_pairs:
                    added_from_list = self.get_new_markings_from_list(pair)
                    self.marked_pairs = self.marked_pairs.union(added_from_list)
                else:
                    for symb2 in sorted(list(self.symbols)):
                        if self.transition(pair[0], symb2) == self.transition(pair[1], symb2): continue
                        if tuple(sorted([self.transition(pair[0], symb2), self.transition(pair[1], symb2)])) != pair:
                            self.pair_lists[tuple(sorted([self.transition(pair[0], symb2), self.transition(pair[1], symb2)]))].add(pair)
        self.merged_states = self.pairs.difference(self.marked_pairs)  # TODO bug origin, for ham_input should have only q3q4, q3q5, q3q6, instead have almost everything w q0... -> fixed
        for state in sorted(list(self.merged_states)):                 # TODO or is it back in marking states ? -> fixed
            if sorted(state)[1] in self.states.copy():
                self.states.remove(state[1])
        self.states_to_remove = [x[1] for x in self.merged_states]
        self.minimize_transition_function()

        for state in sorted(list(self.merged_states)):
            if self.start_state in state:
                self.start_state = state[0]

    def get_states(self):
        strprnt = ""
        for state in sorted(list(self.states)): strprnt += f"{state},"
        return strprnt[:-1]

    def print_dka(self):
        print(self.get_states())
        print(*sorted(list(self.symbols)), sep=",")
        print(*sorted(list(self.accept_states.intersection(self.states))), sep=",")
        print(self.start_state)
        for par in sorted(list(set(self.transition_function_dict.items()))):
            print(f"{par[0][0]},{par[0][1]}->{par[1]}")


def main():
    dka = DKA(DKA.parse_input())
    dka.minimize()
    dka.print_dka()


if __name__ == '__main__':
    main()
