#!/usr/bin/env python
# coding: utf-8

# In[4]:


from graphviz import Digraph
from automata.fa.nfa import NFA
from automata.fa.dfa import DFA
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors

import wand


# In[5]:



def NFA_to_graph(automata, filename):
    f = Digraph('finite_state_machine', filename=filename,format="png")
    f.attr(rankdir='LR', size='15.5')
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
    return f 
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
    automat = DFA.from_nfa(automata).minify()
    for state in automat.states:
        if state in automata.final_states:
            automat.final_states.remove(state)
        elif state not in automat.final_states:
            automat.final_states.add(state)
    return automat
def DFA_to_graph(automata, filename):
    f = Digraph('finite_state_machine', filename=filename, format="png")
    f.attr(rankdir='LR', size='15.5')
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
    return f


print("Faites introduire votre automate :")


# In[6]:


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


# In[7]:


NFA_to_graph(nfa,"Automate_de_base")
print("L'automate de base :")




# In[8]:


NFA_to_graph(miror(nfa),'Automate_miroir')
print("L'automate miroir :")


# In[9]:


DFA_to_graph(DFA.from_nfa(nfa),'Automate_deterministe')
print("L'automate deterministe :")

comp = DFA.from_nfa(nfa)

for transition in comp.transitions.keys():
    print(transition)



# In[7]:


DFA_to_graph(compliment(nfa),"Automate_complement")
print("L'automate Complément")


# In[8]:



text_lines = list()
line = ""
for state in nfa.transitions.keys():
    mid_transition = nfa.transitions[state]
    line += state + " ----> "
    for alphabet in mid_transition.keys():
        transition = mid_transition[alphabet]
        for trans in transition:
            line += alphabet+ trans + " / "
    if state in nfa.final_states : line += "&"
    text_lines.append(line)
    line = ""

pdf = canvas.Canvas("grammaire.pdf")
pdf.setTitle('TP THP')

text_lines = list()
line = ""
for state in nfa.transitions.keys():
    mid_transition = nfa.transitions[state]
    line += state + " ----> "
    for alphabet in mid_transition.keys():
        transition = mid_transition[alphabet]
        for trans in transition:
            line += alphabet+ trans + " / "
    if state in nfa.final_states : line += "&"
    text_lines.append(line)
    line = ""
pdf.setFont("Times-Roman",26)
pdf.drawCentredString(300, 800, "Les grammaires de l'automate")
pdf.line(30,770,570,770)
pdf.setFont("Times-Roman",22)
pdf.drawCentredString(300,730,"L'automate de base ")
pdf.setFont("Times-Roman",18)
pdf.drawString(40,680,"Grammaire Reguliere gauche :")
text = pdf.beginText(40,660)
text.setFont("Times-Roman",15)
for line in text_lines:
    text.textLine(line)
pdf.drawText(text)


mir = miror(nfa)
text_lines = list()
line = ""
for state in mir.transitions.keys():
    mid_transition = mir.transitions[state]
    line += state + " ----> "
    for alphabet in mid_transition.keys():
        transition = mid_transition[alphabet]
        for trans in transition:
            line += alphabet+ trans + " / "
    if state in mir.final_states : line += "&"
    text_lines.append(line)
    line = ""
pdf.setFont("Times-Roman",22)
pdf.drawCentredString(300,500,"Le miroir")
pdf.setFont("Times-Roman",18)
pdf.drawString(40,450,"Grammaire Reguliere gauche :")
text = pdf.beginText(40,430)
text.setFont("Times-Roman",15)
for line in text_lines:
    text.textLine(line)
pdf.drawText(text)




comp = compliment(nfa)
text_lines = list()
line = ""
for transition in comp.transitions.keys() :
    mid = comp.transitions[transition]
    line += transition + " ----> "
    for alphabet in mid.keys():
        line += alphabet + mid[alphabet] + " / "
    if transition in comp.final_states: line += "&"
    print(line)
    text_lines.append(line)
    line=""
pdf.setFont("Times-Roman",22)
pdf.drawCentredString(300,330,"Le complément")
pdf.setFont("Times-Roman",18)
pdf.drawString(40,300,"Grammaire Reguliere gauche :")
text = pdf.beginText(40,270)
text.setFont("Times-Roman",15)
for line in text_lines:
    text.textLine(line)
pdf.drawText(text)


pdf.save()



# In[9]:


from wand.image import Image as WImage
img = WImage(filename='grammaire.pdf')
img
print("Géneration des grammaires :")


# In[ ]:





# In[ ]:




