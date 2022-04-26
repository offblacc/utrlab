import sys


class DPA:
    def __init__(self, seq, states, in_chars, stack_chars, accept_states, start_state, start_stack_state, transitions):
        self.seq = seq
        self.states = states
        self.in_chars = in_chars
        self.stack_chars = stack_chars
        self.accept_states = accept_states
        self.curr_state = start_state
        self.curr_stack_state = start_stack_state
        self.transitions = transitions

    def run(self):
        i = 0
        print(f'{self.curr_state}#{self.curr_stack_state}', end='')
        while i < len(self.seq):
            char = self.seq[i]
            if tuple([self.curr_state, char, self.curr_stack_state[0]]) in self.transitions or tuple([self.curr_state, '$', self.curr_stack_state[0]]) in self.transitions:
                if tuple([self.curr_state, '$', self.curr_stack_state[0]]) in self.transitions: 
                    char, i = '$', i - 1
                new_state = self.transitions[tuple([self.curr_state, char, self.curr_stack_state[0]])][0]
                new_stack_state = self.transitions[tuple([self.curr_state, char, self.curr_stack_state[0]])][1] + self.curr_stack_state[1:]
                if new_stack_state[0] == '$' and len(new_stack_state) > 1: new_stack_state = new_stack_state[1:]
                self.curr_state, self.curr_stack_state = new_state, new_stack_state
                print(f'|{self.curr_state}#{self.curr_stack_state}', end='')
            else:
                print(f'|fail|0')
                return
            i += 1

        if self.curr_state in self.accept_states:
            print(f'|1')
            return

        search_epsilon = tuple([self.curr_state, '$', self.curr_stack_state[0]]) in self.transitions
        while search_epsilon:
            if tuple([self.curr_state, '$', self.curr_stack_state[0]]) in self.transitions:
                self.curr_state, self.curr_stack_state = self.transitions[tuple([self.curr_state, '$', self.curr_stack_state[0]])][0], self.transitions[tuple([self.curr_state, '$', self.curr_stack_state[0]])][1] + self.curr_stack_state[1:]
                if new_stack_state[0] == '$' and len(new_stack_state) != 1: new_stack_state = new_stack_state[1:]
                print(f'|{self.curr_state}#{self.curr_stack_state}', end='')
                search_epsilon = tuple([self.curr_state, '$', self.curr_stack_state[0]]) in self.transitions
            else: 
                search_epsilon = False
            
            if self.curr_state in self.accept_states:
                print('|1')
                return
        print('|0')


def main():
    seqs = [seq.split(',') for seq in sys.stdin.readline().strip().split('|')]
    args = [[]]
    for _ in range(4): args.append(set(sys.stdin.readline().strip().split(',')))
    for _ in range(2): args.append(sys.stdin.readline().strip())
    args.append(dict())
    for line in sys.stdin.readlines(): args[-1].update({tuple(line.strip().split('->')[0].split(',')): tuple(line.strip().split('->')[1].split(','))})
    for seq in seqs:
        args[0] = seq
        DPA(*args).run()


if __name__ == '__main__':
    main()
