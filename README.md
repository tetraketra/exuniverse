
# EXUniverse
The open-source custom card card API and battling website for Extinction Unleashed.

# Table of Contents
0. [Table of Contents](#table-of-contents) (you are here!)
1. [API Specification](#api-specification)
2. [Query Strings](#query-strings)

# API Specification
The following endpoints accept the following inputs in the request body as JSON:

`POST https://exuniverse.net/user/register`
 - `username: str`, required unique username of the new user.
 - `password: str`, required plain password of the new user.
 - `email: str`, required unique email of the new user.

`GET https://exuniverse.net/cards`
 - `id: list[int]`, list of card ids to get. If included, other filters will be ignored.
 - `name: list[str]`, list of card names to get. If included, other filters will be ignored.
 - `treated_as: list[str]`, list of card treated-as names to get. If included, other filters will be ignored.
 - `name_contains: str`, query string to search card names. See [Query Strings](#query-strings).
 - `treated_as_contains: str`, query string to search card treated-as names. See [Query Strings](#query-strings).
 - `effect_contains: str`, query string to search card effects. See [Query Strings](#query-strings).
 - `pen_effect_contains: str`, query string to search card pendulum effect. See [Query Strings](#query-strings).
 - `attributes_include: list[str]`, list of card attributes to include in the result (e.g. ['DARK', 'EARTH']).
 - `attributes_exclude: list[str]`, list of card attributes to exclude from the result (e.g. ['DARK', 'EARTH']).
 - `mon_abilities_include: list[str]`, list of card monster abilities to include in the result (e.g. ['FLIP', 'TUNER']).
 - `mon_abilities_exclude: list[str]`, list of card monster abilities to exclude from the result.
 - `mon_types_include: list[str]`, list of card monster types to include in the result.
 - `mon_types_exclude: list[str]`, list of card monster types to exclude from the result.
 - `t_type: list[str]`, list of card template types to get (e.g. ['Monster', 'Spell']).
 - `t_type_id: list[int]`, list of card template type ids to get (e.g. [1, 2]).
 - `t_subtype: list[str]`, list of card template subtypes to get (e.g. ['Fusion', 'Continuous']).
 - `t_subtype_id: list[int]`, list of card template subtype ids to get (e.g. [7, 8]).
 - `mon_atk: list[int]`, list of monster attacks to get (e.g. [100, 200, 4000]).
 - `mon_atk_max: int`, maximum monster attack to get. Inclusive (e.g. 4000).
 - `mon_atk_min: int`, minimum monster attack to get. Inclusive (e.g. 100).
 - `mon_atk_variadic: bool`, whether to include/exclude variadic ("?") attack cards. Defaults to `False`.
 - `mon_def: list[int]`, list of monster defenses to get (e.g. [100, 200, 4000]).
 - `mon_def_max: int`, maximum monster defense to get. Inclusive (e.g. 4000).
 - `mon_def_min: int`, minimum monster defense to get. Inclusive (e.g. 100).
 - `mon_def_variadic: bool`, whether to include/exclude variadic ("?") defense cards. Defaults to `False`.
 - `mon_level: list[int]`, list of monster levels to get (e.g. [1, 2, 10]).
 - `mon_level_max: int`, maximum monster level to get. Inclusive (e.g. 7).
 - `mon_level_min: int`, minimum monster level to get. Inclusive (e.g. 2).
 - `mon_level_not: bool`, makes `mon_level` exclusive rather than inclusive. Defaults to `False`.
 - `pen_scale: list[int]`, list of pendulum scales to get. If included, quivalent l/r filters will be ignored.
 - `pen_scale_max: int`, maximum pendulum scale to get. Inclusive. If included, quivalent l/r filters will be ignored.
 - `pen_scale_min: int`, minimum pendulum scale to get. Inclusive. If included, quivalent l/r filters will be ignored.
 - `pen_scale_l: list[int]`, list of pendulum scales (left) to get.
 - `pen_scale_l_max: int`, maximum pendulum scale (left) to get. Inclusive.
 - `pen_scale_l_min: int`, minimum pendulum scale (left) to get. Inclusive.
 - `pen_scale_r: list[int]`, list of pendulum scales (right) to get.
 - `pen_scale_r_max: int`, maximum pendulum scale (right) to get. Inclusive.
 - `pen_scale_r_min: int`, minimum pendulum scale (right) to get. Inclusive.
 - `# TODO (?): link_arrow_indices: list[int]`, list of link arrow indices to get (e.g. [0, 4] for up-left and/or down-right). You should use this in combination with `mon_level` to be more specific.
 - `# TODO (?): format: list[str]`, list of card formats the gotten card may be in. Defaults to "or" searching unless `format_contains_all` is set to `True`.
 - `# TODO (?): format_exact: bool`, toggles card format search mode to "exact" filtering (e.g. input ['ocg', 'exu'] will match cards *only in* OCG and EXU). Defaults to "or" filtering (e.g. input ['ocg', 'exu'] will match cards in either OCG or EXU).
 - `# TODO (?): created_by_user_id: list[int]`, list of user ids to get cards created by (e.g. [1, 2, 3]).
 - `# TODO (?): created_by_user_name: list[str]`, list of usernames to get cards created by (e.g. ['user1', 'user2', 'user3']).




# Query Strings
Query strings use square brackets `[]` to indicate text matching groups and
parentheses `()` to indicate logical condition groupings. For example:
`[FOO BAR]` `[FOO*BAR]` `[FOO**BAR]` `i[FOO**BAR]` `[FOO**BAR] & i[FOO*BAR]`
`[FOO*BAR] | !i[FOO**BAR]` `([FOO**BAR] & i[FOO*BAR]) | [BAR BASH]`
- `[` and `]` indicate text matching groups.
- `(` and `)` clarify logical condition groupings.
- `|` indicates logical or.
- `&` indicates logical and.
- `i` indicates case-insensitive matching for the following match group.
- `!` indicates negation for the following match group.
- `*` matches any number of characters between the left and right characters.
- `**` matches any number of characters between the left and right characters, excluding periods.
