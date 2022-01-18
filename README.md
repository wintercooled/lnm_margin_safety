# LNM Margin Safety
Adds margin to an LNM position until it is within safety limits.

You must ensure you have enough balance to cover margin additions within your LMN account first before running.

Before running amend:

`SAFETY_MARGIN`

`MARGIN_ADD_AMOUNT`

`KEY`

`SECRET`

`PASSPHRASE`

Example:

If the price (bid) is at $40000 and your open long position margin calls at $39000 and
you want to add margin until margin call drops to $38000 then set `SAFETY_MARGIN` to 2000
and run the script.
