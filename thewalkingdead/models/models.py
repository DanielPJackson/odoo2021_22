# -*- coding: utf-8 -*-

from operator import pos
from odoo import models, fields, api
import random
import math

class player(models.Model):
    _name = 'thewalkingdead.player'
    _description = 'Players'


    survivors = fields.One2many('thewalkingdead.survivor','player')

    name = fields.Char()
    energy = fields.Float()
    oil = fields.Float()
    food = fields.Float()
    water = fields.Float()
    infected = fields.Float()
    daysinfected = fields.Float()


class survivor(models.Model):
    _name = 'thewalkingdead.survivor'
    _description = 'Players'


    survivors = fields.One2many('thewalkingdead.survivor', 'player')
    def _generate_name(self):
        first = ["Commander","Bullet","Imperator","Doof","Duff","Immortal","Big","Grease", "Junk", "Rusty"
                 "Gas","War","Feral","Blood","Lead","Max","Sprog","Smoke","Wagon","Baron", "Leather", "Rotten"
                 "Salt","Slake","Nuke","Oil","Night","Water","Tank","Rig","People","Nocturne", "Satanic"
                 "Dead", "Deadly", "Mike", "Mad", "Jhonny","Unpredictable","Freakish","Snake","Praying"]
        second = ["Killer","Rider","Cutter","Guts","Eater","Warrior","Colossus","Blaster","Gunner", "Smith", "Doe"
                  "Farmer","Rock","Claw", "Boy", "Girl", "Driver","Ace","Quick","Blitzer", "Fury", "Roadster",
                  "Interceptor", "Bastich", "Thief", "Bleeder", "Face", "Mutant", "Anomaly", "Risk",
                  "Garcia", "Salamanca", "Goodman", "Sakura","Bleding Gums","Absent","Hybrid","Desire","Bubblegum"
                  ,"Serpente","Petal","Dust","Mantis","Preacher"]
        return random.choice(first)+" "+random.choice(second)

    name = fields.Char(default=_generate_name)
    name = fields.Char()
    infected = fields.Float()
    daysinfected = fields.Float()
    zombie = fields.Float()


class outpost(models.Model):
    _name = 'thewalkingdead.outpost'
    _description = 'outpost'

    name = fields.Char()
    energy = fields.Float()
    oil = fields.Float()
    food = fields.Float()
    water = fields.Float()

    buildings = fields.One2many('thewalkindead.building', 'outpost')
    survivors = fields.One2many('thewalkingdead.survivor', 'outpost')

    position_x = fields.Integer()
    position_y = fields.Integer()

    @api.model
    def action_generate_outposts(self):
        print('**************Generate')
        existent_outposts = self.search([])
        existent_outposts.unlink()
        board = [[0 for x in range(50)] for y in range(50)]
        new_outposts = self

        if len(existent_outposts) != -1:
            positions = [x for x in range(2500)]
            random.shuffle(positions)
            # print(positions)
            for i in range(0, 50):
                x = math.floor(positions[i] / 50)
                y = positions[i] % 50
                print(x, y)
                board[x][y] = 1
                new_outpost = self.create({
                    "energy": random.random() * 100,
                    "oil": random.random() * 100,
                    "food": random.random() * 100,
                    "water": random.random() * 100,
                    "position_x": x,
                    "position_y": y})
                new_outposts = new_outposts | new_outpost
            # for i in range(50):
            #    print(board[i])

            # Crear les carreteres
            # outposts_done = self
            # for c in new_outposts:
            #    outposts_done = outposts_done | c
            #    for c2 in new_outposts - outposts_done:
            #        self.env['negooutpost.road'].create({'outpost_1': c.id, 'outpost_2': c2.id})

            all_roads = False
            i = 1
            while all_roads == False:
                all_roads = True

                for c in new_outposts:
                    distancias = new_outposts.sorted(key=lambda r: math.sqrt(
                        (r.position_x - c.position_x) ** 2
                        + (r.position_y - c.position_y) ** 2)
                                                   )
                    # Si no exiteix previament una igual
                    if len(distancias) > i:
                        # print('i:',i)
                        if (len(self.env['thewalkingdead.road'].search(
                                [('outpost_1', '=', distancias[i].id), ('outpost_2', '=', c.id)])) == 0):
                            # print(self.env['negooutpost.road'].search([('outpost_2','=', distancias[i].id),('outpost_1','=', c.id)]))
                            if (len(self.env['thewalkingdead.road'].search(
                                    [('outpost_2', '=', distancias[i].id), ('outpost_1', '=', c.id)])) == 0):
                                # print('Mateixa',c.id)
                                # Si no té colisió
                                # https://stackoverflow.com/questions/3838329/how-can-i-check-if-two-segments-intersect
                                def ccw(A, B, C):
                                    return (C.position_y - A.position_y) * (B.position_x - A.position_x) > (
                                                B.position_y - A.position_y) * (C.position_x - A.position_x)

                                # Return true if line segments AB and CD intersect
                                def intersect(A, B, C, D):
                                    return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)

                                colisionen = self.env['thewalkingdead.road'].search([]).filtered(
                                    lambda r: intersect(r.outpost_1, r.outpost_2, c, distancias[i]))
                                if len(colisionen) == 0:
                                    self.env['thewalkingdead.road'].create(
                                        {'outpost_1': c.id, 'outpost_2': distancias[i].id})  # la primera és ella mateixa
                                    all_roads = False
                i = i + 1
                print(all_roads, i)


class building_type(models.Model):
    _name = 'thewalkingdead.building_type'
    _description = 'Building types'

    name = fields.Char()
    energy = fields.Float() # Pot ser positiu o negatiu i aumenta en el nivell
    oil = fields.Float()
    food = fields.Float()
    water = fields.Float()

class building(models.Model):
    _name = 'thewalkingdead.building'
    _description = 'Buildings'

    name = fields.Char()
    type = fields.Many2one('thewalkingdead.building_type')
    level = fields.Float(default=1) # Possible widget
    ruined = fields.Float(default=50) # 100% és ruina total i 0 està perfecte
    outpost = fields.Many2one('thewalkingdead.outpost')
