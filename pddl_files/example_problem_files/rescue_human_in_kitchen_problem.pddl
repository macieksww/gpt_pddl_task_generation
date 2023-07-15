(define (problem rescue_human_in_kitchen_problem)
(:domain system_domain)
(:objects
    kitchen bathroom livingroom startpoint - location
    rico - robot
    macias - person
)
(:init
    (at-location rico startpoint)
    (at-location macias kitchen)
)
(:goal  
    (and
    (approached rico macias)
    (talked rico macias kitchen)
)
)
)