#!/usr/bin/env python
# encoding: utf-8
# Généré par Mocodo 2.3.8 le Fri, 21 Aug 2020 19:00:08

from __future__ import division
from math import hypot

import time, codecs

(width,height) = (627,376)
cx = {
    u"Administrateur":  268,
    u"Inscrire"      :  423,
    u"Définir"       :   53,
    u"Créer"         :  159,
    u"Ajouter"       :  268,
    u"Élève"         :  423,
    u"Professeur"    :  556,
    u"Discipline"    :  423,
    u"Affecter"      :  556,
    u"Période"       :   53,
    u"Classe"        :  423,
}
cy = {
    u"Administrateur":   38,
    u"Inscrire"      :   38,
    u"Définir"       :  146,
    u"Créer"         :  146,
    u"Ajouter"       :  146,
    u"Élève"         :  146,
    u"Professeur"    :  146,
    u"Discipline"    :  263,
    u"Affecter"      :  263,
    u"Période"       :  346,
    u"Classe"        :  346,
}
shift = {
    u"Inscrire,Administrateur,-1.0":    0,
    u"Inscrire,Administrateur,1.0" :    0,
    u"Inscrire,Professeur"         :    0,
    u"Inscrire,Élève"              :    0,
    u"Définir,Période"             :    0,
    u"Définir,Administrateur"      :    0,
    u"Créer,Classe"                :    0,
    u"Créer,Administrateur"        :    0,
    u"Ajouter,Discipline"          :    0,
    u"Ajouter,Administrateur"      :    0,
    u"Affecter,Professeur"         :    0,
    u"Affecter,Discipline"         :    0,
    u"Affecter,Classe"             :    0,
    u"Affecter,Élève"              :    0,
}
colors = {
    u"annotation_color"                : '#b35806',
    u"annotation_text_color"           : '#f7f7f7',
    u"association_attribute_text_color": '#000000',
    u"association_cartouche_color"     : '#fdb863',
    u"association_cartouche_text_color": '#000000',
    u"association_color"               : '#fee0b6',
    u"association_stroke_color"        : '#e08214',
    u"background_color"                : '#f7f7f7',
    u"card_text_color"                 : '#542788',
    u"entity_attribute_text_color"     : '#000000',
    u"entity_cartouche_color"          : '#b2abd2',
    u"entity_cartouche_text_color"     : '#000000',
    u"entity_color"                    : '#d8daeb',
    u"entity_stroke_color"             : '#8073ac',
    u"leg_stroke_color"                : '#e08214',
    u"transparent_color"               : 'none',
}
card_max_width = 19
card_max_height = 14
card_margin = 5
arrow_width = 12
arrow_half_height = 6
arrow_axis = 8
card_baseline = 3

def cmp(x, y):
    return (x > y) - (x < y)

def offset(x, y):
    return (x + card_margin, y - card_baseline - card_margin)

def line_intersection(ex, ey, w, h, ax, ay):
    if ax == ex:
        return (ax, ey + cmp(ay, ey) * h)
    if ay == ey:
        return (ex + cmp(ax, ex) * w, ay)
    x = ex + cmp(ax, ex) * w
    y = ey + (ay-ey) * (x-ex) / (ax-ex)
    if abs(y-ey) > h:
        y = ey + cmp(ay, ey) * h
        x = ex + (ax-ex) * (y-ey) / (ay-ey)
    return (x, y)

