install python 3.x
pip install requirements.txt

py program.py


example usage:
I want change `relay state` of all meter on one `groundbolt` to `off` state, but *excluding* meters where `customer_name` or `address_street` contain `Streetlight` text.

- login

  > `l login `

- setup filter

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
  > Input new meter state with `off`/`on`/`auto` or key else to abort: off

