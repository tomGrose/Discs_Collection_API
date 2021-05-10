# Discs Collection API

The Disc Collection is a free source for getting information about disc golf discs. Discs can be searched by name, speed, glide, and much more!

### There are 5 endpoints to retrieve information. Discs have 8 attributes.
1. Name
2. Plastic Type
3. Disc Type
4. Difficulty
5. Speed
6. Glide
7. Turn
8. Turn
9. Company Name


#### api/discs GET
Returns a list of all the discs currently in the database

#### api/discs/name GET
Since discs can have multiple variation of the same disc, or different turns and fades depending on the plastic, this search feature is used to return all discs that contain the search valu ein their name.
For example: {disc_name":"aviar"} would return the "aviar p & a", "aviar classic", "yeti pro aviar", and so on.
This can also be used to look up a disc if you are unsure of the exact spelling and only want to use part of the name.
For example: {"disc_name":"asher"} would return the "thrasher" disc.
If you want to retrieve discs exactly the way they are spelled then see api/discs/filter.

#### api/discs/filter GET
Returns discs based on filter parameters. Discs can be filtered by all 8 of their attributes.
- name: Exact spelling of a disc name. For example "boss"
- plastic: The name of the plastic type you want to return discs of. For example "champion"
- disc Type: "putter", "mid", "fairway", "driver"
- difficulty: Integer between and including 0 - 6
- speed: Integer between and including 1 - 14
- glide: Integer between and including 1 - 7
- turn: Integer between and including -5 - 1
- fade: Integer between and including 0 - 5
- company name: "innova", "latitude 64", etc.

#### api/companies GET
Returns a list of all the companies in the database.


