(define (problem system_problem)
(:domain system_domain)
(:objects
    robot1 - robot
    person1 - person
    location1 - location
    location2 - location
    thing1 - thing
    bomb1 - bomb
)
(:init
    (at robot1 location1)
    (at person1 location1)
    (at thing1 location1)
    (at bomb1 location2)
)
(:goal
    (and
        (at robot1 location2)
        (talked robot1 person1 location1)
        (shouted robot1)
        (jumped robot1)
        (taken_thing thing1)
    )
)
)
