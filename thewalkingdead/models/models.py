# -*- coding: utf-8 -*-
from datetime import timedelta, datetime
from operator import pos
from odoo import models, fields, api
import random
import math
from odoo.exceptions import ValidationError

from odoo.exceptions import UserError


class player(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    survivors = fields.One2many('thewalkingdead.survivor', 'player')
    is_player = fields.Boolean(default=False)
    energy = fields.Float()
    oil = fields.Float()
    food = fields.Float()
    water = fields.Float()
    premiumplayer = fields.Boolean(default=False)
    infected = fields.Float()
    daysinfected = fields.Float()
    quantity_survivors = fields.Integer(compute='_get_q_survivors')
    outposts = fields.Many2many('thewalkingdead.outpost', compute='_get_cities')
    coins = fields.Integer(default=10)

    def create_survivor(self):
        for p in self:
            template = random.choice(self.env['thewalkingdead.character_template'].search([]).mapped(lambda t: t.id))
            outpost = random.choice(self.env['thewalkingdead.outpost'].search([]).mapped(lambda t: t.id))
            survivor = self.env['thewalkingdead.survivor'].create(
                {'player': p.id, 'template': template, 'outpost': outpost})

    @api.depends('survivors')
    def _get_cities(self):
        for p in self:
            p.outposts = p.survivors.outpost.ids

    @api.depends('survivors')
    def _get_q_survivors(self):
        for p in self:
            p.quantity_survivors = len(p.survivors)

    def apply_coins(self, addcoin):
        for p in self:
            p.coins = p.coins + addcoin







class survivor(models.Model):
    _name = 'thewalkingdead.survivor'
    _description = 'Players'


    def revive(self):
        for s in self:
            if (s.infected==1):
                if (s.player.coins >=100):
                    s.infected=0
                    s.player.coins=s.player.coins-100
                else:
                    raise ValidationError('Not enough coins!')





    def _generate_name(self):
        first = ["Commander", "Bullet", "Crusty", "Imperator", "Doof", "Duff", "Immortal", "Big", "Grease", "Junk",
                 "Rusty"
                 "Gas", "War", "Feral", "Blood", "Lead", "Max", "Sprog", "Smoke", "Bum", "Wagon", "Baron", "Leather",
                 "Rotten"
                 "Salt", "Slake", "Nuke", "Oil", "Night", "Water", "Ass", "Tank", "Rig", "People", "Leaky", "Nocturne",
                 "Satanic"
                 "Dead", "Deadly", "Mike", "Mad", "Eggy", "Slick", "Johnny", "Unpredictable", "Freakish", "Snake",
                 "Praying"]
        second = ["Killer", "Rider", "Cutter", "Guts", "Eater", "Warrior", "Colossus", "Blaster", "Gunner", "Smith",
                  "Doe"
                  "Farmer", "Rock", "Claw", "Boy", "Girl", "Driver", "Ace", "Quick", "Blitzer", "Fury", "Roadster",
                  "Interceptor", "Bastich", "Cheerio", "Thief", "Bleeder", "Sausage", "Ass", "Face", "Mutant", "Anomaly", "Risk",
                  "Garcia", "Salamanca", "Goodman", "Bum", "Sakura", "Bleding Gums", "Absent", "Hybrid", "Desire",
                  "Bubblegum"
            , "Serpente", "Petal", "Dust", "Mantis", "Preacher"]
        return random.choice(first) + " " + random.choice(second)

    def _generate_infection_state(self):
        return round(random.random())

    name = fields.Char(default=_generate_name)

    infected = fields.Integer(default=_generate_infection_state)

    zombie = fields.Float(default=0)
    player = fields.Many2one('res.partner', ondelete='set null')
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

        x = random.randint(-1000, 1000)
        for e in existent_outposts:
            if e.position_x != x:
                return x

    def _generate_name(self):
        first = ["Dark", "chuck up", "hopeful", "hopeless", "steel", "hard", "musky", "crusty", "rotton", "shining",
                 "gloomy", "graceful", "silver"]
        second = ["hut", "city", "rock", "shire", "town", "forest", "cliff", "point", "clearing", "district", "club",
                  "horizon"]
        return random.choice(first) + " " + random.choice(second)

    name = fields.Char(default=_generate_name)
    energy = fields.Float()
    oil = fields.Float()
    food = fields.Float()
    water = fields.Float()

    roads = fields.Many2many('thewalkingdead.roads', compute='_get_roads')
    players = fields.Many2many('res.partner', compute='_get_players', string='Players with survivors')
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
            c.roads = self.env['thewalkingdead.roads'].search(
                ['|', ('outpost_1', '=', c.id), ('outpost_2', '=', c.id)]).ids


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

    @api.depends('outpost_1', 'outpost_2')
    def _get_distance(self):
        for r in self:
            r.distance = math.sqrt((r.outpost_1.position_x - r.outpost_1.position_x) ** 2 + (
                        r.outpost_2.position_x - r.outpost_2.position_y) ** 2)

    @api.onchange('distance')
    def _get_name(self):
        for r in self:
            r.name = r.outpost_1.name, " <--> ", r.outpost_2.name


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
    state = fields.Selection([('preparation', 'Preparation'), ('inprogress', 'In Progress'), ('finished', 'Finished')],
                             default='preparation')

    @api.onchange('destiny')
    def _onchange_destiny(self):
        if self.destiny != False:
            roads_available = self.origin.roads & self.destiny.roads
            self.roads = roads_available.id
            return {}

    def launch_travel(self):
        for t in self:
            t.date_departure = fields.datetime.now()
            t.state = 'inprogress'
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

                    time_remaining = fields.Datetime.context_timestamp(self,
                                                                       t.date_end) - fields.Datetime.context_timestamp(
                        self, datetime.now())
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

    @api.model
    def update_travel(self):
        travels_in_progress = self.search([('state', '=', 'inprogress')])
        print("Updating progress in: ", travels_in_progress)
        for t in travels_in_progress:
            if t.progress >= 100:
                t.state = 'finished'
                for p in t.passengers:
                    p.write({'outpost': t.destiny.id})
                self.env['thewalkingdead.event'].create(
                    {'name': 'Arrival travel ' + t.name, 'player': t.player,
                     'event': 'thewalkingdead.travel,' + str(t.id),
                     'description': 'Arrival travel... '})
                print('Arrived!')

    player = fields.Many2one('res.partner')
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


class event(models.Model):
    _name = 'thewalkingdead.event'
    _description = 'Events'

    name = fields.Char()
    player = fields.Many2many('res.partner')
    event = fields.Reference([('thewalkingdead.building', 'Building'), ('thewalkingdead.travel', 'Travel'),
                              ('res..partner', 'Player'), ('thewalkingdead.survivor', 'Survivor')])
    description = fields.Text()

    @api.model
    def clean_messages(self):
        yesterday = fields.Datetime.to_string(datetime.now() - timedelta(hours=24))
        old_messages = self.search([('creation_date', '<', yesterday)])
        old_messages.unlink()




class product_coins(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    coins = fields.Integer(default=100)




class sale_coins(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'



    def apply_coins(self):

        premium_products = self.order_line.filtered(lambda p: p.product_id.coins)
        for p in premium_products:
            self.partner_id.apply_coins(p.product_id.coins)

    def write(self,values):
        super(sale_coins,self).write(values)
        self.apply_coins()

    @api.model
    def create(self,values):
        record = super(sale_coins,self).create(values)
        record.apply_coins()
        return record

class RevCharacter(models.TransientModel):

    def _get_player(self):
        print(self.env['res.partner'].browse(self._context.get('active_id')))
        return self.env['res.partner'].browse(self._context.get('active_id'))
    def _get_survivors(self):
        print(self.env['res.partner'].browse(self._context.get('active_id')).survivors.ids)
        survivors= self.env['res.partner'].browse(self._context.get('active_id')).survivors
        survivors = survivors.filtered(lambda s:s.infected==1).ids
        return survivors
        #return self.origin.survivors.filtered(infected==1)

    _name = 'thewalkingdead.wizard_revive'
    player=fields.Many2one('res.partner', default=_get_player)
    survivors_dead =fields.Many2many('thewalkingdead.survivor', default=_get_survivors)
    coins = fields.Integer(related='player.coins')



class MakeAssistedCharacter(models.TransientModel):

    def _get_player(self):
        print(self.env['res.partner'].browse(self._context.get('active_id')))
        return self.env['res.partner'].browse(self._context.get('active_id'))
    def _get_survivors(self):
        print(self.env['res.partner'].browse(self._context.get('active_id')).survivors.ids)
        survivors= self.env['res.partner'].browse(self._context.get('active_id')).survivors
        survivors = survivors.filtered(lambda s:s.infected==1).ids
        return survivors
        #return self.origin.survivors.filtered(infected==1)

    def next(self):
        if (self.state=='1'):
            self.state='2'

        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }

    def previous(self):
        if (self.state == '2'):
            self.state = '1'

        return {
            'type' : 'ir.actions.act_window',
            'res_model' : self._name,
            'res_id' : self.id,
            'view_mode' : 'form',
            'target' : 'new',
        }





    _name = 'thewalkingdead.wizard_create'
    player=fields.Many2one('res.partner', default=_get_player)
    survivors_dead =fields.Many2many('thewalkingdead.survivor', default=_get_survivors)
    coins = fields.Integer(related='player.coins')
    state = fields.Selection([('1','survivor info'),('2','starting resources')],default='1')

    name = fields.Char()
    outpost = fields.Many2one('thewalkingdead.outpost', ondelete='restrict')





    def create_survivor(self):
        print (self.name)
        survivor = self.env['thewalkingdead.survivor'].create({
                                                                'player' : self.player.id,
                                                                'name': self.name,
                                                                'outpost': self.outpost.id,
                                                                        })


