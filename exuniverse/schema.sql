-- version: 1.0

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS cards;
DROP TABLE IF EXISTS template_subtypes;
DROP TABLE IF EXISTS template_types;
DROP TABLE IF EXISTS template_attributes;
DROP TABLE IF EXISTS monster_types;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    password_salt TEXT NOT NULL,
    email TEXT NOT NULL,
    is_active BOOLEAN DEFAULT 0,
    profile_name TEXT, -- automatically defaults to username
    profile_about TEXT,
    profile_pic_link TEXT -- should default if not specified
);
CREATE TRIGGER users_default_profile_name_to_username
    AFTER INSERT ON users
    FOR EACH ROW
    WHEN NEW.profile_name IS NULL
    BEGIN
        UPDATE users SET profile_name = NEW.username WHERE rowid = NEW.rowid;
    END;

CREATE TABLE template_types (
    id INTEGER PRIMARY KEY, -- non-AUTOINCREMENT for easier viewing of template_types
    template_type TEXT NOT NULL
);
INSERT INTO template_types(id, template_type)
VALUES
    (0, 'Monster'),
    (1, 'Spell'),
    (2, 'Trap');

CREATE TABLE template_subtypes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    template_type_id INTEGER NOT NULL,
    template_subtype TEXT NOT NULL,
    FOREIGN KEY(template_type_id) REFERENCES template_types(id)
);
INSERT INTO template_subtypes(template_type_id, template_subtype)
VALUES
    (0, 'Normal'),
    (0, 'Effect'),
    (0, 'Ritual'),
    (0, 'Fusion'),
    (0, 'Synchro'),
    (0, 'Xyz'),
    (0, 'Pendulum'),
    (0, 'Link'),
    (0, 'Token'),
    (1, 'Normal'),
    (1, 'Continuous'),
    (1, 'Field'),
    (1, 'Equip'),
    (1, 'Quick-Spell'),
    (1, 'Ritual'),
    (2, 'Normal'),
    (2, 'Continuous'),
    (2, 'Counter');

CREATE TABLE template_attributes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    template_attribute TEXT
);
INSERT INTO template_attributes(template_attribute)
VALUES
    ('DARK'),
    ('LIGHT'),
    ('EARTH'),
    ('FIRE'),
    ('WIND'),
    ('WATER');

CREATE TABLE monster_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    monster_type TEXT
);
INSERT INTO monster_types(monster_type)
VALUES
    ('Aqua'),
    ('Beast'),
    ('Beast-Warrior'),
    ('Creator God'),
    ('Cyberse'),
    ('Dinosaur'),
    ('Divine-Beast'),
    ('Dragon'),
    ('Fairy'),
    ('Fiend'),
    ('Fish'),
    ('Insect'),
    ('Illusion'),
    ('Machine'),
    ('Machine'),
    ('Plant'),
    ('Psychic'),
    ('Pyro'),
    ('Reptile'),
    ('Rock'),
    ('Sea Serpent'),
    ('Spellcaster'),
    ('Thunder'),
    ('Warrior'),
    ('Winged Beast'),
    ('Wyrm'),
    ('Zombie');

CREATE TABLE cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT NOT NULL,
    treated_as TEXT, -- automatically defaults to name
    effect TEXT,
    pic TEXT NOT NULL, -- link to a 480x480 texture, defaults before specified

    template_type_id INTEGER NOT NULL,
    template_subtype_id INTEGER NOT NULL,
    template_attribute_id INTEGER,

    monster_atk INTEGER,
    monster_def INTEGER,
    monster_type_id INTEGER,
    monster_is_gemini BOOLEAN DEFAULT 0 NOT NULL,
    monster_is_spirit BOOLEAN DEFAULT 0 NOT NULL,
    monster_is_toon BOOLEAN DEFAULT 0 NOT NULL,
    monster_is_tuner BOOLEAN DEFAULT 0 NOT NULL,
    monster_is_union BOOLEAN DEFAULT 0 NOT NULL,
    monster_is_flip BOOLEAN DEFAULT 0 NOT NULL,

    pendulum_scale INTEGER,
    pendulum_effect TEXT,

    link_arrows TEXT -- like "01100111", read in clockwise spiral from top-left

    ocg BOOLEAN DEFAULT 0, -- y/n in ocg
    ocg_date TEXT,
    ocg_limit INTEGER,
    tcg BOOLEAN DEFAULT 0, -- y/n in tcg
    tcg_date TEXT,
    tcg_limit INTEGER,
    exu_limit INTEGER,

    created_by_id INTEGER NOT NULL,
    date_created DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, -- auto-gen!
    date_updated DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, -- auto-gen and auto-update!

    FOREIGN KEY(template_type_id) REFERENCES template_types(id),
    FOREIGN KEY(template_subtype_id) REFERENCES template_subtypes(id),
    FOREIGN KEY(template_attribute_id) REFERENCES template_attribute(id),
    FOREIGN KEY(monster_type_id) REFERENCES monster_types(id),
    FOREIGN KEY(created_by_id) REFERENCES users(id)
);
CREATE TRIGGER cards_default_treated_as_to_name
    AFTER INSERT ON cards
    FOR EACH ROW
    WHEN NEW.treated_as IS NULL
    BEGIN
        UPDATE cards SET treated_as = NEW.name WHERE rowid = NEW.rowid;
    END;
CREATE TRIGGER cards_update_date_updated
    AFTER UPDATE ON cards
    FOR EACH ROW
    BEGIN
        UPDATE cards SET date_updated = CURRENT_TIMESTAMP WHERE rowid = NEW.rowid;
    END;