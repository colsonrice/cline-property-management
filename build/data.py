# -*- coding: utf-8 -*-
"""
Content + config for the Cline Property Management site.

Copy follows Slack's content principles: clear, concise, human. In practice
that means short sentences, active voice, second person, sentence case for
headings and buttons, and no cleverness that costs clarity. Specifics beat
adjectives: "two to three inches" earns trust, "premium quality mulch" does not.
"""

SITE = {
    "name": "Cline Property Management",
    "short": "Cline",
    "tagline": "Grounds care for every season",
    "phone_display": "(317) 677-4709",
    "phone_href": "+13176774709",
    "email": "Clinepropertymanagement@gmail.com",
    "base": "https://www.squatchcraft.com/cline-property-management",
    "city": "Whitestown",
    "region": "IN",
    "region_long": "Indiana",
    "county": "Boone County",
    "areas_short": "Whitestown · Zionsville · West Carmel",
}

# The site currently lives on a borrowed GitHub Pages domain. Keep it out of
# the search index until it sits on a real Cline domain -- otherwise Google
# builds ranking authority at an address that is going to change, and the
# listings show someone else's brand in the URL.
# Flip to False, rebuild and redeploy once SITE["base"] is the real domain.
STAGING = True

MOW_AREAS = ["Whitestown", "Zionsville", "West Carmel"]

SEASONS = [
    {
        "key": "spring", "name": "Spring", "months": "March – May",
        "color": "#4E7F44",
        "count": "4 services",
        "head": "Reset the property",
        "body": "Winter leaves beds matted and edges ragged. In spring we clear all of it out, "
                "re-cut the bed lines, lay fresh mulch, and get your first cuts on the schedule.",
        "services": ["spring-fall-cleanups", "mulching", "lawn-mowing", "soft-washing"],
        "img": ("mulching", "mulch-install-front-entry", "Fresh spring mulch install at a front entry"),
    },
    {
        "key": "summer", "name": "Summer", "months": "June – August",
        "color": "#B98A28",
        "count": "4 services",
        "head": "Keep it sharp every week",
        "body": "Weekly mowing on a set day, clean edges, and beds that stay tidy. Summer is also "
                "the best window for washing, because siding and concrete dry fast and stay clean.",
        "services": ["lawn-mowing", "pressure-washing", "soft-washing", "mulching"],
        "img": ("mowing", "lawn-mowing-striped-residential", "Striped residential lawn after a summer cut"),
    },
    {
        "key": "fall", "name": "Fall", "months": "September – November",
        "color": "#B0552A",
        "count": "4 services",
        "head": "Stay ahead of the leaves",
        "body": "Leaves don't all come down at once, so one visit is rarely enough. We come back "
                "through the drop, finish with a full cleanup, and leave the property ready for winter.",
        "services": ["leaf-removal", "spring-fall-cleanups", "lawn-mowing", "mulching"],
        "img": ("leaf-removal", "leaf-removal-backpack-blower", "Crew clearing fall leaves with backpack blowers"),
    },
    {
        "key": "winter", "name": "Winter", "months": "December – February",
        "color": "#4A6B84",
        "count": "Snow & ice",
        "head": "Cleared before you leave",
        "body": "We clear drives, lots, and walks once snow hits an agreed depth. Commercial and "
                "HOA properties get priority routing and repeat passes while it's still falling.",
        "services": ["snow-removal"],
        "img": ("commercial", "commercial-median-shrub-beds", "Dormant-season commercial bed maintenance"),
    },
]

