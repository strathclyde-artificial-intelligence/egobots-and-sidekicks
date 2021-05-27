(define (problem egobot-3-reduced-problem) (:domain maintenance-domain)
(:objects 
    l11 l12 l13 l14 l21 l22 l23 l24 l31 l32 l33 l34 l41 l42 l43 l44 lsid - location
    ego3 - egobot
    sid - sidekick
    pn311 pn312 pn313 pn314 pn321 pn322 pn323 pn324 pn331 pn332 pn333 pn334 pn341 pn342 pn343 pn344 - panel
    w1 w2 - welder
    pa1 pa2 pa3 pa4 pa5 pa6 pa7 pa8 - patch
)

(:init
    (egobot-adjacent l31 l32)
    (egobot-adjacent l32 l33)
    (egobot-adjacent l33 l34)
    (egobot-adjacent l34 l33)
    (egobot-adjacent l33 l32)
    (egobot-adjacent l32 l31)

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

    (at ego3 l32)
    (camera-free ego3)
    (hands-free ego3)
    
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

    (panel-at pn311 l31)
    (panel-at pn312 l31)
    (panel-at pn313 l31)
    (panel-at pn314 l31)

    (panel-at pn321 l32)
    (panel-at pn322 l32)
    (panel-at pn323 l32)
    (panel-at pn324 l32)

    (panel-at pn331 l33)
    (panel-at pn332 l33)
    (panel-at pn333 l33)
    (panel-at pn334 l33)

    (panel-at pn341 l34)
    (panel-at pn342 l34)
    (panel-at pn343 l34)
    (panel-at pn344 l34)

    (deadline-open)
)

(:goal (and
    (is-inspected pn311)
    (is-inspected pn312)
    (is-inspected pn313)
    (is-inspected pn314)

    (is-inspected pn321)
    (is-inspected pn322)
    (is-inspected pn323)
    (is-inspected pn324)
    
    (is-inspected pn331)
    (is-inspected pn332)
    (is-inspected pn333)
    (is-inspected pn334)

    (is-inspected pn341)
    (is-inspected pn342)
    (is-inspected pn343)
    (is-inspected pn344)
))

;un-comment the following line if metric is needed
;(:metric minimize (???))
)
