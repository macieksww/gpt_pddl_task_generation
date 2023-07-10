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
    (at ?o - object ?l - location)
    (talked ?r - robot ?p - person ?l - location)
    (shouted ?r - robot)
    (jumped ?r - robot)
    (taken_thing ?t - thing)
    (give_thing ?t - thing)
)
(:action move_between_locations
    :parameters (?r - robot 
        ?start_loc - location ?end_loc - location)
    :precondition (
        and(at ?r ?start_loc)
        (not(at ?r ?end_loc))
    )

    :effect (
        and(at ?r ?end_loc)
        (not(at ?r ?start_loc))
    )
)

(:action talk_to_person
    :parameters (?r - robot 
        ?p - person ?l - location)
    :precondition (
        and(at ?r ?l)
            (at ?p ?l)
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
    :parameters (?r - robot 
        ?t - thing ?l - location ?p - person)
    :precondition (
        and(at ?r ?l)
            (at ?t ?l)
            (at ?p ?l)
    )
    :effect (
        and(taken_thing ?t)
    )
)

(:action give_thing
    :parameters (?r - robot 
        ?t - thing ?l - location)
    :precondition (
        and(at ?r ?l)
        (taken_thing ?t)
    )
    :effect (
        and(not(taken_thing ?t))
        (give_thing ?t)
    )
)
)