SERVICES = [
    {
        "slug": "lawn-mowing",
        "name": "Lawn Mowing",
        "nav": "Lawn Mowing",
        "short": "Weekly and bi-weekly cuts for homes, businesses, HOAs, and municipalities.",
        "title": "Lawn Mowing in Whitestown, Zionsville & West Carmel IN",
        "desc": "Weekly lawn mowing for homes, businesses, HOAs and municipalities in Whitestown, "
                "Zionsville and West Carmel, Indiana. Clean edges, free estimates.",
        "hero": ("mowing", "lawn-mowing-striped-residential"),
        "hero_alt": "Freshly striped residential lawn in Zionsville, Indiana",
        "lede": "A cut on a schedule you can plan your week around. Trimming, edging, and blow-off "
                "happen every visit, not just when there's time left over.",
        "area_note": True,
        "body": [
            ("h2", "What every visit includes"),
            ("p", "We cut at the right height for the season and alternate direction each time, which "
                  "keeps the grass standing upright. Then we handle everything the mower deck can't reach."),
            ("ul", [
                "Mowing at a seasonally adjusted height, with direction alternated each visit",
                "String trimming around beds, posts, trees, and foundations",
                "Mechanical edging along drives, walks, and curb lines",
                "A full blow-off of every hard surface before we leave",
                "Clippings dispersed or hauled off, depending on the property",
            ]),
            ("h2", "Properties we mow"),
            ("p", "Equipment and routing change a lot depending on what we're cutting, so it's worth "
                  "being specific."),
            ("cards", [
                ("Residential", "Weekly or bi-weekly cuts on a set day. Gated yards, narrow side yards, "
                                "and detailed landscaping are all fine."),
                ("Commercial", "Retail, office, and industrial frontage kept presentable on a schedule "
                               "that works around your business hours."),
                ("HOA and common areas", "Entrances, monument signs, common turf, and detention areas. "
                                         "These set the tone for a whole neighborhood."),
                ("Municipal", "Right-of-way, median, and roadside mowing, including the wide or steep "
                              "ground that needs bigger equipment."),
            ]),
            ("h2", "Overgrown lots and rough cutting"),
            ("p", "Not every job is a manicured lawn. Vacant lots, easements, and detention basins need "
                  "brush-capable equipment and a different approach. We take those on as one-time "
                  "reclaims or on a seasonal rotation."),
        ],
        "gallery": [
            ("mowing", "lawn-mowing-striped-residential", "Striped residential lawn, Zionsville"),
            ("mowing", "lawn-mowing-stripes-spring", "Early-season cut with clean stripe lines"),
            ("mowing", "rough-mowing-overgrown-lot", "Rough-cutting an overgrown lot"),
            ("mowing", "commercial-field-mowing", "Commercial frontage mowing"),
            ("mowing", "large-property-mowing-roadside", "Large roadside property, mowed and finished"),
            ("mowing", "acreage-mowing", "Acreage mowing on open ground"),
        ],
        "faqs": [
            ("Which towns do you mow?",
             "We mow in Whitestown, Zionsville, and West Carmel. Keeping the route tight is what lets us "
             "hold a consistent day of the week. Our other services travel further, so it's worth asking "
             "even if you're outside those three towns."),
            ("Weekly or every other week?",
             "Weekly through the main growing season is what we recommend, and it's what most properties "
             "end up on. Bi-weekly works in the shoulder months. In May and June, though, a two-week gap "
             "usually means cutting off more than a third of the blade, which stresses the lawn."),
            ("Do I need to be home?",
             "No. As long as we can reach the turf, we'll take care of it. Just leave gates unlocked and "
             "pets inside."),
            ("What happens if it rains on my day?",
             "We move you to the next workable day. Cutting saturated turf ruts the ground and clumps the "
             "clippings, which makes things worse. If weather pushes us more than a day or two, you'll "
             "hear from us."),
        ],
    },
    {
        "slug": "mulching",
        "name": "Mulching",
        "nav": "Mulching",
        "short": "Fresh mulch and re-cut bed edges, which is what makes a property look finished.",
        "title": "Mulch Installation & Bed Edging | Whitestown, IN",
        "desc": "Mulch installation, bed edging and seasonal refresh for homes, HOA entrances and "
                "commercial properties across Boone County, Indiana.",
        "hero": ("mulching", "mulch-install-front-entry"),
        "hero_alt": "Fresh dark mulch installed around a front entry with trimmed shrubs",
        "lede": "Nothing changes how a property looks faster than fresh mulch and a sharp bed edge. "
                "It's the highest-return day of work we do.",
        "body": [
            ("h2", "How we do a mulch job properly"),
            ("p", "Mulch dumped on top of last year's layer looks good for a month, then goes flat and "
                  "grey. The prep is what makes it last."),
            ("ul", [
                "Beds cleared of weeds, debris, and matted old material",
                "Edges re-cut to a clean, defined trench line",
                "Existing mulch turned and levelled so the depth stays even",
                "Fresh mulch deep enough to suppress weeds, but not deep enough to smother roots",
                "Mulch pulled back from trunks and stems instead of piled against them",
                "Walks, drives, and turf edges blown clean before we go",
            ]),
            ("h2", "Where it matters most"),
            ("p", "We mulch everything from a single front bed to every common area in a subdivision. "
                  "HOA entrances and monument signs are worth calling out. Residents and visitors see "
                  "them every day, and a crisp entrance sets expectations for the whole neighborhood."),
            ("h2", "How much mulch does a bed need?"),
            ("p", "Two to three inches is the working range. Under two inches, weeds push straight "
                  "through. Over four, you start holding water against roots and crowns."),
            ("p", "If a bed has had mulch piled on year after year without being turned, the right move "
                  "is usually to pull some out before adding any. We'll tell you when that's the case "
                  "rather than burying the problem."),
        ],
        "beforeafter": [
            ("mulching", "mulch-refresh-before", "mulch-refresh-after",
             "Front bed refresh", "Thin, tired beds re-cut and topped with fresh dark mulch"),
        ],
        "gallery": [
            ("mulching", "hoa-entrance-mulch-harcourt-springs", "HOA entrance beds at Harcourt Springs"),
            ("mulching", "hoa-monument-mulch-bed", "Monument sign bed, freshly mulched"),
            ("mulching", "mulch-install-entry-walkway", "Entry walkway beds with fresh mulch"),
            ("mulching", "mulch-bed-brick-wall", "Foundation bed along a brick elevation"),
            ("mulching", "mulch-bed-black-fence", "Bed line running along a wrought-iron fence"),
            ("mulching", "curbside-mulch-bed", "Curbside island bed, edged and mulched"),
            ("mulching", "tree-ring-mulch-curbside", "Tree ring mulched to a clean circle"),
            ("mulching", "mulch-bed-house-corner", "Corner bed with a re-cut edge"),
            ("mulching", "mulch-bed-fence-line", "Fence-line bed, weeded and topped"),
        ],
        "faqs": [
            ("When is the best time to mulch?",
             "Spring is the main window, usually April into May. That's once the ground has dried enough "
             "to work and before growth takes off. Fall mulching also works well and insulates beds going "
             "into winter. Either is fine."),
            ("Do you haul away the old mulch?",
             "Only when it needs it. Most beds are better served by turning and levelling what's already "
             "there, then topping it. That saves you money and it's better for the soil. When a bed has "
             "years of buildup choking the plants, we pull the excess and haul it off."),
            ("What kind of mulch do you use?",
             "Hardwood is the standard and what most properties get. If you'd prefer dyed black or brown, "
             "or decorative stone instead, tell us and we'll price it that way."),
            ("Can you edge the beds without adding new mulch?",
             "Yes. Re-cutting bed edges on its own makes a surprising difference, and it's a common "
             "mid-season touch-up when the mulch is still in decent shape."),
        ],
    },
    {
        "slug": "spring-fall-cleanups",
        "name": "Spring & Fall Cleanups",
        "nav": "Spring & Fall Cleanups",
        "short": "A full-property reset at both ends of the season.",
        "title": "Spring & Fall Property Cleanups | Boone County, IN",
        "desc": "Complete spring and fall property cleanups: bed clearing, cut-backs, debris removal "
                "and edging in Whitestown, Zionsville and West Carmel, Indiana.",
        "hero": ("cleanups", "fence-line-cleanup-before-after"),
        "hero_alt": "Before and after of an overgrown fence line cleared and cut back",
        "lede": "Two visits a year that make everything in between easier, and cheaper.",
        "body": [
            ("h2", "Spring cleanup"),
            ("p", "Winter leaves a property matted down and full of whatever blew in. A spring cleanup "
                  "clears it out and sets a clean baseline, so mowing, mulching, and planting all start "
                  "from solid ground."),
            ("ul", [
                "Beds cleared of leaves, sticks, and winter debris",
                "Matted turf raked out so it can breathe and green up evenly",
                "Ornamental grasses and perennials cut back",
                "Bed edges re-cut and defined",
                "Fence lines and hard-to-reach corners cleared",
                "All debris hauled off the property",
            ]),
            ("h2", "Fall cleanup"),
            ("p", "The fall version runs the same idea in reverse. We get everything off the property "
                  "before it sits under snow all winter, matting the turf and rotting into the beds."),
            ("ul", [
                "A final leaf clearing once the drop finishes",
                "Beds cleared and cut back for winter",
                "Gutters and hard surfaces cleared of leaf litter",
                "A final cut at the right height to go into dormancy",
                "Everything hauled away, not blown into the tree line",
            ]),
            ("h2", "Neglected and overgrown properties"),
            ("p", "Some properties have been let go for a season or several. Fence lines swallowed by "
                  "weeds, beds gone to brush, an easement nobody has touched. That's a reclaim rather "
                  "than a cleanup, and we do those too. It's usually one hard day that gets everything "
                  "back to a maintainable baseline."),
        ],
        "gallery": [
            ("cleanups", "fence-line-cleanup-before-after", "Fence line before and after clearing"),
            ("leaf-removal", "leaf-removal-raking-pile", "Raking out a heavy leaf accumulation"),
            ("leaf-removal", "leaf-removal-finished-lawn", "Property finished and cleared"),
            ("mulching", "mulch-bed-spring-shrubs", "Beds cleared and cut back in spring"),
        ],
        "faqs": [
            ("When should a spring cleanup happen?",
             "As soon as the ground firms up enough to work without tearing the turf. Around here that's "
             "usually mid-March into April. Going too early does more damage than waiting a week or two."),
            ("Is a fall cleanup the same as leaf removal?",
             "They overlap, but they're not the same. Leaf removal is the repeated passes through the "
             "drop. The fall cleanup is the single thorough visit at the end that also handles bed "
             "cut-backs, gutters, and the final mow. Most properties want both."),
            ("Do you haul the debris away?",
             "Yes, all of it goes with us. We don't blow debris into a neighbor's yard or pile it at the "
             "back of the property."),
        ],
    },
    {
        "slug": "leaf-removal",
        "name": "Leaf Removal",
        "nav": "Leaf Removal",
        "short": "Repeat visits through the drop, with a truck-mounted vacuum for the heavy stuff.",
        "title": "Leaf Removal in Whitestown & Zionsville, IN",
        "desc": "Fall leaf removal for homes, HOAs and commercial properties in Boone County, Indiana. "
                "Multiple scheduled passes and truck-mounted leaf vacuum.",
        "hero": ("leaf-removal", "leaf-removal-backpack-blower"),
        "hero_alt": "Crew member clearing heavy leaf cover with a backpack blower",
        "lede": "Leaves don't fall on a schedule. One pass in November is how lawns end up patchy and "
                "dead by spring.",
        "body": [
            ("h2", "Why one visit isn't enough"),
            ("p", "A mature canopy drops over several weeks, not over a weekend. Leaves left sitting "
                  "block light, hold moisture against the crown, and invite snow mold. That's why a lawn "
                  "that looked fine in October comes out of winter with dead patches shaped like leaf piles."),
            ("p", "We schedule repeat passes through the drop, then a final clearing once the canopy is "
                  "bare. The turf never stays smothered for long."),
            ("h2", "How we clear"),
            ("ul", [
                "Backpack and walk-behind blowers to move leaves out of beds and off turf",
                "A truck-mounted vacuum for volume, including wet piles a rake can't move",
                "Beds, fence lines, window wells, and landscape corners, not just open lawn",
                "Drives, walks, and patios blown clean",
                "Everything hauled off site",
            ]),
            ("h2", "Commercial and HOA leaf work"),
            ("p", "Parking lots, entrances, and common areas fill faster than anywhere else, because they "
                  "catch whatever blows in from around them. Wet leaves on a lot are also a real slip "
                  "hazard. We run commercial properties on a tighter rotation for that reason."),
        ],
        "gallery": [
            ("leaf-removal", "leaf-removal-backpack-blower", "Clearing leaves with a backpack blower"),
            ("leaf-removal", "leaf-vacuum-truck-curb", "Truck-mounted leaf vacuum working a curb line"),
            ("leaf-removal", "leaf-removal-raking-pile", "Raking out a heavy accumulation by hand"),
            ("leaf-removal", "leaf-removal-under-tree", "Clearing beneath a mature canopy"),
            ("leaf-removal", "leaf-removal-finished-lawn", "Turf cleared and ready for winter"),
            ("leaf-removal", "leaf-covered-yard", "Heavy leaf cover before clearing"),
            ("leaf-removal", "leaf-covered-driveway", "Leaf-covered drive before a pass"),
            ("leaf-removal", "fall-leaves-driveway", "Leaf line along a driveway edge"),
        ],
        "faqs": [
            ("How many visits will I need?",
             "It depends on your canopy. A property with a few young trees might need two passes. Mature "
             "oaks and maples usually mean three or four across October and November. We'll look at the "
             "property and give you a real number instead of selling you visits you don't need."),
            ("Can you just do one big cleanup at the end?",
             "We can, and for some properties that's the right call. But with heavy cover, waiting until "
             "the end means weeks of smothered turf and a heavier, more expensive final visit."),
            ("Do you mulch the leaves into the lawn instead?",
             "On light cover, yes. Mulching leaves back into the turf is good for the soil. Once cover "
             "gets heavy, it just leaves shredded material sitting on the crown, so it has to come off."),
        ],
    },
    {
        "slug": "snow-removal",
        "name": "Snow Removal",
        "nav": "Snow Removal",
        "short": "Drives, lots, and walks cleared at an agreed depth, with priority commercial routing.",
        "title": "Snow Removal & Ice Management | Whitestown, IN",
        "desc": "Commercial and residential snow plowing, walk clearing and ice management in "
                "Whitestown, Zionsville and West Carmel, Indiana.",
        "hero": ("commercial", "commercial-median-shrub-beds"),
        "hero_alt": "Dormant-season commercial property maintained through winter",
        "lede": "The point of snow service is that you don't have to think about it. You leave on time.",
        "body": [
            ("h2", "How service gets triggered"),
            ("p", "You don't have to call. Properties on contract are cleared automatically once snow "
                  "reaches an agreed depth, commonly two inches for commercial lots and residential "
                  "drives. During a long storm we make repeat passes, instead of letting it build into "
                  "something that can't be pushed."),
            ("h2", "What we clear"),
            ("ul", [
                "Residential driveways and walks",
                "Commercial parking lots, drive aisles, and approaches",
                "HOA private streets, common drives, and mail kiosk areas",
                "Sidewalks, entries, and ADA access routes",
                "Ice management on treated surfaces",
            ]),
            ("h2", "Commercial and HOA priority"),
            ("p", "Commercial and HOA properties are routed ahead of residential and cleared before "
                  "business hours. If you have a specific time you need to be open, tell us during the "
                  "walkthrough and it goes into the route order."),
            ("h2", "Seasonal contract or per event"),
            ("p", "A seasonal contract gives you a fixed cost for the winter and a spot in the priority "
                  "rotation, however the season goes. Per-event billing costs less in a mild winter and "
                  "more in a hard one. Commercial properties are usually better off on contract, and "
                  "residential can go either way."),
        ],
        "faqs": [
            ("What time will you get to me?",
             "Commercial and HOA properties are cleared first, so they're open for business hours. "
             "Residential drives are worked through after. During a large storm we run continuously and "
             "make repeat passes rather than waiting for it to stop."),
            ("Do you salt as well as plow?",
             "Yes. Ice management is available on walks, entries, and lots. It's priced separately, "
             "because not every property wants it on every event."),
            ("Do I need to sign up before it snows?",
             "Please do. Routes are built before the season starts, and being on the list ahead of time "
             "is the difference between guaranteed service and hoping we have room. Early fall is the "
             "right time to call."),
            ("What snow depth do you clear at?",
             "Two inches is standard, but we set it per property. Some commercial sites want a one-inch "
             "trigger because of foot traffic, and some residential drives are happy at three."),
        ],
        "needs_photos": True,
    },
    {
        "slug": "soft-washing",
        "name": "Soft Washing",
        "nav": "Soft Washing",
        "short": "Low-pressure cleaning for siding, roofs, and anything high pressure would damage.",
        "title": "Soft Washing for Siding & Roofs | Zionsville, IN",
        "desc": "Low-pressure soft washing for vinyl siding, roofs and painted exteriors in Whitestown "
                "and Zionsville, Indiana. Removes algae and streaking.",
        "hero": ("soft-washing", "soft-wash-siding-after"),
        "hero_alt": "Vinyl siding after soft washing, clean and streak-free",
        "lede": "That green film down the shaded side of your house is algae. Blasting it with pressure "
                "drives water behind the siding. Soft washing removes it properly.",
        "body": [
            ("h2", "What soft washing actually is"),
            ("p", "Soft washing uses low pressure, closer to a garden hose than a pressure washer, along "
                  "with cleaning solutions that break down the growth itself. The solution does the work, "
                  "not force."),
            ("p", "That matters, because the green and black staining on siding and roofs is alive. It's "
                  "algae, mildew, and lichen. Pressure knocks the surface layer off and it returns within "
                  "months. Treating it kills it at the root, so it stays gone far longer."),
            ("h2", "Where it's the right method"),
            ("ul", [
                "Vinyl, aluminum, and composite siding",
                "Roof shingles with black streaking or moss",
                "Painted wood, trim, and soffits",
                "Stucco, EIFS, and dryvit",
                "Screens, gutters, and fascia",
                "Fences and decks that would splinter under pressure",
            ]),
            ("h2", "Why not just use high pressure?"),
            ("p", "On siding, high pressure forces water up under the laps and into the wall, where it "
                  "has no fast way out. On shingles it strips the granules that protect the roof, which "
                  "shortens its life and can void a manufacturer's warranty. On painted wood it lifts the "
                  "finish."),
            ("p", "Anywhere the surface is soft, layered, or coated, pressure is the wrong tool. That "
                  "covers most of a house above the foundation."),
            ("h2", "Plants and pets"),
            ("p", "Solutions strong enough to kill algae aren't good for landscaping. We soak beds and "
                  "plantings before we start, keep them wet through the job, and rinse thoroughly "
                  "afterward. Keep pets inside while we work and until treated surfaces have been rinsed."),
        ],
        "beforeafter": [
            ("soft-washing", "soft-wash-siding-before", "soft-wash-siding-after",
             "Vinyl siding", "Years of algae on a shaded elevation, removed without pressure damage"),
        ],
        "gallery": [
            ("soft-washing", "soft-wash-siding-before", "Algae streaking on shaded vinyl siding"),
            ("soft-washing", "soft-wash-siding-after", "The same elevation after soft washing"),
        ],
        "faqs": [
            ("Will soft washing damage my siding or roof?",
             "No, and that's the whole reason the method exists. Pressure is what causes the damage. Soft "
             "washing runs at low pressure and lets the solution do the work, which is why shingle "
             "manufacturers point to it for roofs."),
            ("How long before the green comes back?",
             "Much longer than a pressure-washed surface, because the growth is killed rather than knocked "
             "off. On a shaded north wall under trees, expect a couple of years. A sunnier wall goes longer."),
            ("Do you clean roofs?",
             "Yes, and roofs are soft wash only. High pressure on shingles strips the protective granules "
             "and can void your warranty."),
        ],
    },
    {
        "slug": "pressure-washing",
        "name": "Pressure Washing",
        "nav": "Pressure Washing",
        "short": "Even, streak-free concrete, drives, and hardscape. No zebra stripes.",
        "title": "Pressure Washing Driveways & Concrete | Whitestown IN",
        "desc": "Pressure washing for driveways, sidewalks, patios and concrete in Whitestown, "
                "Zionsville and West Carmel, Indiana. Even, streak-free results.",
        "hero": ("pressure-washing", "driveway-pressure-washing-after"),
        "hero_alt": "Concrete driveway after pressure washing, clean and evenly finished",
        "lede": "Concrete collects grime so gradually that most people stop seeing it. Then half of it "
                "gets cleaned, and the difference is impossible to miss.",
        "body": [
            ("h2", "Surfaces we clean"),
            ("ul", [
                "Driveways, aprons, and parking pads",
                "Sidewalks, walkways, and front stoops",
                "Patios, pool decks, and hardscape",
                "Commercial entries, drive-throughs, and dumpster pads",
                "Retaining walls, steps, and curbing",
                "Metal awnings, canopies, and covered entries",
            ]),
            ("h2", "Why the equipment matters"),
            ("p", "A wand on its own leaves arcing stripes across concrete, the pattern people call zebra "
                  "striping. It happens because pressure and dwell time vary across every sweep."),
            ("p", "We use a rotating surface cleaner that holds a consistent distance and pressure across "
                  "its full width, and that's what produces an even finish. The wand comes out for edges, "
                  "corners, and detail work."),
            ("h2", "Stains and organic growth"),
            ("p", "Not everything on concrete comes off with pressure. Algae and mildew in shaded areas "
                  "need a treatment step. Rust, oil, and battery acid are chemical problems, not force "
                  "problems."),
            ("p", "We'll tell you up front what will lift and what won't. Some deep oil staining in older "
                  "concrete is permanent, and it's better to know that before we start than to be "
                  "disappointed after."),
        ],
        "beforeafter": [
            ("pressure-washing", "driveway-pressure-washing-before", "driveway-pressure-washing-after",
             "Concrete driveway", "The same driveway, the same morning: grey and stained, then even"),
            ("pressure-washing", "awning-pressure-washing-before", "awning-pressure-washing-after",
             "Metal awning", "Spotted and weather-stained metal brought back to white"),
        ],
        "gallery": [
            ("pressure-washing", "concrete-pressure-washing-in-progress", "Mid-wash: the line between cleaned and untouched concrete"),
            ("pressure-washing", "driveway-pressure-washing-before", "Driveway before washing"),
            ("pressure-washing", "driveway-pressure-washing-after", "The same driveway, finished"),
            ("pressure-washing", "awning-pressure-washing-before", "Metal awning before cleaning"),
            ("pressure-washing", "awning-pressure-washing-after", "Awning after cleaning"),
        ],
        "faqs": [
            ("How often should concrete be washed?",
             "Most drives and walks look best on a one to two year cycle. Shaded concrete under trees "
             "grows algae faster and often wants annual attention. Open, sunny concrete can go longer."),
            ("Will pressure washing damage my concrete?",
             "Not at the right pressure with the right tool. Damage happens when someone runs too much "
             "pressure too close with a narrow tip, which etches the surface and leaves permanent lines. "
             "Surface cleaners exist to prevent exactly that."),
            ("Can you get oil stains out?",
             "Often, but not always. Fresh oil usually lifts with a degreaser and hot water. Oil that has "
             "soaked into porous concrete for years has gone below the surface. We can lighten it a lot, "
             "but removing it completely may not be realistic. You'll get an honest read before we start."),
            ("Can you do pressure washing and soft washing on the same visit?",
             "Yes, and it's a common pairing. Soft wash the house, pressure wash the drive and walks, all "
             "in one day. Bundling the visit costs less than booking them separately."),
        ],
    },
]

