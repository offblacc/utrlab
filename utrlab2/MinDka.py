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
        self.states_to_remove = None

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
        for key in sorted(self.transition_function_dict):
            if self.transition_function_dict.get(key) in self.states_to_remove:
                for par in sorted(self.merged_states):
                    if self.transition_function_dict[key] != par[1]: continue
                    self.transition_function_dict[key] = par[0]
        for key in sorted(self.transition_function_dict):
            if key[0] in self.states_to_remove:
                self.transition_function_dict.pop(key)

    def fill_dict(self):
        for pair in sorted(list(self.pairs)):
            self.pair_lists.update({pair: set()})

    def mark_trivially_nonequivalent(self):
        for st1 in sorted(list(self.states)):
            for st2 in sorted(list(self.states)):
                if st1 == st2: continue  # only different states pass this statement
                if (st1 in self.accept_states) != (st2 in self.accept_states):  # different acceptedness
                    self.marked_pairs.add(tuple(sorted([st1, st2])))
                else:
                    self.unmarked_pairs.add(tuple(sorted([st1, st2])))
        self.pairs = self.marked_pairs.union(self.unmarked_pairs)
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

        self.merged_states = self.pairs.difference(self.marked_pairs)
        for state in sorted(list(self.merged_states)):
            if sorted(state)[1] in self.states.copy(): self.states.remove(state[1])
        self.states_to_remove = [x[1] for x in self.merged_states]
        self.minimize_transition_function()

        for state in sorted(list(self.merged_states)):
            if self.start_state in state:
                self.start_state = state[0]

    def print_dka(self):
        print(*sorted(list(self.states)), sep=",")
        print(*sorted(list(self.symbols)), sep=",")
        print(*sorted(list(self.accept_states.intersection(self.states))), sep=",")
        print(self.start_state)
        for par in sorted(list(set(self.transition_function_dict.items()))): print(f"{par[0][0]},{par[0][1]}->{par[1]}")


def main():
    states = set(sys.stdin.readline().strip().split(","))
    symbols = set(sys.stdin.readline().strip().split(","))
    accept_states = set(sys.stdin.readline().strip().split(","))
    start_state = sys.stdin.readline().strip()
    transition_function = dict([(tuple((x.split("->")[0]).split(",")), x.split("->")[1].strip()) for x in sys.stdin.readlines()])
    dka = DKA(states, symbols, accept_states, start_state, transition_function)
    dka.minimize()
    dka.print_dka()


if __name__ == '__main__':
    main()
