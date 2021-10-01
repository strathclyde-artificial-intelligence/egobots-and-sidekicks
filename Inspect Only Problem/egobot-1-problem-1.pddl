(define (problem egobot-1-problem) (:domain maintenance-domain)
(:objects 
    l11 l12 l13 l14 l21 l22 l23 l24 l31 l32 l33 l34 l41 l42 l43 l44 lsid - location
    ego1 - egobot
    sid - sidekick
    pn111 pn112 pn113 pn114 pn121 pn122 pn123 pn124 pn131 pn132 pn133 pn134 pn141 pn142 pn143 pn144 - panel
    pn211 pn212 pn213 pn214 pn221 pn222 pn223 pn224 pn231 pn232 pn233 pn234 pn241 pn242 pn243 pn244 - panel
    pn311 pn312 pn313 pn314 pn321 pn322 pn323 pn324 pn331 pn332 pn333 pn334 pn341 pn342 pn343 pn344 - panel
    pn411 pn412 pn413 pn414 pn421 pn422 pn423 pn424 pn431 pn432 pn433 pn434 pn441 pn442 pn443 pn444 - panel
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

    (egobot-adjacent l21 l22)
    (egobot-adjacent l22 l23)
    (egobot-adjacent l23 l24)
    (egobot-adjacent l24 l23)
    (egobot-adjacent l23 l22)
    (egobot-adjacent l22 l21)

    (egobot-adjacent l31 l32)
    (egobot-adjacent l32 l33)
    (egobot-adjacent l33 l34)
    (egobot-adjacent l34 l33)
    (egobot-adjacent l33 l32)
    (egobot-adjacent l32 l31)

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

    (hands-free ego1)
))

;un-comment the following line if metric is needed
;(:metric minimize (???))
)
