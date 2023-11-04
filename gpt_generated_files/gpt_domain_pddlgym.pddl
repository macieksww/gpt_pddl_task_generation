;Header and description
(define (domain system_domain)
(:requirements :strips :typing :negative-preconditions)

(:types
    location - object
    robot - object
    person - object
    thing - object
)

(:predicates 
    (at-location-robot ?r - robot ?l - location)
    (at-location-thing ?t - thing ?l - location)
    (at-location-person ?p - person ?l - location)
    (visited ?r - robot ?l - location)
    (talked ?r - robot ?p - person ?l - location)
    (shouted ?r - robot)
    (jumped ?r - robot)
    (taken-thing ?t - thing)
    (given-thing ?t - thing ?l - location)
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
        (at-location-robot ?r ?start_loc)
        (not(at-location-robot ?r ?end_loc))
    )

    :effect (
        and
        (at-location-robot ?r ?end_loc)
        (not(at-location-robot ?r ?start_loc))
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
        (at-location-robot ?r ?l)
        (at-location-person ?p ?l)
    )
    :effect (
        and(talked ?r ?p ?l)
    )
)

;(:action shout
;    :parameters (?r - robot)
;    :precondition ()
;    :effect (
;        and(shouted ?r)
;    )
;)
;
;(:action jump
;    :parameters (?r - robot)
;    :precondition ()
;    :effect (
;        and(jumped ?r)
;    )
;)

(:action take_thing
    :parameters (
        ?r - robot 
        ?t - thing 
        ?l - location 
    )
    :precondition (
        and
        (at-location-robot ?r ?l)
        (at-location-thing ?t ?l)
    )
    :effect (
        and(taken-thing ?t)
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
        (at-location-robot ?r ?l)
        (taken-thing ?t)
        (not(given-thing ?t ?l))
    )
    :effect (
        and
        (not(taken-thing ?t))
        (given-thing ?t ?l)
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
        (at-location-robot ?r ?start-loc)
        (at-location-thing ?t ?start-loc)
        (taken-thing ?t)
    )
    :effect (
        and
        (at-location-robot ?r ?end-loc)
        (at-location-thing ?t ?end-loc)
        (taken-thing ?t)
    )
)

(:action approach_human
    :parameters (
        ?r - robot 
        ?p - person 
        ?l - location)
    :precondition (
        and
        (at-location-robot ?r ?l)
        (at-location-person ?p ?l)
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
        (at-location-robot ?r ?start_loc)
        (at-location-person ?p ?start_loc)
        (not(at-location-robot ?r ?end_loc))
        (not(at-location-person ?p ?end_loc))
        (approached ?r ?p)
        (not(guided ?p ?end_loc))
    )
    :effect (
        and
        (at-location-robot ?r ?end_loc)
        (at-location-person ?p ?end_loc)
        (not(at-location-robot ?r ?start_loc))
        (not(at-location-person ?p ?start_loc))
        (not(approached ?r ?p))
        (guided ?p ?end_loc)
    )
)
)
