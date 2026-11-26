# Acme: one bet through the loop

Acme is an invented company (invoicing software for trades businesses). Every figure is illustrative.

`briefs/` holds the canonical landing briefs every skill's sample reads. The bet followed end to end is `quote-drafting`. Each skill renders its own sample from these briefs and writes its key into `landing/quote-drafting.json`; `tools/sample.py` runs them in loop order.
