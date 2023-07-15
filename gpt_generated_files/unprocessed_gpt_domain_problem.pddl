I apologize for the error. Here is the corrected PDDL problem definition for the "bring_beverage" planning problem:

```plaintext
(define (problem bring_beverage)
    (:domain system_domain)
    (:objects
        kitchen bathroom livingroom startpoint - location
        rico - robot
        beverage - thing
    )
    (:init
        (at-location rico bathroom)
        (at-location beverage kitchen)
    )
    (:goal 
        (given_thing beverage livingroom)
    )
)
```

Please note that I have fixed the parameter type for the "given_thing" proposition in the goal state.