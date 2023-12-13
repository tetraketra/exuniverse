
# EXUniverse
The open-source custom card card API and battling website for Extinction Unleashed.

# Table of Contents
0. [Table of Contents](#table-of-contents) (you are here!)
1. [API Specification](#api-specification)

# API Specification
The following endpoints accept the following inputs in the request body as JSON:
`POST https://exuniverse.net/user/register`
 - `username: str`, required unique username of the new user.
 - `password: str`, required plain password of the new user.
 - `email: str`, required unique email of the new user.

`GET https://exuniverse.net/cards`
 - `id: list[int]`, list of card ids to get. If included, other filters will be ignored.
 - `name: list[str]`, list of card names to get.
 - `name_contains: list[str]`, list of strings to search card names for. Defaults to "or" searching unless `name_contains_all` is set to `True`.
 - `name_contains_all: bool`, toggles card name search mode to "sequence" filtering (e.g. input ['foo', 'bar', 'bash'] will match "foo ... bar ... bash" but not "foo. bar bash", where "..." represents any run of characters that does not contain a period). Defaults to "disconnected" filtering. (e.g. input ['foo', 'bar'] will match "foo bar", "foo. bar", "foo", or "bar").
 - `name_contains_sequence: bool`, toggles card name search mode to "sequence" filtering (e.g. input ['foo', 'bar', 'bash'] will match "foo ... bar ... bash" but not "foo. bar bash", where "..." represents any run of characters that does not contain a period). Defaults to "disconnected" filtering. (e.g. input ['foo', 'bar'] will match "foo bar", "foo. bar", "foo", or "bar").
 - `name_contains_not: bool`, toggles card name searching to exclude any/all in `name_contains` (depending on `name_contains_all`).
 - `treated_as: list[str]`, list of card treated-as names to get.
 - `effect_contains: list[str]`, list of strings to search card effects for. Defaults to "or" searching unless `effect_contains_all` is set to `True`.
 - `effect_contains_all: bool`, toggles card effect search mode to "all" filtering (e.g. input ['foo', 'bar'] will match "foo bar" but not "foo"). Defaults to "or" filtering (e.g. input ['foo', 'bar'] will match "foo bar", "foo", or "bar").
 - `effect_contains_sequence: bool`, toggles card effect search mode to "sequence" filtering (e.g. input ['foo', 'bar', 'bash'] will match "foo ... bar ... bash" but not "foo. bar bash", where "..." represents any run of characters that does not contain a period). Defaults to "disconnected" filtering. (e.g. input ['foo', 'bar'] will match "foo bar", "foo. bar", "foo", or "bar").
 - `effect_contains_not: bool`, toggles card effect searching to exclude any/all in `effect_contains` (depending on `effect_contains_all`).
 - `ttype: list[str]`, list of template types to get (e.g. ['monster', 'spell']).
 - `tsubtype: list[str]`, list of template subtypes to get (e.g. ['fusion', 'continuous']).
 - `attribute_contains: list[str]`, list of attributes to get (e.g. ['dark', 'earth', 'water', 'wind']). Defaults to "or" searching unless `attribute_contains_all` is set to `True`.
 - `attribute_contains_all: bool`, toggles card attributes search mode to "all" filtering (e.g. input ['dark', 'light'] will match "dark/light" but not "dark"). Defaults to "or" filtering (e.g. input ['dark', 'light'] will match "dark/light", "dark", or "light").
 - `attribute_contains_not: bool`, toggles card attributes searching to exclude any/all in `attribute_contains` (depending on `attribute_contains_all`).
 - `mon_atk: list[int]`, list of monster attacks to get.
 - `mon_atk_max: int`, maximum monster attack to get. Inclusive.
 - `mon_atk_min: int`, minimum monster attack to get. Inclusive.
 - `mon_atk_include_variadic: bool`, specifies monster defense searching to include/exclude variadic ("?") attack cards.
 - `mon_def: list[int]`, list of monster defenses to get.
 - `mon_def_max: int`, maximum monster defense to get. Inclusive.
 - `mon_def_min: int`, minimum monster defense to get. Inclusive.
 - `mon_def_include_variadic: bool`, specifies monster defense searching to include/exclude variadic ("?") defense cards.
 - `mon_level: list[int]`, list of monster levels to get (e.g. [1, 2, 10]).
 - `mon_level_max: int`, maximum monster level to get. Inclusive.
 - `mon_level_min: int`, minimum monster level to get. Inclusive.
 - `mon_level_not: bool`, toggles monster level searching to exclude all in `mon_level`.
 - `pen_scale: list[int]`, list of pendulum scales to get.
 - `pen_scale_max: int`, maximum pendulum scale to get. Inclusive.
 - `pen_scale_min: int`, minimum pendulum scale to get. Inclusive.
 - `pen_effect_contains: list[str]`, list of strings to search pendulum effects for. Defaults to "or" searching unless `pen_effect_contains_all` is set to `True`.
 - `pen_effect_contains_all: bool`, toggles card pendulum effect search mode to "all" filtering (e.g. input ['foo', 'bar'] will match "foo bar" but not "foo"). Defaults to "or" filtering (e.g. input ['foo', 'bar'] will match "foo bar", "foo", or "bar").
 - `pen_effect_contains_sequence: bool`, toggles card pendulum effect search mode to "sequence" filtering (e.g. input ['foo', 'bar'] will match "foo ... bar" but not "foo. bar.", where "..." represents any run of characters that does not contain a period). Defaults to "disconnected" filtering. (e.g. input ['foo', 'bar'] will match "foo bar", "foo. bar", "foo", or "bar").
 - `pen_effect_contains_not: bool`, toggles card pendulum effect searching to exclude any/all in `pen_effect_contains` (depending on `pen_effect_contains_all`).
 - `link_arrow_indices: list[int]`, list of link arrow indices to get (e.g. [0, 4] for up-left and/or down-right). You should use this in combination with `mon_level` to be more specific.
 - `format: list[str]`, list of card formats the gotten card may be in. Defaults to "or" searching unless `format_contains_all` is set to `True`.
 - `format_exact: bool`, toggles card format search mode to "exact" filtering (e.g. input ['ocg', 'exu'] will match cards *only in* OCG and EXU). Defaults to "or" filtering (e.g. input ['ocg', 'exu'] will match cards in either OCG or EXU).
 - `created_by_user_id: list[int]`, list of user ids to get cards created by.
 - `created_by_user_name: list[str]`, list of user names to get cards created by.