AREAS = [
    {
        "slug": "whitestown",
        "name": "Whitestown",
        "full": "Whitestown, Indiana",
        "blurb": "Our home base. Whitestown has grown fast, and much of that growth is newer "
                 "subdivisions with HOA common areas and young landscaping.",
        "detail": [
            "Whitestown is where we're based. That means shorter drive times, easier scheduling, and "
            "the flexibility to swing back if something needs a second look.",
            "The building boom here left a lot of properties with landscaping installed to a budget and "
            "never developed past it. Thin mulch, bed lines that have blurred into the turf, shrubs that "
            "have never been shaped. All of that is fixable, usually in a single day.",
        ],
        "img": ("mulching", "hoa-entrance-mulch-harcourt-springs"),
        "img_alt": "HOA entrance landscaping maintained in Whitestown, Indiana",
        "highlights": ["HOA common areas and entrances", "New-construction landscape establishment",
                       "Commercial frontage along the 267 corridor", "Full winter snow routing"],
    },
    {
        "slug": "zionsville",
        "name": "Zionsville",
        "full": "Zionsville, Indiana",
        "blurb": "Mature trees, established landscaping, and a high standard. Zionsville lots mean "
                 "serious fall leaf volume and beds worth maintaining properly.",
        "detail": [
            "Zionsville properties are generally older and more heavily wooded than the newer "
            "developments nearby, and that changes the work. Mature oaks and maples mean leaf removal "
            "is a rotation through October and November, not a single visit.",
            "Established landscaping also rewards proper maintenance in a way new plantings can't yet. "
            "Beds cared for over years, with clean edges and correct mulch depth, are the difference "
            "between a property that looks maintained and one that looks expensive.",
        ],
        "img": ("mowing", "lawn-mowing-striped-residential"),
        "img_alt": "Striped residential lawn maintained in Zionsville, Indiana",
        "highlights": ["Weekly mowing with detail trim and edging", "Multi-visit fall leaf removal",
                       "Established bed and mulch maintenance", "Soft washing for shaded elevations"],
    },
    {
        "slug": "west-carmel",
        "name": "West Carmel",
        "full": "West Carmel, Indiana",
        "blurb": "Larger lots and higher expectations. West Carmel properties usually want the whole "
                 "package handled by one crew instead of four separate vendors.",
        "detail": [
            "West Carmel sits at the edge of our mowing territory, and it suits the way we work. These "
            "are larger properties where one company handling mowing, beds, washing, and snow beats "
            "coordinating between several.",
            "Bigger lots also mean the finish details carry more weight. On a large property, edges that "
            "wander and beds with soft lines read from the street immediately. That's why we treat "
            "edging and trim as part of every visit rather than an add-on.",
        ],
        "img": ("mulching", "mulch-install-front-entry"),
        "img_alt": "Front entry landscaping and mulch installation in West Carmel, Indiana",
        "highlights": ["Full-property programs under one crew", "Large-lot mowing and detail",
                       "Mulch, wash, and seasonal packages", "Priority winter service"],
    },
]