def straight_leg_factory(ex, ey, ew, eh, ax, ay, aw, ah, cw, ch):
    
    def card_pos(twist, shift):
        compare = (lambda x1_y1: x1_y1[0] < x1_y1[1]) if twist else (lambda x1_y1: x1_y1[0] <= x1_y1[1])
        diagonal = hypot(ax-ex, ay-ey)
        correction = card_margin * 1.4142 * (1 - abs(abs(ax-ex) - abs(ay-ey)) / diagonal) - shift
        (xg, yg) = line_intersection(ex, ey, ew, eh + ch, ax, ay)
        (xb, yb) = line_intersection(ex, ey, ew + cw, eh, ax, ay)
        if compare((xg, xb)):
            if compare((xg, ex)):
                if compare((yb, ey)):
                    return (xb - correction, yb)
                return (xb - correction, yb + ch)
            if compare((yb, ey)):
                return (xg, yg + ch - correction)
            return (xg, yg + correction)
        if compare((xb, ex)):
            if compare((yb, ey)):
                return (xg - cw, yg + ch - correction)
            return (xg - cw, yg + correction)
        if compare((yb, ey)):
            return (xb - cw + correction, yb)
        return (xb - cw + correction, yb + ch)
    
    def arrow_pos(direction, ratio):
        (x0, y0) = line_intersection(ex, ey, ew, eh, ax, ay)
        (x1, y1) = line_intersection(ax, ay, aw, ah, ex, ey)
        if direction == "<":
            (x0, y0, x1, y1) = (x1, y1, x0, y0)
        (x, y) = (ratio * x0 + (1 - ratio) * x1, ratio * y0 + (1 - ratio) * y1)
        return (x, y, x1 - x0, y0 - y1)
    
    straight_leg_factory.card_pos = card_pos
    straight_leg_factory.arrow_pos = arrow_pos
    return straight_leg_factory


def curved_leg_factory(ex, ey, ew, eh, ax, ay, aw, ah, cw, ch, spin):
    
    def bisection(predicate):
        (a, b) = (0, 1)
        while abs(b - a) > 0.0001:
            m = (a + b) / 2
            if predicate(bezier(m)):
                a = m
            else:
                b = m
        return m
    
    def intersection(left, top, right, bottom):
       (x, y) = bezier(bisection(lambda p: left <= p[0] <= right and top <= p[1] <= bottom))
       return (int(round(x)), int(round(y)))
    
    def card_pos(shift):
        diagonal = hypot(ax-ex, ay-ey)
        correction = card_margin * 1.4142 * (1 - abs(abs(ax-ex) - abs(ay-ey)) / diagonal)
        (top, bot) = (ey - eh, ey + eh)
        (TOP, BOT) = (top - ch, bot + ch)
        (lef, rig) = (ex - ew, ex + ew)
        (LEF, RIG) = (lef - cw, rig + cw)
        (xr, yr) = intersection(LEF, TOP, RIG, BOT)
        (xg, yg) = intersection(lef, TOP, rig, BOT)
        (xb, yb) = intersection(LEF, top, RIG, bot)
        if spin > 0:
            if (yr == BOT and xr <= rig) or (xr == LEF and yr >= bot):
                return (max(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y >= bot) - correction + shift, bot + ch)
            if (xr == RIG and yr >= top) or yr == BOT:
                return (rig, min(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x >= rig) + correction + shift)
            if (yr == TOP and xr >= lef) or xr == RIG:
                return (min(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y <= top) + correction + shift - cw, TOP + ch)
            return (LEF, max(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x <= lef) - correction + shift + ch)
        if (yr == BOT and xr >= lef) or (xr == RIG and yr >= bot):
            return (min(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y >= bot) + correction + shift - cw, bot + ch)
        if xr == RIG or (yr == TOP and xr >= rig):
            return (rig, max(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x >= rig) - correction + shift + ch)
        if yr == TOP or (xr == LEF and yr <= top):
            return (max(x for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if y <= top) - correction + shift, TOP + ch)
        return (LEF, min(y for (x, y) in ((xr, yr), (xg, yg), (xb, yb)) if x <= lef) + correction + shift)
    
    def arrow_pos(direction, ratio):
        t0 = bisection(lambda p: abs(p[0] - ax) > aw or abs(p[1] - ay) > ah)
        t3 = bisection(lambda p: abs(p[0] - ex) < ew and abs(p[1] - ey) < eh)
        if direction == "<":
            (t0, t3) = (t3, t0)
        tc = t0 + (t3 - t0) * ratio
        (xc, yc) = bezier(tc)
        (x, y) = derivate(tc)
        if direction == "<":
            (x, y) = (-x, -y)
        return (xc, yc, x, -y)
    
    diagonal = hypot(ax - ex, ay - ey)
    (x, y) = line_intersection(ex, ey, ew + cw / 2, eh + ch / 2, ax, ay)
    k = (cw *  abs((ay - ey) / diagonal) + ch * abs((ax - ex) / diagonal))
    (x, y) = (x - spin * k * (ay - ey) / diagonal, y + spin * k * (ax - ex) / diagonal)
    (hx, hy) = (2 * x - (ex + ax) / 2, 2 * y - (ey + ay) / 2)
    (x1, y1) = (ex + (hx - ex) * 2 / 3, ey + (hy - ey) * 2 / 3)
    (x2, y2) = (ax + (hx - ax) * 2 / 3, ay + (hy - ay) * 2 / 3)
    (kax, kay) = (ex - 2 * hx + ax, ey - 2 * hy + ay)
    (kbx, kby) = (2 * hx - 2 * ex, 2 * hy - 2 * ey)
    bezier = lambda t: (kax*t*t + kbx*t + ex, kay*t*t + kby*t + ey)
    derivate = lambda t: (2*kax*t + kbx, 2*kay*t + kby)
    
    curved_leg_factory.points = (ex, ey, x1, y1, x2, y2, ax, ay)
    curved_leg_factory.card_pos = card_pos
    curved_leg_factory.arrow_pos = arrow_pos
    return curved_leg_factory


