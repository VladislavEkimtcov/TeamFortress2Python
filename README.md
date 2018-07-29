# Title: Python Team Fortress 2 simulation

## Team Member(s):
Vladislav Ekimtcov

# Monte Carlo Simulation Scenario & Purpose:
This Python program simulates a match in Team Fortress 2, a popular video game developed by Valve Corporation. There is no objective in this simulation besides eliminating the enemy team. 

The primary goal of the simulation is to answer questions I had about Team Fortress 2 for the last nine years.

## Simulation's variables of uncertainty
All three simulations feature random spawn locations on the field, random classes used, random damage dealt and critical hit chance. 

## Hypothesis or hypotheses before running the simulation:
* Do teams with a Healer character have an advantage? This question had been bothering me for a while and is the main reason I wanted to build this simulation.
* Does the settled 6v6 format generalist class lineup pose an advantage? Team Fortress 2 competitive scene is highly controversial, and the "traditional" team lineup had been discussed many, many times. This simulation aims to evaluate its effectiveness.
* How accurate is this simulation? To evaluate the other two outcomes, this simulation will calculate how correct the simulated classes are at dealing damage and whenever it corresponds to real life.  

## Analytical Summary of your findings:
Healer simulation: the simulation confirms my suspicion that teams that feature Healers have the upper hand.

6v6 simulation: the simulation had provided results opposite of reality, meaning that further improvements need to be made.

Damage and kills simulation had demonstrated that the class damage output is mostly correct, but can be fine-tuned further. 

No adjustments were made to keep results consistent and repeatable, but some conclusions were drawn for further improvements.

## Instructions on how to use the program:
Run _Main_visual.py_ to see the game play itself with the verbose output. You can modify the _field_size_ and spawn classes/heroes for teams of your choosing, for example:

```
h2 = Healer("Red", "Healer")
players.append(h2)
i1 = Infiltrator("Blue", "Infiltrator")
players.append(i1)
``` 
To run the healer simulation, use _Healers research.py_. To run the 6v6 simulation, run _6v6 research.py_. To run the self-evaluation/most damaging class simulation, run _Damage and Frags research.py_. 

## All Sources Used:
TF2 wiki: https://wiki.teamfortress.com/wiki/Main_Page

TF2 on Wikipedia: https://en.wikipedia.org/wiki/Team_Fortress_2
