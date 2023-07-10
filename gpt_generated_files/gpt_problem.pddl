(define (problem system_problem)
  (:domain system_domain)
  (:objects
    robot1 - robot
    location1 - location
    location2 - location
    person1 - person
    coffee_machine - thing
  )
  (:init
    (at robot1 location1)
    (at person1 location1)
    (at coffee_machine location2)
  )
  (:goal
    (taken_thing coffee_machine)
  )
)
