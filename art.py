import pygame as pg

TITLE = pg.image.load('Art\Title.jpeg').convert_alpha()
MENU = pg.image.load('Art\Menu.jpeg').convert_alpha()
NEW_GAME = pg.transform.scale2x(pg.image.load('Art\\New Game.jpeg').convert_alpha())
CONTINUE = pg.transform.scale2x(pg.image.load('Art\\Continue.jpeg').convert_alpha())
OPTIONS = pg.transform.scale2x(pg.image.load('Art\\Options.jpeg').convert_alpha())
NEW_SAVE = pg.image.load('Art\\New Save.jpeg').convert_alpha()
LOAD = pg.image.load('Art\Load.jpeg').convert_alpha()
LOAD_P1 = pg.image.load('Art\Load1.jpeg').convert_alpha()
LOAD_P2 = pg.image.load('Art\Load2.jpeg').convert_alpha()
LOAD_P3 = pg.image.load('Art\Load3.jpeg').convert_alpha()

JOIN_SPRITESHEET = pg.image.load('Art\Player-Sheet.png').convert_alpha()
BLOB_SPRITESHEET = pg.image.load('Art\Blob-Sheet.png').convert_alpha()
SKULLIE_SPRITESHEET = pg.image.load('Art\Skullie-Sheet.png').convert_alpha()
BOSS_SPRITESHEET = pg.image.load('Art\Boss-Sheet.png').convert_alpha()
EMPTY_SPRITESHEET = pg.image.load('Art\Empty-Sheet.png').convert_alpha()

POTION = pg.transform.scale2x(pg.image.load('Art\Potion.png').convert_alpha())

T001 = pg.image.load('Art\\001.jpeg').convert_alpha()
T002 = pg.image.load('Art\\002.jpeg').convert_alpha()
T003 = pg.image.load('Art\\003.jpeg').convert_alpha()
T004 = pg.image.load('Art\\004.jpeg').convert_alpha()
T005 = pg.image.load('Art\\005.jpeg').convert_alpha()
T006 = pg.image.load('Art\\006.jpeg').convert_alpha()
T007 = pg.image.load('Art\\007.jpeg').convert_alpha()
T008 = pg.image.load('Art\\008.jpeg').convert_alpha()
T009 = pg.image.load('Art\\009.jpeg').convert_alpha()

TILE_LIST = [EMPTY_SPRITESHEET, T001, T002, T003, T004, T005, T006, T007, T008, T009]