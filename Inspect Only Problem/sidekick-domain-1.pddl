;Header and description

(define (domain maintenance-domain-gobjects)

;I set it to use durative actions so I can have at start and at end things
(:requirements :durative-actions :typing :numeric-fluents :timed-initial-literals)

(:types 
    egobot sidekick - robot
    location
    panel
    patch welder - tool
)

(:functions
    (ingoal ?pn - panel)
    (pagoal ?l - location)
    (wegoal ?l - location)
    (score)
)

;camera-free restricts the robots to only one inspect, patch, weld, pick-up, or drop action at a time
;hands-free restricts the robots to carrying only one tool at a time
;hands-free is negated by holding
;dropped is negated by holding
;there are two different definitions of adjacency, because sidekick can travel further than egobot
;issues do not exist, there are simply goals to achieve panel predicates
;inspection requires no tool and can be done by any robot
;patching requires a patch, must be done by an egobot, and consumes the patch
;welding requires a welder, must be done by an egobot, and does not consume the welder
(:predicates 
    (hands-free ?r - robot)
    (camera-free ?r - robot)
    (at ?r - robot ?l - location)
    (holding ?r - robot ?t - tool)
    (dropped ?t - tool ?l - location)
    (egobot-adjacent ?l1 - location ?l2 - location)
    (sidekick-adjacent ?l1 - location ?l2 - location)
    (panel-at ?pn - panel ?l - location)
    (is-inspected ?pn - panel)
    (is-not-inspected ?pn - panel)
    (is-patched ?pn - panel)
    (is-welded ?pn - panel)

    (deadline-open)
)

(:durative-action egobot-move
    :parameters (?e - egobot ?l1 - location ?l2 - location)
    :duration (= ?duration 1)
    :condition (and 
        (at start (and 
            (at ?e ?l1)
        ))
        (over all (and
            (egobot-adjacent ?l1 ?l2)
        ))
    )
    :effect (and 
        (at start (and 
            (not (at ?e ?l1))
        ))
        (at end (and 
            (at ?e ?l2)
        ))
    )
)

(:durative-action sidekick-move
    :parameters (?s - sidekick ?l1 - location ?l2 - location)
    :duration (= ?duration 1)
    :condition (and 
        (at start (and 
            (at ?s ?l1)
        ))
        (over all (and
            (sidekick-adjacent ?l1 ?l2)
        ))
    )
    :effect (and 
        (at start (and (not (at ?s ?l1))))
        (at end (and (at ?s ?l2)))
    )
)



(:durative-action inspect
    :parameters (?r - robot ?pn - panel ?l - location)
    :duration (= ?duration 1)
    :condition (and 
        (at start (camera-free ?r))
        (at start (deadline-open))
        (over all (panel-at ?pn ?l))
        (over all (at ?r ?l))
        (at start (is-not-inspected ?pn))
    )
    :effect (and 
        (at start (not (is-not-inspected ?pn)))
        (at start (not (camera-free ?r)))
        (at end (is-inspected ?pn))
        (at end  (camera-free ?r))
        (at end (increase (score) (ingoal ?pn)))
        )
    )
)