from graphviz import Digraph
import pandas

from automata.fa.nfa import NFA
from automata.fa.dfa import DFA

nfa = NFA(
    states={'S0', 'S1', 'S2', 'S3'},
    input_symbols={'a', 'b'},
    transitions={
        'S0': {'a': {'S1'}},
        'S1': {'': {'S2'}},
        'S2': {'b': {'S3'}, 'a': {'S1', 'S2'}},
        'S3': {'a': {'S2'}},
    },
    initial_state='S0',
    final_states={'S3', 'S2'}

)


def NFA_to_graph(automata, filename):
    f = Digraph('finite_state_machine', filename=filename)
    f.attr(rankdir='LR', size='15,5')
    f.attr('node', shape='rarrow', color='Green')
    f.node("Debut")
    f.attr('node', shape='circle', color='black')
    f.node(automata.initial_state)
    f.edge("Debut", automata.initial_state)
    f.edge("Debut", automata.initial_state)
    for state in automata.states:
        if (state != automata.initial_state) and (state not in automata.final_states):
            f.attr('node', shape='circle', color='black')
            f.node(state)
    for state in automata.final_states:
        f.attr('node', shape='doublecircle', color='Red')
        f.node(state)
    for key in automata.transitions.keys():
        transition = automata.transitions[key]
        for alphabet in transition:
            for sub_trans in transition[alphabet]:
                if alphabet == "":
                    f.edge(key, sub_trans, "Ɛ")
                else:
                    f.edge(key, sub_trans, alphabet)

    f.view()
def miror(automata):
    automat = automata.copy()
    if len(automat.final_states) > 1:
        automat.states.add('{}')
        for state in automat.final_states:
            transition = automat.transitions[state]
            if "" in transition.keys():
                list = transition[""]
                list.add('{}')
            else:
                transition.update({'': {'{}'}})
            automat.transitions.update({state: transition})
        automat.final_states.clear()
        automat.final_states.add('{}')
    swap = automat.final_states.pop()
    automat.final_states.add(automat.initial_state)
    automat.initial_state = swap
    sub_transition = {}
    transitions = {}
    for state in sorted(automat.states):
        sub_transition = {}
        for key in automat.transitions.keys():
            transition = automat.transitions[key]
            list = set()
            for alphabet in transition:
                for sub_trans in transition[alphabet]:
                    if state == sub_trans:
                        if alphabet in sub_transition.keys():
                            list = sub_transition.get(alphabet)
                        list.add(key)
                        sub_transition.update({alphabet: list})
        transitions.update({state: sub_transition})
    automat.transitions = transitions
    return automat
def compliment(automata):
    automat = DFA.from_nfa(automata)
    for state in automat.states:
        if state in automata.final_states:
            automat.final_states.remove(state)
        elif state not in automat.final_states:
            automat.final_states.add(state)
    return automat
def DFA_to_graph(automata, filename):
    f = Digraph('finite_state_machine', filename=filename)
    f.attr(rankdir='LR', size='15,5')
    f.attr('node', shape='rarrow', color='Green')
    f.node("Debut")
    f.attr('node', shape='circle', color='black')
    f.node(automata.initial_state)
    f.edge("Debut", automata.initial_state)
    f.edge("Debut", automata.initial_state)
    for state in automata.states:
        if (state != automata.initial_state) and (state not in automata.final_states):
            f.attr('node', shape='circle', color='black')
            f.node(state)
    for state in automata.final_states:
        f.attr('node', shape='doublecircle', color='Red')
        f.node(state)

    for key in automata.transitions.keys():
        transition = automata.transitions[key]
        for alphabet in transition:
            f.edge(key, transition[alphabet], alphabet)

    f.view()



NFA_to_graph(nfa,"base_automata")
NFA_to_graph(miror(nfa),'miror_automata')
DFA_to_graph(DFA.from_nfa(nfa),'determinste_automata')
DFA_to_graph(compliment(nfa),"compliment_automata")










