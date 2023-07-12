(define (problem system_problem)
  (:domain system_domain)

  ; Objects
  (:objects
    robot1 - robot
    location1 location2 - location
    person1 - person
    coffee - thing
  )

  ; Initial state
  (:init
    (at robot1 location1)
    (at person1 location1)
    (at coffee location2)
  )

  ; Goal state
  (:goal
    (taken_thing coffee)
  )
)