def upper_round_rect(x, y, w, h, r):
    return " ".join([str(x) for x in ["M", x + w - r, y, "a", r, r, 90, 0, 1, r, r, "V", y + h, "h", -w, "V", y + r, "a", r, r, 90, 0, 1, r, -r]])

def lower_round_rect(x, y, w, h, r):
    return " ".join([str(x) for x in ["M", x + w, y, "v", h - r, "a", r, r, 90, 0, 1, -r, r, "H", x + r, "a", r, r, 90, 0, 1, -r, -r, "V", y, "H", w]])

def arrow(x, y, a, b):
    c = hypot(a, b)
    (cos, sin) = (a / c, b / c)
    return " ".join([str(x) for x in [ "M", x, y, "L", x + arrow_width * cos - arrow_half_height * sin, y - arrow_half_height * cos - arrow_width * sin, "L", x + arrow_axis * cos, y - arrow_axis * sin, "L", x + arrow_width * cos + arrow_half_height * sin, y + arrow_half_height * cos - arrow_width * sin, "Z"]])

def safe_print_for_PHP(s):
    try:
        print(s)
    except UnicodeEncodeError:
        print(s.encode("utf8"))


lines = '<?xml version="1.0" standalone="no"?>\n<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"\n"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">'
lines += '\n\n<svg width="%s" height="%s" view_box="0 0 %s %s"\nxmlns="http://www.w3.org/2000/svg"\nxmlns:link="http://www.w3.org/1999/xlink">' % (width,height,width,height)
lines += u'\\n\\n<desc>Généré par Mocodo 2.3.8 le %s</desc>' % time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
lines += '\n\n<rect id="frame" x="0" y="0" width="%s" height="%s" fill="%s" stroke="none" stroke-width="0"/>' % (width,height,colors['background_color'] if colors['background_color'] else "none")

