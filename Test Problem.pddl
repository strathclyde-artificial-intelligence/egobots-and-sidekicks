(define (problem test-problem) (:domain maintenance-domain)
(:objects 
    l1 l2 l3 - location
    ego - egobot
    sid - sidekick
    pn11 pn12 pn13 pn21 pn22 pn23 - panel
    w - welder
    pa1 pa2 - patch
)

(:init
    (egobot-adjacent l1 l2)
    (egobot-adjacent l2 l1)
    (sidekick-adjacent l1 l2)
    (sidekick-adjacent l2 l1)
    (sidekick-adjacent l2 l3)
    (sidekick-adjacent l3 l2)
    (at ego l1)
    (camera-free ego)
    (hands-free ego)
    (at sid l3)
    (camera-free sid)
    (hands-free sid)
    (dropped w l3)
    (dropped pa1 l3)
    (dropped pa2 l3)
    (panel-at pn11 l1)
    (panel-at pn12 l1)
    (panel-at pn13 l1)
    (panel-at pn21 l2)
    (panel-at pn22 l2)
    (panel-at pn23 l2)

    (deadline-open)
)

(:goal (and
    (is-inspected pn11)
    (is-welded pn12)
    (is-patched pn13)
    (is-inspected pn21)
    (is-patched pn22)
    (is-inspected pn23)
))

)
