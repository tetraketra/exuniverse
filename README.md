
# EXUniverse
The open-source custom card card API and battling website for Extinction Unleashed.

# Table of Contents
0. [Table of Contents](#table-of-contents) (you are here!)
1. [API Specification](#api-specification)

# API Specification
`GET https://exuniverse.net/user/register`
 - `username: str`: Unique username of the new user.
 - `password: str`: Plain password of the new user.
 - `email: str`: Unique email of the new user.
`GET https://exuniverse.net/cards`
 - `id: list[int]`: List of card ids to get. If included, other filters will be ignored.
 - `name: list[str]`: List of card names to get. If included, other filters will be ignored.
 - `treated_as: list[str]`: List of card treated-as names to get.
 - `effect_contains: list[str]`: List of strings to search card effects for. Defaults to "or" searching unless `effect_contains_all` is set to `True`.
 - `effect_contains_all: bool`: Toggles card effect search mode to "all" filtering (e.g. input ['foo', 'bar'] will match "foo bar" but not "foo"). Defaults to "or" (e.g. input ['foo', 'bar'] will match "foo bar", "foo", or "bar").
 - `ttype: list[str]`: List of template types to get (e.g. ['monster', 'spell']).
 - `tsubtype: list[str]`: List of template subtypes to get (e.g. ['fusion', 'continuous']).
 - `attribute_contains: list[str]`: List of attributes to get (e.g. ['dark', 'earth', 'water', 'wind']). Defaults to "or" searching unless `attribute_contains_all` is set to `True`.
 - `attribute_contains_all: bool`: Toggles card attributes search mode to "all" filtering (e.g. input ['dark', 'light'] will match "dark/light" but not "dark"). Defaults to "or" (e.g. input ['dark', 'light'] will match "dark/light", "dark", or "light").
 - `mon_atk: list[int]`: List of monster attacks to get.
 - `mon_atk_max: int`: Maximum monster attack to get.
 - `mon_atk_min: int`: Minimum monster attack to get.
 - `mon_def: list[int]`: List of monster defenses to get.
 - `mon_def_max: int`: Maximum monster defense to get.
 - `mon_def_min: int`: Minimum monster defense to get.
 - `mon_level: list[int]`: List of monster levels to get.
 - `mon_level_max: int`: Maximum monster level to get.
 - `mon_level_min: int`: Minimum monster level to get.
 - `pen_scale: list[int]`: List of pendulum scales to get.
 - `pen_effect_contains: list[str]`: List of strings to search pendulum effects for. Defaults to "or" searching unless `pen_effect_contains_all` is set to `True`.
 - `pen_effect_contains_all: bool`: Toggles card pendulum effect search mode to "all" filtering (e.g. input ['foo', 'bar'] will match "foo bar" but not "foo"). Defaults to "or" (e.g. input ['foo', 'bar'] will match "foo bar", "foo", or "bar").
 - `ocg: bool`: Include only cards in or out of the ocg.
 - `tcg: bool`: Include only cards in or out of the tcg.
 - `created_by_user_id: list[int]`: List of user ids to get cards created by.
 - `created_by_user_name: list[str]`: List of user names to get cards created by.

