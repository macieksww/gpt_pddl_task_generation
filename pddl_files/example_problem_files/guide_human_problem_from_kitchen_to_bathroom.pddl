(define (problem guide_human_from_kitchen_to_bathroom)
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
(:goal (and
    (guided macias bathroom)
)
)
)