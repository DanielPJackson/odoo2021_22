# -*- coding: utf-8 -*-
from datetime import timedelta, datetime
from operator import pos
from odoo import models, fields, api
import random
import math




from odoo.exceptions import UserError


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
    quantity_survivors = fields.Integer(compute='_get_q_survivors')
    outposts = fields.Many2many('thewalkingdead.outpost',compute='_get_cities')
    def create_survivor(self):
        for p in self:
            template = random.choice(self.env['thewalkingdead.character_template'].search([]).mapped(lambda t: t.id))
            outpost = random.choice(self.env['thewalkingdead.outpost'].search([]).mapped(lambda t: t.id))
            survivor = self.env['thewalkingdead.survivor'].create({'player': p.id, 'template': template, 'outpost': outpost})



    @api.depends('survivors')
    def _get_cities(self):
        for p in self:
            p.outposts = p.survivors.outpost.ids


    @api.depends('survivors')
    def _get_q_survivors(self):
        for p in self:
            p.quantity_survivors = len(p.survivors)


class survivor(models.Model):
    _name = 'thewalkingdead.survivor'
    _description = 'Players'


    def _generate_name(self):
        first = ["Commander","Bullet","Crusty", "Imperator","Doof","Duff","Immortal","Big","Grease", "Junk", "Rusty"
                 "Gas","War","Feral","Blood","Lead","Max","Sprog","Smoke","Bum", "Wagon","Baron", "Leather", "Rotten"
                 "Salt","Slake","Nuke","Oil","Night","Water","Ass","Tank","Rig","People","Leaky","Nocturne", "Satanic"
                 "Dead", "Deadly", "Mike", "Mad","Smeg","Smeggy", "Jhonny","Unpredictable","Freakish","Snake","Praying"]
        second = ["Killer","Rider","Cutter","Guts","Eater","Warrior","Colossus","Blaster","Gunner", "Smith", "Doe"
                  "Farmer","Rock","Claw", "Boy", "Girl", "Driver","Ace","Quick","Blitzer", "Fury", "Roadster",
                  "Interceptor", "Bastich", "Thief", "Bleeder", "smeg","Ass","Face", "Mutant", "Anomaly", "Risk",
                  "Garcia", "Salamanca", "Goodman","Bum", "Sakura","Bleding Gums","Absent","Hybrid","Desire","Bubblegum"
                  ,"Serpente","Petal","Dust","Mantis","Preacher"]
        return random.choice(first)+" "+random.choice(second)




    def _generate_infection_state(self):

        return round(random.random())

    name = fields.Char(default=_generate_name)

    infected = fields.Integer(default=_generate_infection_state)

    zombie = fields.Float(default=0)
    player = fields.Many2one('thewalkingdead.player', ondelete='set null')
    outpost = fields.Many2one('thewalkingdead.outpost', ondelete='restrict')
    template = fields.Many2one('thewalkingdead.character_template', ondelete='restrict')
    avatar = fields.Image(max_width=200, max_height=400, related='template.image')
    state = fields.Selection(string="state", selection=[

        ('draft', 'Draft'),
        ('confirmar', 'Confirmado')

    ], required=False, default='draft')


    def btn_draft(self):
        self.state = 'draft'


    def btn_confirmar(self):
        self.state = 'confirmar'




class outpost(models.Model):
    _name = 'thewalkingdead.outpost'
    _description = 'outpost'
    def _generate_position(self):
        existent_outposts = self.search([])

        x = random.randint(-1000,1000)
        for e in existent_outposts:
            if e.position_x!=x:
                return x





    def _generate_name(self):
        first = ["Dark","chuck up","hopeful","hopeless","steel", "hard", "musky", "crusty", "rotton", "shining", "gloomy", "graceful", "silver"]
        second = ["hut", "city", "rock", "shire" ,"town", "forest", "cliff","point","clearing","district","club","horizon"]
        return random.choice(first)+" "+random.choice(second)
    name =  fields.Char(default=_generate_name)
    energy = fields.Float()
    oil = fields.Float()
    food = fields.Float()
    water = fields.Float()

    roads = fields.Many2many('thewalkingdead.roads', compute='_get_roads')
    players = fields.Many2many('thewalkingdead.player', compute='_get_players', string='Players with survivors')
    survivors = fields.One2many('thewalkingdead.survivor', 'player')

    position_x = fields.Integer(default=_generate_position)
    position_y = fields.Integer(default=_generate_position)

    @api.depends('survivors')
    def _get_players(self):
        for c in self:
            players = []
            for s in c.survivors:
                if s.player:
                    players.append(s.player.id)
            print(players)
            c.players = players


  

    def _get_roads(self):
        for c in self:
            c.roads = self.env['thewalkingdead.roads'].search(['|', ('outpost_1', '=', c.id), ('outpost_2', '=', c.id)]).ids


