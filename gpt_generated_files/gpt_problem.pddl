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
