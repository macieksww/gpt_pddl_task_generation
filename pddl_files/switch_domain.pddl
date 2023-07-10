(define (domain switch) 
(:requirements :strips)
(:predicates 
(switch_is_on) 
(switch_is_off)
)
(:action switch_on 
 :precondition (switch_is_off)
 :effect (and 
 (switch_is_on)
 (not (switch_is_off))
 )
)
 (:action switch_off 
 :precondition (switch_is_on) 
 :effect (and 
 (switch_is_off)
 (not (switch_is_on))
 )
) 
)