class building_type(models.Model):
    _name = 'thewalkingdead.building_type'
    _description = 'Building types'

    name = fields.Char()
    energy = fields.Float()
    oil = fields.Float()
    food = fields.Float()
    water = fields.Float()
    weapon_power = fields.Float()
    defense = fields.Float()
class roads(models.Model):
    _name = 'thewalkingdead.roads'
    _description = 'Roads beween outposts'


    name = fields.Char(compute='_get_name')
    outpost_1 = fields.Many2one('thewalkingdead.outpost', ondelete='cascade')
    outpost_2 = fields.Many2one('thewalkingdead.outpost', ondelete='cascade')
    distance = fields.Float(compute='_get_distance')

    @api.depends('outpost_1','outpost_2')
    def _get_distance(self):
        for r in self:
            r.distance = math.sqrt((r.outpost_1.position_x - r.outpost_1.position_x)**2 + (r.outpost_2.position_x - r.outpost_2.position_y)**2)



    @api.onchange('distance')
    def _get_name(self):
        for r in self:
            r.name = r.outpost_1.name," <--> ",r.outpost_2.name


class travel(models.Model):
    _name = 'thewalkingdead.travel'
    _description = 'journeys between outposts'

    name = fields.Char(default="journey")
    origin = fields.Many2one('thewalkingdead.outpost', ondelete='cascade')
    destiny = fields.Many2one('thewalkingdead.outpost', ondelete='cascade')
    roads = fields.Many2one('thewalkingdead.roads', ondelete='cascade')
    date_departure = fields.Datetime(default=lambda r: fields.datetime.now())
    date_end = fields.Datetime(compute='_get_progress')
    progress = fields.Float(compute='_get_progress')

#    @api.onchange('origin')
    def _onchange_origin(self):
        if self.origin != False:
            roads_available = self.origin.roads
            outposts_available = roads_available.outpost_1 + roads_available.outpost_2 - self.origin
            players_in_outpost = self.origin.players.ids
            print(outposts_available)
            return {
                'domain': {
                    'destiny': [('id', 'in', outposts_available.ids)],
                    'player': [('id', 'in', players_in_outpost)]
                }
            }

    @api.onchange('destiny')
    def _onchange_destiny(self):
        if self.destiny != False:
            roads_available = self.origin.roads & self.destiny.roads
            self.roads = roads_available.id
            return {}


    def launch_travel(self):
        for t in self:
            t.date_departure = fields.datetime.now()
            for p in t.passengers:
                p.outpost = False


    @api.depends('date_departure', 'roads')
    def _get_progress(self):
        for t in self:
            if t.roads:
                print(t.roads.distance)
                if t.date_departure:
                    d_dep = t.date_departure
                    data = fields.Datetime.from_string(d_dep)
                    data = data + timedelta(hours=t.roads.distance)
                    t.date_end = fields.Datetime.to_string(data)

                    time_remaining = fields.Datetime.context_timestamp(self, t.date_end) - fields.Datetime.context_timestamp(self, datetime.now())
                    time_remaining = time_remaining.total_seconds() / 60 / 60
                    t.progress = (1 - time_remaining / t.roads.distance) * 100
                    if t.progress >= 100:
                        t.progress = 100
                else:
                    t.progress = 0
                    t.date_end = False
            else:
                t.progress = 0
                t.date_end = False

    player = fields.Many2one('thewalkingdead.player')
    passengers = fields.Many2many('thewalkingdead.survivor')

class building(models.Model):
    _name = 'thewalkingdead.building'
    _description = 'Buildings'

    name = fields.Char()
    type = fields.Many2one('thewalkingdead.building_type')
    outpost = fields.Many2one('thewalkingdead.outpost')



class character_template(models.Model):
    _name = 'thewalkingdead.character_template'
    _description = 'Templates to generate characters'
    name = fields.Char()
    image = fields.Image(max_width=200, max_height=400)