HOME_FAQS = [
    ("What areas do you serve?",
     "We mow in Whitestown, Zionsville, and West Carmel, which keeps our routes tight enough to hold a "
     "reliable day of the week. Everything else we do travels further across Boone County and the "
     "northwest side. If you're nearby but not in those three towns, it's still worth a call."),
    ("Do you work with HOAs and commercial properties?",
     "Yes, and it's a large part of what we do. We maintain HOA entrances, monument signs, and common "
     "areas, along with commercial frontage and municipal right-of-way work. Those run on contracts and "
     "scheduled rotations rather than one-off visits."),
    ("Can I get more than one service on the same visit?",
     "Usually that's the most cost-effective way to do it. Mulching alongside a spring cleanup, or soft "
     "washing the house the same day we pressure wash the drive, saves you a separate trip each time."),
    ("How do I get a quote?",
     "Call or text " + SITE["phone_display"] + ", send us an email, or fill in the form on this site. We "
     "can quote most work from a quick look at the property. Larger commercial and HOA properties usually "
     "need a walkthrough, so the scope is clear on both sides."),
    ("Are you insured?",
     "Yes. Certificates are available on request, which commercial and HOA clients typically need before "
     "work begins."),
]

PROCESS = [
    ("Tell us about the property",
     "Call, text, email, or use the form. Photos help. So does telling us what's been bothering you about "
     "the property, because that's usually what we should fix first."),
    ("We look, then we quote",
     "We can price most residential work quickly. Commercial, HOA, and municipal properties get a "
     "walkthrough, so the scope is written down and agreed before anyone starts."),
    ("You get a schedule, not a maybe",
     "Recurring work goes on a set day. One-time work gets a real date. If weather moves us, we tell you "
     "instead of leaving you wondering."),
    ("We do the whole job",
     "Edges, trim, and blow-off every visit, not just when there's time. If something isn't right, tell "
     "us and we'll come back."),
]

