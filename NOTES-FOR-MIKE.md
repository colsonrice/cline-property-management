# Open questions for Mike

Everything here is either **on the site as a claim we can't verify**, or a **gap
we've worked around**. Grouped by how much it matters.

---

## 1. Must confirm — these are promises to customers

The site states these as fact. If any is wrong it needs changing before the site
is indexed, because HOA boards and property managers act on them.

| Claim on the site | Where | Question |
|---|---|---|
| "Certificates of insurance available on request" | About, Contact, Commercial section | Are you insured, and can you produce a COI on request? Property managers will ask for this before you set foot on site. |
| "Cleared automatically once snow reaches an agreed depth, commonly two inches" | Snow Removal | Is two inches your actual trigger? Different for commercial vs residential? |
| "Recurring work goes on a fixed day of the week" | About, Mowing | Do you actually hold a set day, or is it a rough weekly rotation? |
| "Our own crew does all of it" | Home, About | Any of the seven services subcontracted out? |
| "Free estimates on everything we do" | Contact, throughout | True for commercial and HOA walkthroughs as well? |
| "If something isn't right, tell us and we'll come back" | About | Happy to stand behind that in writing? |
| Fall cleanup "also handles gutters" | Spring & Fall Cleanups | Do you clear gutters? There's a photo of a truck and ladder at a roofline that suggests yes — confirm, because it's currently written as a service. |
| Municipal right-of-way and median work | Home, Mowing | Do you contract directly with municipalities, or is that work through a general contractor? |
| Snow: seasonal contract **or** per-event billing | Snow Removal | Do you offer both? |

---

## 2. Photos we still need

**Snow removal has zero photos.** It's the one service with no real imagery —
there's a drawn illustration standing in for it. Most useful, in order:

1. **Before / after of a single snowfall** — same driveway, snow-covered then
   cleared. This is the strongest possible shot and would slot straight into the
   existing drag-slider component.
2. A truck with the plow on, mid-push
3. A cleared commercial lot or HOA drive at dawn
4. Salted / treated walkway
5. Anything showing scale — a long private road, a big lot

**Also worth having:**

- **Mike himself, the crew, or a branded truck.** There is currently not a single
  photo of a person's face or a company vehicle. For a local trade business
  that's the single biggest trust gap after reviews.
- Winter or dormant-season shots generally — the year-round pitch is thin on
  December–February.

---

## 3. Reviews — biggest missing piece

There are **no testimonials or reviews anywhere on the site.** This was
deliberate: making them up would be inventing records for a real business. But
it's the largest credibility gap, and it matters twice over:

- Buyers of local services read reviews before they call.
- Google weighs review volume and recency heavily in local ranking.

**What's needed:** three to five real customers willing to be quoted by first
name and town ("Sarah M., Zionsville"). If there's a Google Business Profile with
reviews already, we can pull from there instead.

**Related:** does Cline have a **Google Business Profile**? If not, that is
probably higher value than anything left on this site. It's what puts him in the
map pack for "lawn mowing near me."

---

## 4. Business details not yet on the site

- **Domain name.** The site is on a borrowed URL and is deliberately hidden from
  Google until it moves. Nothing ranks until this is sorted.
- **Business hours.** Not stated anywhere. Worth adding if there are real ones.
- **Years in business / founded.** Would strengthen the About page.
- **Logo.** The current mark is one we generated. If there's a real logo, it
  should replace it.
- **Service radius is now confirmed.** The six non-mowing services cover the ten
  communities listed below.

---

## 5. Service area — confirmed, noting it here so it stays straight

- **Mowing:** Whitestown, Zionsville, **West Carmel** only.
- **The other six services:** Whitestown, Zionsville, Indianapolis, Carmel,
  Westfield, Brownsburg, Lebanon, Avon, Plainfield, and Fishers.

---

## 6. Turning the contact form on, and testing it

**Right now the form does not deliver.** It needs one activation click from
Mike, and until that happens every enquiry is silently discarded. The site is
live and indexable, so this is the one item that is actively costing money.

### The part that confuses everyone

The form posts to FormSubmit. **The first submission is consumed by activation** —
it does not arrive as an enquiry. Instead FormSubmit emails a confirmation link
to `Clinepropertymanagement@gmail.com`. So the sequence is:

1. Someone submits the form once. That submission is **not** delivered.
2. Mike gets an email from FormSubmit with a confirmation link, and clicks it.
3. From then on, submissions arrive normally.

If Mike submits once, sees nothing land, and concludes it is broken, he has
stopped exactly one step early. That is the failure mode to warn him about.

### The test, step by step

**Step 1 — activate.** Go to https://clinepropertymgmt.com/contact.html and
send a submission. Use real details so the result is easy to recognise.

**Step 2 — Mike checks his inbox** for a message from FormSubmit asking him to
confirm. **Check spam and the Promotions tab.** Automated senders land there
constantly. He clicks the link in that email. This is one time only.

**Step 3 — send a second submission.** This one should arrive as a proper
enquiry within a minute or two.

**Step 4 — check what arrived.** A working enquiry looks like:

- **Subject:** `[Cline Web] Lawn Mowing + Mulching · Zionsville — Dana Whitfield`
  The service and town are built from what the person actually ticked, so the
  subject alone says what and where before he opens it.
- **Body:** a table with name, phone, email, property type, address, services,
  message, and which page they were reading when they asked.
- **Reply-to:** the customer's own address. Hitting reply goes to them, not to
  FormSubmit. Worth having Mike actually test reply on this message.

### Make sure it never gets lost

In Gmail: **Settings → Filters → Create a new filter**, with `[Cline Web]` in
the *Has the words* box. Then tick **Never send it to Spam**, **Always mark as
important**, and apply a label like `Website enquiries`.

That single filter catches every submission, because the `[Cline Web]` tag is
on every one of them, including the plain-HTML fallback if JavaScript fails.

### Ongoing confidence

Worth submitting a test through the live form once a month, or before any
seasonal push. It is a free service with no delivery dashboard and no alert if
it stops working, so a silent failure would otherwise only surface as an
unexplained quiet spell.

