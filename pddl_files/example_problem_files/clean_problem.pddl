(define (problem clean_problem)
(:domain system_domain)
(:objects
    kitchen bathroom livingroom startpoint - location
    rico - robot
)
(:init
    (at-location rico startpoint)
    (not(at-location rico bathroom))
    (not(at-location rico kitchen))
    (not(at-location rico livingroom))
)
(:goal 
    (and
    (visited rico kitchen)
    (visited rico bathroom)
    (visited rico livingroom)
)
)
)