lines += u"""\n\n<!-- Association Inscrire -->"""
(x,y) = (cx[u"Inscrire"],cy[u"Inscrire"])
(ex,ey) = (cx[u"Administrateur"],cy[u"Administrateur"])
leg=curved_leg_factory(ex,ey,80,21,x,y,46,29,19+2*card_margin,14+2*card_margin,-1.0)
(x0, y0, x1, y1, x2, y2, x3, y3)=leg.points
lines += u"""\n<path d="M%(x0)s %(y0)s C %(x1)s %(y1)s %(x2)s %(y2)s %(x3)s %(y3)s" fill="none" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': x0, 'y0': y0, 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'x3': x3, 'y3': y3, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(shift[u"Inscrire,Administrateur,-1.0"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Futura" font-size="11">1,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
(ex,ey) = (cx[u"Administrateur"],cy[u"Administrateur"])
leg=curved_leg_factory(ex,ey,80,21,x,y,46,29,18+2*card_margin,14+2*card_margin,1.0)
(x0, y0, x1, y1, x2, y2, x3, y3)=leg.points
lines += u"""\n<path d="M%(x0)s %(y0)s C %(x1)s %(y1)s %(x2)s %(y2)s %(x3)s %(y3)s" fill="none" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': x0, 'y0': y0, 'x1': x1, 'y1': y1, 'x2': x2, 'y2': y2, 'x3': x3, 'y3': y3, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(shift[u"Inscrire,Administrateur,1.0"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Futura" font-size="11">1,1</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
(ex,ey) = (cx[u"Professeur"],cy[u"Professeur"])
leg=straight_leg_factory(ex,ey,62,55,x,y,46,29,18+2*card_margin,14+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"Inscrire,Professeur"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Futura" font-size="11">1,1</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
(ex,ey) = (cx[u"Élève"],cy[u"Élève"])
leg=straight_leg_factory(ex,ey,35,21,x,y,46,29,18+2*card_margin,14+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"Inscrire,Élève"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Futura" font-size="11">1,1</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
lines += u"""\n<g id="association-Inscrire">""" % {}
path = upper_round_rect(-46+x,-29+y,92,28,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_cartouche_color'], 'stroke_color': colors['association_cartouche_color']}
path = lower_round_rect(-46+x,-1.0+y,92,30,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_color'], 'stroke_color': colors['association_color']}
lines += u"""\n	<rect x="%(x)s" y="%(y)s" width="92" height="58" fill="%(color)s" rx="14" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -46+x, 'y': -29+y, 'color': colors['transparent_color'], 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x0': -46+x, 'y0': -1+y, 'x1': 46+x, 'y1': -1+y, 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Copperplate" font-size="18">Inscrire</text>""" % {'x': -39+x, 'y': -7.7+y, 'text_color': colors['association_cartouche_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Association Définir -->"""
(x,y) = (cx[u"Définir"],cy[u"Définir"])
(ex,ey) = (cx[u"Période"],cy[u"Période"])
leg=straight_leg_factory(ex,ey,44,21,x,y,42,29,18+2*card_margin,14+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"Définir,Période"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Futura" font-size="11">1,1</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
(ex,ey) = (cx[u"Administrateur"],cy[u"Administrateur"])
leg=straight_leg_factory(ex,ey,80,21,x,y,42,29,19+2*card_margin,14+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"Définir,Administrateur"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Futura" font-size="11">1,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
lines += u"""\n<g id="association-Définir">""" % {}
path = upper_round_rect(-42+x,-29+y,84,28,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_cartouche_color'], 'stroke_color': colors['association_cartouche_color']}
path = lower_round_rect(-42+x,-1.0+y,84,30,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_color'], 'stroke_color': colors['association_color']}
lines += u"""\n	<rect x="%(x)s" y="%(y)s" width="84" height="58" fill="%(color)s" rx="14" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -42+x, 'y': -29+y, 'color': colors['transparent_color'], 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x0': -42+x, 'y0': -1+y, 'x1': 42+x, 'y1': -1+y, 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Copperplate" font-size="18">Définir</text>""" % {'x': -35+x, 'y': -7.7+y, 'text_color': colors['association_cartouche_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Association Créer -->"""
(x,y) = (cx[u"Créer"],cy[u"Créer"])
(ex,ey) = (cx[u"Classe"],cy[u"Classe"])
leg=straight_leg_factory(ex,ey,40,21,x,y,35,29,18+2*card_margin,14+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"Créer,Classe"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Futura" font-size="11">1,1</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
(ex,ey) = (cx[u"Administrateur"],cy[u"Administrateur"])
leg=straight_leg_factory(ex,ey,80,21,x,y,35,29,19+2*card_margin,14+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"Créer,Administrateur"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Futura" font-size="11">1,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
lines += u"""\n<g id="association-Créer">""" % {}
path = upper_round_rect(-35+x,-29+y,70,28,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_cartouche_color'], 'stroke_color': colors['association_cartouche_color']}
path = lower_round_rect(-35+x,-1.0+y,70,30,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_color'], 'stroke_color': colors['association_color']}
lines += u"""\n	<rect x="%(x)s" y="%(y)s" width="70" height="58" fill="%(color)s" rx="14" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -35+x, 'y': -29+y, 'color': colors['transparent_color'], 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x0': -35+x, 'y0': -1+y, 'x1': 35+x, 'y1': -1+y, 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Copperplate" font-size="18">Créer</text>""" % {'x': -28+x, 'y': -7.7+y, 'text_color': colors['association_cartouche_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Association Ajouter -->"""
(x,y) = (cx[u"Ajouter"],cy[u"Ajouter"])
(ex,ey) = (cx[u"Discipline"],cy[u"Discipline"])
leg=straight_leg_factory(ex,ey,55,38,x,y,44,29,18+2*card_margin,14+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"Ajouter,Discipline"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Futura" font-size="11">1,1</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
(ex,ey) = (cx[u"Administrateur"],cy[u"Administrateur"])
leg=straight_leg_factory(ex,ey,80,21,x,y,44,29,19+2*card_margin,14+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"Ajouter,Administrateur"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Futura" font-size="11">1,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
lines += u"""\n<g id="association-Ajouter">""" % {}
path = upper_round_rect(-44+x,-29+y,88,28,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_cartouche_color'], 'stroke_color': colors['association_cartouche_color']}
path = lower_round_rect(-44+x,-1.0+y,88,30,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_color'], 'stroke_color': colors['association_color']}
lines += u"""\n	<rect x="%(x)s" y="%(y)s" width="88" height="58" fill="%(color)s" rx="14" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -44+x, 'y': -29+y, 'color': colors['transparent_color'], 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x0': -44+x, 'y0': -1+y, 'x1': 44+x, 'y1': -1+y, 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Copperplate" font-size="18">Ajouter</text>""" % {'x': -37+x, 'y': -7.7+y, 'text_color': colors['association_cartouche_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Association Affecter -->"""
(x,y) = (cx[u"Affecter"],cy[u"Affecter"])
(ex,ey) = (cx[u"Professeur"],cy[u"Professeur"])
leg=straight_leg_factory(ex,ey,62,55,x,y,49,29,19+2*card_margin,14+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"Affecter,Professeur"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Futura" font-size="11">0,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
(ex,ey) = (cx[u"Discipline"],cy[u"Discipline"])
leg=straight_leg_factory(ex,ey,55,38,x,y,49,29,19+2*card_margin,14+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"Affecter,Discipline"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Futura" font-size="11">0,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
(ex,ey) = (cx[u"Classe"],cy[u"Classe"])
leg=straight_leg_factory(ex,ey,40,21,x,y,49,29,19+2*card_margin,14+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"Affecter,Classe"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Futura" font-size="11">0,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
(ex,ey) = (cx[u"Élève"],cy[u"Élève"])
leg=straight_leg_factory(ex,ey,35,21,x,y,49,29,19+2*card_margin,14+2*card_margin)
lines += u"""\n<line x1="%(ex)s" y1="%(ey)s" x2="%(ax)s" y2="%(ay)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'ex': ex, 'ey': ey, 'ax': x, 'ay': y, 'stroke_color': colors['leg_stroke_color']}
(tx,ty)=offset(*leg.card_pos(False,shift[u"Affecter,Élève"]))
lines += u"""\n<text x="%(tx)s" y="%(ty)s" fill="%(text_color)s" font-family="Futura" font-size="11">0,N</text>""" % {'tx': tx, 'ty': ty, 'text_color': colors['card_text_color']}
lines += u"""\n<g id="association-Affecter">""" % {}
path = upper_round_rect(-49+x,-29+y,98,28,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_cartouche_color'], 'stroke_color': colors['association_cartouche_color']}
path = lower_round_rect(-49+x,-1.0+y,98,30,14)
lines += u"""\n	<path d="%(path)s" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'path': path, 'color': colors['association_color'], 'stroke_color': colors['association_color']}
lines += u"""\n	<rect x="%(x)s" y="%(y)s" width="98" height="58" fill="%(color)s" rx="14" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -49+x, 'y': -29+y, 'color': colors['transparent_color'], 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x0': -49+x, 'y0': -1+y, 'x1': 49+x, 'y1': -1+y, 'stroke_color': colors['association_stroke_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Copperplate" font-size="18">Affecter</text>""" % {'x': -42+x, 'y': -7.7+y, 'text_color': colors['association_cartouche_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Entity Administrateur -->"""
(x,y) = (cx[u"Administrateur"],cy[u"Administrateur"])
lines += u"""\n<g id="entity-Administrateur">""" % {}
lines += u"""\n	<g id="frame-Administrateur">""" % {}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="160" height="30" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -80+x, 'y': -21+y, 'color': colors['entity_cartouche_color'], 'stroke_color': colors['entity_cartouche_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="160" height="12" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -80+x, 'y': 9.0+y, 'color': colors['entity_color'], 'stroke_color': colors['entity_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="160" height="42" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -80+x, 'y': -21+y, 'color': colors['transparent_color'], 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n		<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x0': -80+x, 'y0': 9+y, 'x1': 80+x, 'y1': 9+y, 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n	</g>""" % {}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Copperplate" font-size="18">Administrateur</text>""" % {'x': -72+x, 'y': 0.3+y, 'text_color': colors['entity_cartouche_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Entity Élève -->"""
(x,y) = (cx[u"Élève"],cy[u"Élève"])
lines += u"""\n<g id="entity-Élève">""" % {}
lines += u"""\n	<g id="frame-Élève">""" % {}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="70" height="30" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -35+x, 'y': -21+y, 'color': colors['entity_cartouche_color'], 'stroke_color': colors['entity_cartouche_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="70" height="12" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -35+x, 'y': 9.0+y, 'color': colors['entity_color'], 'stroke_color': colors['entity_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="70" height="42" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -35+x, 'y': -21+y, 'color': colors['transparent_color'], 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n		<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x0': -35+x, 'y0': 9+y, 'x1': 35+x, 'y1': 9+y, 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n	</g>""" % {}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Copperplate" font-size="18">Élève</text>""" % {'x': -27+x, 'y': 0.3+y, 'text_color': colors['entity_cartouche_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Entity Professeur -->"""
(x,y) = (cx[u"Professeur"],cy[u"Professeur"])
lines += u"""\n<g id="entity-Professeur">""" % {}
lines += u"""\n	<g id="frame-Professeur">""" % {}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="124" height="30" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -62+x, 'y': -55+y, 'color': colors['entity_cartouche_color'], 'stroke_color': colors['entity_cartouche_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="124" height="80" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -62+x, 'y': -25.0+y, 'color': colors['entity_color'], 'stroke_color': colors['entity_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="124" height="110" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -62+x, 'y': -55+y, 'color': colors['transparent_color'], 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n		<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x0': -62+x, 'y0': -25+y, 'x1': 62+x, 'y1': -25+y, 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n	</g>""" % {}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Copperplate" font-size="18">Professeur</text>""" % {'x': -54+x, 'y': -33.7+y, 'text_color': colors['entity_cartouche_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Gill Sans" font-size="15">professeur_id</text>""" % {'x': -54+x, 'y': -7.9+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -54+x, 'y0': -5+y, 'x1': 33+x, 'y1': -5+y, 'stroke_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Gill Sans" font-size="15">prenom</text>""" % {'x': -54+x, 'y': 9.1+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Gill Sans" font-size="15">nom</text>""" % {'x': -54+x, 'y': 26.1+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Gill Sans" font-size="15">titre</text>""" % {'x': -54+x, 'y': 43.0+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Entity Discipline -->"""
(x,y) = (cx[u"Discipline"],cy[u"Discipline"])
lines += u"""\n<g id="entity-Discipline">""" % {}
lines += u"""\n	<g id="frame-Discipline">""" % {}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="110" height="30" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -55+x, 'y': -38+y, 'color': colors['entity_cartouche_color'], 'stroke_color': colors['entity_cartouche_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="110" height="46" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -55+x, 'y': -8.0+y, 'color': colors['entity_color'], 'stroke_color': colors['entity_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="110" height="76" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -55+x, 'y': -38+y, 'color': colors['transparent_color'], 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n		<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x0': -55+x, 'y0': -8+y, 'x1': 55+x, 'y1': -8+y, 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n	</g>""" % {}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Copperplate" font-size="18">Discipline</text>""" % {'x': -47+x, 'y': -16.7+y, 'text_color': colors['entity_cartouche_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Gill Sans" font-size="15">discipline_id</text>""" % {'x': -47+x, 'y': 9.1+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n	<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1"/>""" % {'x0': -47+x, 'y0': 12+y, 'x1': 30+x, 'y1': 12+y, 'stroke_color': colors['entity_attribute_text_color']}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Gill Sans" font-size="15">nom</text>""" % {'x': -47+x, 'y': 26.1+y, 'text_color': colors['entity_attribute_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Entity Période -->"""
(x,y) = (cx[u"Période"],cy[u"Période"])
lines += u"""\n<g id="entity-Période">""" % {}
lines += u"""\n	<g id="frame-Période">""" % {}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="88" height="30" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -44+x, 'y': -21+y, 'color': colors['entity_cartouche_color'], 'stroke_color': colors['entity_cartouche_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="88" height="12" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -44+x, 'y': 9.0+y, 'color': colors['entity_color'], 'stroke_color': colors['entity_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="88" height="42" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -44+x, 'y': -21+y, 'color': colors['transparent_color'], 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n		<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x0': -44+x, 'y0': 9+y, 'x1': 44+x, 'y1': 9+y, 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n	</g>""" % {}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Copperplate" font-size="18">Période</text>""" % {'x': -36+x, 'y': 0.3+y, 'text_color': colors['entity_cartouche_text_color']}
lines += u"""\n</g>""" % {}

lines += u"""\n\n<!-- Entity Classe -->"""
(x,y) = (cx[u"Classe"],cy[u"Classe"])
lines += u"""\n<g id="entity-Classe">""" % {}
lines += u"""\n	<g id="frame-Classe">""" % {}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="80" height="30" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -40+x, 'y': -21+y, 'color': colors['entity_cartouche_color'], 'stroke_color': colors['entity_cartouche_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="80" height="12" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="0"/>""" % {'x': -40+x, 'y': 9.0+y, 'color': colors['entity_color'], 'stroke_color': colors['entity_color']}
lines += u"""\n		<rect x="%(x)s" y="%(y)s" width="80" height="42" fill="%(color)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x': -40+x, 'y': -21+y, 'color': colors['transparent_color'], 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n		<line x1="%(x0)s" y1="%(y0)s" x2="%(x1)s" y2="%(y1)s" stroke="%(stroke_color)s" stroke-width="1.5"/>""" % {'x0': -40+x, 'y0': 9+y, 'x1': 40+x, 'y1': 9+y, 'stroke_color': colors['entity_stroke_color']}
lines += u"""\n	</g>""" % {}
lines += u"""\n	<text x="%(x)s" y="%(y)s" fill="%(text_color)s" font-family="Copperplate" font-size="18">Classe</text>""" % {'x': -32+x, 'y': 0.3+y, 'text_color': colors['entity_cartouche_text_color']}
lines += u"""\n</g>""" % {}
lines += u'\n</svg>'

with codecs.open(r"mocodo_notebook/sandbox.svg", "w", "utf8") as f:
    f.write(lines)
safe_print_for_PHP(u'Fichier de sortie "mocodo_notebook/sandbox.svg" généré avec succès.')