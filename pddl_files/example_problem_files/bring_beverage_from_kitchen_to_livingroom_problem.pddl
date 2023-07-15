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
    (and
    (given_thing beverage livingroom)
)
)
)