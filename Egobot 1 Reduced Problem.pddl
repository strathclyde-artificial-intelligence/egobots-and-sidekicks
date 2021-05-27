(define (problem egobot-1-problem) (:domain maintenance-domain)
(:objects 
    l11 l12 l13 l14 l21 l22 l23 l24 l31 l32 l33 l34 l41 l42 l43 l44 lsid - location
    ego1 - egobot
    sid - sidekick
    pn111 pn112 pn113 pn114 pn121 pn122 pn123 pn124 pn131 pn132 pn133 pn134 pn141 pn142 pn143 pn144 - panel
    w1 w2 - welder
    pa1 pa2 pa3 pa4 pa5 pa6 pa7 pa8 - patch
)

(:init
    (egobot-adjacent l11 l12)
    (egobot-adjacent l12 l13)
    (egobot-adjacent l13 l14)
    (egobot-adjacent l14 l13)
    (egobot-adjacent l13 l12)
    (egobot-adjacent l12 l11)

    (sidekick-adjacent l11 l12)
    (sidekick-adjacent l12 l13)
    (sidekick-adjacent l13 l14)
    (sidekick-adjacent l14 l21)
    (sidekick-adjacent l21 l22)
    (sidekick-adjacent l22 l23)
    (sidekick-adjacent l23 l24)
    (sidekick-adjacent l24 l31)
    (sidekick-adjacent l31 l32)
    (sidekick-adjacent l32 l33)
    (sidekick-adjacent l33 l34)
    (sidekick-adjacent l34 l41)
    (sidekick-adjacent l41 l42)
    (sidekick-adjacent l42 l43)
    (sidekick-adjacent l43 l44)
    (sidekick-adjacent l44 l11)
    (sidekick-adjacent l44 lsid)
    (sidekick-adjacent l12 l11)
    (sidekick-adjacent l13 l12)
    (sidekick-adjacent l14 l13)
    (sidekick-adjacent l21 l14)
    (sidekick-adjacent l22 l21)
    (sidekick-adjacent l23 l22)
    (sidekick-adjacent l24 l23)
    (sidekick-adjacent l31 l24)
    (sidekick-adjacent l32 l31)
    (sidekick-adjacent l33 l32)
    (sidekick-adjacent l34 l33)
    (sidekick-adjacent l41 l34)
    (sidekick-adjacent l42 l41)
    (sidekick-adjacent l43 l42)
    (sidekick-adjacent l44 l43)
    (sidekick-adjacent l11 l44)
    (sidekick-adjacent lsid l44)
    
    (at ego1 l12)
    (camera-free ego1)
    (hands-free ego1)
    
    (at sid lsid)
    (camera-free sid)
    (hands-free sid)

    (dropped w1 lsid)
    (dropped w2 lsid)
    (dropped pa1 lsid)
    (dropped pa2 lsid)
    (dropped pa3 lsid)
    (dropped pa4 lsid)
    (dropped pa5 lsid)
    (dropped pa6 lsid)
    (dropped pa7 lsid)
    (dropped pa8 lsid)

    (panel-at pn111 l11)
    (panel-at pn112 l11)
    (panel-at pn113 l11)
    (panel-at pn114 l11)

    (panel-at pn121 l12)
    (panel-at pn122 l12)
    (panel-at pn123 l12)
    (panel-at pn124 l12)

    (panel-at pn131 l13)
    (panel-at pn132 l13)
    (panel-at pn133 l13)
    (panel-at pn134 l13)

    (panel-at pn141 l14)
    (panel-at pn142 l14)
    (panel-at pn143 l14)
    (panel-at pn144 l14)

    (deadline-open)
)

(:goal (and
    (is-inspected pn111)
    (is-inspected pn112)
    (is-inspected pn113)
    (is-inspected pn114)

    (is-inspected pn121)
    (is-inspected pn122)
    (is-inspected pn123)
    (is-inspected pn124)
    
    (is-inspected pn131)
    (is-inspected pn132)
    (is-inspected pn133)
    (is-inspected pn134)

    (is-inspected pn141)
    (is-inspected pn142)
    (is-inspected pn143)
    (is-inspected pn144)
))

;un-comment the following line if metric is needed
;(:metric minimize (???))
)