# Captions for images shown in the gallery but not owned by a single service page
# (commercial and municipal work spans mowing, mulching, and cleanups).
GALLERY_EXTRA = {
    "commercial-median-crew": "Crew maintaining a commercial median in live traffic",
    "commercial-median-landscape": "Ornamental grasses and rock along a divided roadway",
    "municipal-roadside-maintenance": "Municipal roadside bed maintenance",
    "commercial-median-shrub-beds": "Median shrub beds on a commercial corridor",
    "commercial-median-sunset": "Late-day median planting, trimmed and edged",
    "municipal-median-grasses": "Median grasses and stone on a municipal route",
    "fall-cleanup-truck-ladder": "Fall cleanup with truck and ladder on site",
    "leaf-covered-lawn": "Heavy leaf cover across a residential lawn before clearing",
    "mulch-bed-foundation": "Foundation bed edged and topped with fresh mulch",
    "mulch-install-front-entry": "Fresh mulch and trimmed shrubs at a front entry",
    "mulch-refresh-before": "Front bed before the mulch refresh",
    "mulch-refresh-after": "The same front bed after edging and fresh mulch",
    "soft-wash-siding-before": "Algae streaking on shaded vinyl siding before soft washing",
    "soft-wash-siding-after": "The same elevation after low-pressure soft washing",
    "driveway-pressure-washing-before": "Concrete driveway before pressure washing",
    "driveway-pressure-washing-after": "The same driveway after pressure washing",
    "awning-pressure-washing-before": "Weather-stained metal awning before cleaning",
    "awning-pressure-washing-after": "The same awning cleaned back to white",
}
