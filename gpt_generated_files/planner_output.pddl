Domain parsed
Problem parsed
Grounding..
Light Validation Completed
Simplification..
(Pre Simplification) - |A|+|P|+|E|: 42
(After Easy Simplification) - |A|+|P|+|E|: 42
(After AIBR):42
Grounding and Simplification finished
|A|:42
|P|:0
|E|:0
Size(X):0
Size(F):15
Setting horizon to:NaN
Running WA-STAR
Reachable actions and processes: |A U P U E|:42
h(n = s_0)=21.0
f(n) = 21.0 (Expanded Nodes: 0, Evaluated States: 0, Time: 0.016)
f(n) = 22.0 (Expanded Nodes: 12, Evaluated States: 25, Time: 0.051)
f(n) = 23.0 (Expanded Nodes: 15, Evaluated States: 26, Time: 0.051)
f(n) = 28.0 (Expanded Nodes: 16, Evaluated States: 26, Time: 0.052)
Starting Validation
Plan is executed correctly
(Pddl2.1 semantics) Plan is valid:true
Problem Solved
0.0: (move_between_locations rico startpoint kitchen )
1.0: (take_thing rico coffee kitchen )
2.0: (move_between_locations rico kitchen livingroom )
3.0: (give_thing rico coffee livingroom )

Plan-Length:4
Duration:4.0
Metric (Plan):4.0
Metric (Search):4.0
Planning Time:885
Heuristic Time:28
Search Time:53
Expanded Nodes:19
States Evaluated:36
Fixed constraint violations during search (zero-crossing):0
Number of Dead-Ends detected:0
Number of Duplicates detected:65
