
# EXUniverse
The open-source custom card card API and battling website for Extinction Unleashed.

# Table of Contents
0. [Table of Contents](#table-of-contents) (you are here!)
1. [API Specification](#api-specification)

# API Specification
`GET https://exuniverse.net/user/register`
 - `username: str`, unique username of the new user.
 - `password: str`, plain password of the new user.
 - `email: str`, unique email of the new user.
`GET https://exuniverse.net/cards`
 - `id: list[int]`, list of card ids to get
 - `name: list[str]`, list of card names to get
 - `treated_as: list[str]`, list of card treated-as names to get.
 - `effect_contains: list[str]`, list of strings to search card effects for
 - `effect_contains_all: bool`, toggles card effect search mode to "all" filtering (e.g
 - `ttype: list[str]`, list of template types to get (e.g
 - `tsubtype: list[str]`, list of template subtypes to get (e.g
 - `attribute_contains: list[str]`, list of attributes to get (e.g
 - `attribute_contains_all: bool`, toggles card attributes search mode to "all" filtering (e.g
 - `mon_atk: list[int]`, list of monster attacks to get.
 - `mon_atk_max: int`, maximum monster attack to get.
 - `mon_atk_min: int`, minimum monster attack to get.
 - `mon_def: list[int]`, list of monster defenses to get.
 - `mon_def_max: int`, maximum monster defense to get.
 - `mon_def_min: int`, minimum monster defense to get.
 - `mon_level: list[int]`, list of monster levels to get.
 - `mon_level_max: int`, maximum monster level to get.
 - `mon_level_min: int`, minimum monster level to get.
 - `pen_scale: list[int]`, list of pendulum scales to get.
 - `pen_effect_contains: list[str]`, list of strings to search pendulum effects for
 - `pen_effect_contains_all: bool`, toggles card pendulum effect search mode to "all" filtering (e.g
 - `ocg: bool`, include only cards in or out of the ocg.
 - `tcg: bool`, include only cards in or out of the tcg.
 - `created_by_user_id: list[int]`, list of user ids to get cards created by.
 - `created_by_user_name: list[str]`, list of user names to get cards created by.

