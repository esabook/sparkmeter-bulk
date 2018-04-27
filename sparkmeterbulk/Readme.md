install python 3.x
pip install requirements.txt

py program.py

- intro
  > Welcome to 'SparkBulk' for set sparkmeter credit or else
  > 	type 'Help <topic>' for more help
  > 
  > 	1	Show setting (sparkmeter credentials)
  > 	2	Bulk Zeroing credit balance 	!!!for all meter on current setting!!!
  > 	3	Bulk Set custom credit balance	!!!for all meter on current setting!!!
  > 	4	Change meter state
  > 	5	Change meter tariff
  > 	6	Create payment to change meter credit
  > 	7	Bulk edit meter by file of `c` (new temp meter info)
  > 	8	Bulk menu
  > 
  > 	==========================================================================
  > 	l	Login
  > 	f	Set custom filter
  > 	g	Get meter based on custom filter (f) for current login session (l)
  > 	c	Compare current taken meters by (g) with csv (semicolon delimiters) file 
  > 	s	Setting
  > 	x	Exit


example usage:
I want change `relay state` of all meter on one `groundbolt` to `off` state, but *excluding* meters where `customer_name` or `address_street` contain `Streetlight` text.

- login

  > `l login `

- setup filter not contains specific keyword

  > `f set`
  >
  > "customer_name" : "!%" : "Streetlight"
  >
  > "address_street1" : "!%" :  "Streetlight"

  ... **3       save as  **...

  > `3`
  >
  > notStreetLight.json
  >
  > `f fn notStreetLight.json`

- get meter by filter

  > `g`

- set meter relay state to `off`

  > `4 `
  >
  > Input new meter state with `off`/`on`/`auto` or `key else to abort`: off

Reset meters where meter current state is on `protect` state
- Bulk
  > 8 reset-protect
  > select the site targets
  > i or *
- Single
  > l login
  > g
  > resetprotect SN-SM5R-0000000

