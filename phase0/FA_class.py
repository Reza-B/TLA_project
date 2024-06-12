import json


class State:
    __counter = 0

    def __init__(self, id: None) -> None:
        if id is None:
            self.id = State._get_next_id()
        else:
            self.id = id
        self.transitions: dict[str, 'State'] = {}

    def add_transition(self, symbol: str, state: 'State') -> None:
        self.transitions[symbol] = state

    @classmethod
    def _get_next_id(cls) -> int:
        current_id = cls.__counter
        cls.__counter += 1
        return current_id


class DFA:
    def __init__(self) -> None:
        self.init_state = None
        self.states: list['State'] = []
        self.alphabet: list['str'] = []
        self.final_states: list['State'] = []

    @staticmethod
    def deserialize_json(json_str: str) -> 'DFA':
        fa = DFA()
        json_fa = json.loads(json_str)

        fa.alphabet = json_fa["alphabet"]

        for state_str in json_fa["states"]:
            fa.add_state(int(state_str[2:]))

        fa.init_state = fa.get_state_by_id(json_fa["initial_state"][2:])

        for final_str in json_fa["final_states"]:
            fa.add_final_state(fa.get_state_by_id(final_str[2:]))

        for state_str in json_fa["states"]:
            for symbol in fa.alphabet:
                fa.add_transition(fa.get_state_by_id(state_str[2:]), fa.get_state_by_id(json_fa[state_str][symbol][2:]),
                                  symbol)

        return fa

    def serialize_json(self) -> str:
        fa = {
            "states": list(map(lambda s: f"q_{s.id}", self.states)),
            "initial_state": f"q_{self.init_state.id}",
            "final_states": list(map(lambda s: f"q_{s.id}", self.final_states)),
            "alphabet": self.alphabet
        }

        for state in self.states:
            fa[f"q_{state.id}"] = {}
            for symbol in self.alphabet:
                fa[f"q_{state.id}"][symbol] = f"q_{state.transitions[symbol].id}"

        return json.dumps(fa)

    def add_state(self, id: int | None = None) -> State:
        new_state = State(id)
        self.states.append(new_state)
        return new_state

    def add_transition(self, from_state: State, to_state: State, input_symbol: str) -> None:
        from_state.add_transition(input_symbol, to_state)

    def assign_initial_state(self, state: State) -> None:
        self.init_state = state

    def add_final_state(self, state: State) -> None:
        self.final_states.append(state)

    def get_state_by_id(self, id) -> State | None:
        for state in self.states:
            if state.id == int(id):
                return state
        return None

    def is_final(self, state: State) -> bool:
        return state in self.final_states


class NFAState:
    __counter = 0

    def __init__(self, id: None = None) -> None:
        if id is None:
            self.id = NFAState._get_next_id()
        else:
            self.id = id
        self.transitions: dict[str, set['NFAState']] = {}

    def add_transition(self, symbol: str, state: 'NFAState') -> None:
        if symbol in self.transitions:
            self.transitions[symbol].add(state)
        else:
            self.transitions[symbol] = {state}

    @classmethod
    def _get_next_id(cls) -> int:
        current_id = cls.__counter
        cls.__counter += 1
        return current_id


class NFA:
    def __init__(self) -> None:
        self.init_state = None
        self.states: list['NFAState'] = []
        self.final_states: list['NFAState'] = []

    @staticmethod
    def convert_DFA_instanse_to_NFA_instanse(dfa_machine: 'DFA') -> 'NFA':
        nfa = NFA()
        # Convert DFA states to NFA states
        for state in dfa_machine.states:
            nfa_state = NFAState(id=state.id)
            if state == dfa_machine.init_state:
                nfa.assign_initial_state(nfa_state)
            if dfa_machine.is_final(state):
                nfa.add_final_state(nfa_state)
            nfa.add_state(nfa_state)

        # Convert DFA transitions to NFA transitions
        for state in dfa_machine.states:
            for symbol, next_state in state.transitions.items():
                nfa.add_transition(
                    nfa.get_state_by_id(state.id),
                    nfa.get_state_by_id(next_state.id),
                    symbol
                )

        return nfa

    @staticmethod
    def union(machine1: 'NFA', machine2: 'NFA') -> 'NFA':
        union_nfa = NFA()
        # Create a new initial state and connect it to the initial states of machine1 and machine2
        new_initial_state = NFAState()
        union_nfa.assign_initial_state(new_initial_state)
        union_nfa.add_state(new_initial_state)
        union_nfa.add_transition(new_initial_state, machine1.init_state, 'ε')
        union_nfa.add_transition(new_initial_state, machine2.init_state, 'ε')

        # Merge the states and transitions of machine1 and machine2 into the new NFA
        union_nfa.merge_nfa(machine1)
        union_nfa.merge_nfa(machine2)

        return union_nfa

    @staticmethod
    def concat(machine1: 'NFA', machine2: 'NFA') -> 'NFA':
        # Connect final states of machine1 to initial state of machine2
        for final_state in machine1.final_states:
            machine2.add_transition(final_state, machine2.init_state, 'ε')
            machine2.final_states.remove(final_state)

        # Merge the states and transitions of machine2 into machine1
        machine1.merge_nfa(machine2)
        return machine1

    @staticmethod
    def star(machine: 'NFA') -> 'NFA':
        # Create a new initial state and connect it to the initial state of the machine
        new_initial_state = NFAState()
        machine.assign_initial_state(new_initial_state)
        machine.add_state(new_initial_state)
        machine.add_transition(new_initial_state, machine.init_state, 'ε')

        # Connect final states to initial state
        for final_state in machine.final_states:
            machine.add_transition(final_state, machine.init_state, 'ε')

        return machine

    def merge_nfa(self, other_nfa: 'NFA') -> None:
        for state in other_nfa.states:
            self.add_state(state)
        for final_state in other_nfa.final_states:
            self.add_final_state(final_state)
        for state in other_nfa.states:
            for symbol, transitions in state.transitions.items():
                for next_state in transitions:
                    self.add_transition(state, next_state, symbol)

    def serialize_to_json(self) -> str:
        nfa = {
            "states": list(map(lambda s: f"q_{s.id}", self.states)),
            "initial_state": f"q_{self.init_state.id}",
            "final_states": list(map(lambda s: f"q_{s.id}", self.final_states)),
        }

        for state in self.states:
            nfa[f"q_{state.id}"] = {}
            for symbol, next_states in state.transitions.items():
                nfa[f"q_{state.id}"][symbol] = list(map(lambda s: f"q_{s.id}", next_states))

        return json.dumps(nfa)
