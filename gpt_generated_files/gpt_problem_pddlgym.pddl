(define (problem system_problem)
(:domain system_domain)
(:objects
    kitchen bathroom livingroom startpoint - location
    rico - robot
    coffee - thing
)
(:init
    (at-location-robot rico startpoint)
    (at-location-thing coffee kitchen)
)
(:goal 
    (and
        (given-thing coffee livingroom)
    )
)
)
