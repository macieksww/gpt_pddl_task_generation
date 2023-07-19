Sure! Here is the PDDL problem file for the task of making a coffee, based on the provided domain file and the actions that the system can perform:

```PDDL
(define (problem system_problem)
(:domain system_domain)
(:objects
    kitchen bathroom livingroom startpoint - location
    rico - robot
    coffee - thing
)
(:init
    (at-location rico startpoint)
    (at-location coffee kitchen)
)
(:goal 
    (and
        (given_thing coffee livingroom)
    )
)
)
```

This problem file represents the task of making a coffee. The initial state specifies that the robot Rico is at the startpoint location and the coffee is located in the kitchen. The goal is to give the coffee to the livingroom location.

Please note that this problem file does not include any comments.