;Header and description
(define (domain system_domain)
(:requirements :strips :typing :negative-preconditions)

(:types
    location - object
    robot - object
    possible_move - object
    person - object
    bomb - object
    thing - object
)

(:predicates 
    (at-location ?o - object ?l - location)
    (visited ?r-robot ?l - location)
    (talked ?r - robot ?p - person ?l - location)
    (shouted ?r - robot)
    (jumped ?r - robot)
    (taken_thing ?t - thing)
    (given_thing ?t - thing ?l - location)
    (approached ?r - robot ?p - person)
    (guided ?p - person ?l - location)
)
(:action move_between_locations
    :parameters (
        ?r - robot 
        ?start_loc - location 
        ?end_loc - location
    )
    :precondition (
        and
        (at-location ?r ?start_loc)
        (not(at-location ?r ?end_loc))
    )

    :effect (
        and
        (at-location ?r ?end_loc)
        (not(at-location ?r ?start_loc))
    )
)

(:action talk_to_person
    :parameters (
        ?r - robot 
        ?p - person 
        ?l - location
    )
    :precondition (
        and
        (at-location ?r ?l)
        (at-location ?p ?l)
    )
    :effect (
        and(talked ?r ?p ?l)
    )
)

(:action shout
    :parameters (?r - robot)
    :precondition ()
    :effect (
        and(shouted ?r)
    )
)

(:action jump
    :parameters (?r - robot)
    :precondition ()
    :effect (
        and(jumped ?r)
    )
)

(:action take_thing
    :parameters (
        ?r - robot 
        ?t - thing 
        ?l - location 
    )
    :precondition (
        and
        (at-location ?r ?l)
        (at-location ?t ?l)
    )
    :effect (
        and(taken_thing ?t)
    )
)

(:action give_thing
    :parameters (
        ?r - robot 
        ?t - thing 
        ?l - location
    )
    :precondition (
        and
        (at-location ?r ?l)
        (taken_thing ?t)
        (not(given_thing ?t ?l))
    )
    :effect (
        and
        (not(taken_thing ?t))
        (given_thing ?t ?l)
    )
)

(:action move_thing
    :parameters (
        ?r - robot
        ?t - thing
        ?start-loc - location
        ?end-loc - location
    )
    :precondition (
        and
        (at-location ?r ?start-loc)
        (at-location ?t ?start-loc)
        (taken_thing ?t)
    )
    :effect (
        and
        (at-location ?r ?end-loc)
        (at-location ?t ?end-loc)
        (taken_thing ?t)
    )
)

(:action approach_human
    :parameters (
        ?r - robot 
        ?p - person 
        ?l - location)
    :precondition (
        and
        (at-location ?r ?l)
        (at-location ?p ?l)
        (not(approached ?r ?p))
    )
    :effect (
        and
        (approached ?r ?p)
    )
)

(:action assist_human_with_transport
    :parameters (
        ?r - robot 
        ?p - person
        ?start_loc - location
        ?end_loc - location)
    :precondition (
        and
        (at-location ?r ?start_loc)
        (at-location ?p ?start_loc)
        (not(at-location ?r ?end_loc))
        (not(at-location ?p ?end_loc))
        (approached ?r ?p)
        (not(guided ?p ?end_loc))
    )
    :effect (
        and
        (at-location ?r ?end_loc)
        (at-location ?p ?end_loc)
        (not(at-location ?r ?start_loc))
        (not(at-location ?p ?start_loc))
        (not(approached ?r ?p))
        (guided ?p ?end_loc)
    )
)
)
