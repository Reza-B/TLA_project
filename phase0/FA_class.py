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
        ...

    def add_transition(self, from_state: State, to_state: State, input_symbol: str) -> None:
        ...

    def assign_initial_state(self, state: State) -> None:
        ...

    def add_final_state(self, state: State) -> None:
        ...

    def get_state_by_id(self, id) -> State | None:
        ...

    def is_final(self, state: State) -> bool:
        ...



class NFAState:
    ...


class NFA:
    def __init__(self) -> None:
        ...

    @staticmethod
    def convert_DFA_instanse_to_NFA_instanse(dfa_machine: 'DFA') -> 'NFA':
        ...
    
    @staticmethod
    def union(machine1: 'NFA', machine2: 'NFA') -> 'NFA':
        ...
    
    @staticmethod
    def concat(machine1: 'NFA', machine2: 'NFA') -> 'NFA':
        ...
    
    @staticmethod
    def star(machine: 'NFA') -> 'NFA':
        ...

    def serialize_to_json(self) -> str:
        ...
