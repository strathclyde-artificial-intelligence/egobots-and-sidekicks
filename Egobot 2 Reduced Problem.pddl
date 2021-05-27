(define (problem egobot-2-reduced-problem) (:domain maintenance-domain)
(:objects 
    l11 l12 l13 l14 l21 l22 l23 l24 l31 l32 l33 l34 l41 l42 l43 l44 lsid - location
    ego2 - egobot
    sid - sidekick
    pn211 pn212 pn213 pn214 pn221 pn222 pn223 pn224 pn231 pn232 pn233 pn234 pn241 pn242 pn243 pn244 - panel
    w1 w2 - welder
    pa1 pa2 pa3 pa4 pa5 pa6 pa7 pa8 - patch
)

(:init
    (egobot-adjacent l21 l22)
    (egobot-adjacent l22 l23)
    (egobot-adjacent l23 l24)
    (egobot-adjacent l24 l23)
    (egobot-adjacent l23 l22)
    (egobot-adjacent l22 l21)

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

    (at ego2 l22)
    (camera-free ego2)
    (hands-free ego2)
    
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

    (panel-at pn211 l21)
    (panel-at pn212 l21)
    (panel-at pn213 l21)
    (panel-at pn214 l21)

    (panel-at pn221 l22)
    (panel-at pn222 l22)
    (panel-at pn223 l22)
    (panel-at pn224 l22)

    (panel-at pn231 l23)
    (panel-at pn232 l23)
    (panel-at pn233 l23)
    (panel-at pn234 l23)

    (panel-at pn241 l24)
    (panel-at pn242 l24)
    (panel-at pn243 l24)
    (panel-at pn244 l24)

    (deadline-open)
)

(:goal (and
    (is-inspected pn211)
    (is-inspected pn212)
    (is-inspected pn213)
    (is-inspected pn214)

    (is-inspected pn221)
    (is-inspected pn222)
    (is-inspected pn223)
    (is-inspected pn224)
    
    (is-inspected pn231)
    (is-inspected pn232)
    (is-inspected pn233)
    (is-inspected pn234)

    (is-inspected pn241)
    (is-inspected pn242)
    (is-inspected pn243)
    (is-inspected pn244)

    (hands-free ego2)
))

;un-comment the following line if metric is needed
;(:metric minimize (???))
)
