(define (problem egobot-4-reduced-problem) (:domain maintenance-domain)
(:objects 
    l11 l12 l13 l14 l21 l22 l23 l24 l31 l32 l33 l34 l41 l42 l43 l44 lsid - location
    ego4 - egobot
    sid - sidekick
    pn411 pn412 pn413 pn414 pn421 pn422 pn423 pn424 pn431 pn432 pn433 pn434 pn441 pn442 pn443 pn444 - panel
    w1 w2 - welder
    pa1 pa2 pa3 pa4 pa5 pa6 pa7 pa8 - patch
)

(:init
    (egobot-adjacent l41 l42)
    (egobot-adjacent l42 l43)
    (egobot-adjacent l43 l44)
    (egobot-adjacent l44 l43)
    (egobot-adjacent l43 l42)
    (egobot-adjacent l42 l41)

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

    (at ego4 l42)
    (camera-free ego4)
    (hands-free ego4)
    
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

    (panel-at pn411 l41)
    (panel-at pn412 l41)
    (panel-at pn413 l41)
    (panel-at pn414 l41)

    (panel-at pn421 l42)
    (panel-at pn422 l42)
    (panel-at pn423 l42)
    (panel-at pn424 l42)

    (panel-at pn431 l43)
    (panel-at pn432 l43)
    (panel-at pn433 l43)
    (panel-at pn434 l43)

    (panel-at pn441 l44)
    (panel-at pn442 l44)
    (panel-at pn443 l44)
    (panel-at pn444 l44)

    (deadline-open)
)

(:goal (and
    (is-inspected pn411)
    (is-inspected pn412)
    (is-inspected pn413)
    (is-inspected pn414)

    (is-inspected pn421)
    (is-inspected pn422)
    (is-inspected pn423)
    (is-inspected pn424)
    
    (is-inspected pn431)
    (is-inspected pn432)
    (is-inspected pn433)
    (is-inspected pn434)

    (is-inspected pn441)
    (is-inspected pn442)
    (is-inspected pn443)
    (is-inspected pn444)

    (hands-free ego4)
))

;un-comment the following line if metric is needed
;(:metric minimize (???))
)
