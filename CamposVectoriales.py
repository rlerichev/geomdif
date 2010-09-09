# -*- coding: utf-8 -*-
__author__ = 'jpablo'
__date__ = "$24/11/2009 11:06:25 PM$"


from superficie.Book import Page
from math import pi, sin, cos, tan
from superficie.util import Vec3, _1, partial
from superficie.VariousObjects import Curve3D, TangentPlane2
from superficie.Animation import AnimationGroup, Animation
from PyQt4 import QtGui
from superficie.Plot3D import ParametricPlot3D, Plot3D
from pivy.coin import SoTransparencyType
from superficie.gui import VisibleCheckBox


from superficie.Book import Chapter


class HeliceRectificada(Page):
    def __init__(self):
        Page.__init__(self, u"Hélice Circular Rectificada")

        tmin = -4 * pi
        tmax = 4 * pi
        sq2 = 2 ** (0.5)
        ## ============================================
        def helicerec(s):
            return Vec3(cos((1. / sq2) * s), sin((1. / sq2) * s), (1. / sq2) * s)
        def tangente(s):
            return Vec3(-1. / sq2 * sin(s / sq2) , 1. / sq2 * cos(s / sq2) , 1. / sq2)
        def normal(s):
            return Vec3(-cos(s / sq2) , -sin(s / sq2) , 0)
        def binormal(s):
            return Vec3(1. / sq2 * sin(s / sq2) , -1. / sq2 * cos(s / sq2) , 1. / sq2)

        curva = Curve3D(helicerec, (tmin, tmax, 100), _1(206, 75, 150), 2, parent=self)

        #=======================================================================
        # planos
        #=======================================================================
        def embed(fn):
            return lambda u, v: fn(u)

        plano_osculador = TangentPlane2(embed(helicerec), embed(tangente), embed(normal), (tmin, 0), _1(252, 250, 225), visible=True, parent=self)
        plano_normal = TangentPlane2(embed(helicerec), embed(normal), embed(binormal), (tmin, 0), _1(252, 250, 225), visible=True, parent=self)
        plano_rectificante = TangentPlane2(embed(helicerec), embed(binormal), embed(tangente), (tmin, 0), _1(252, 250, 225), visible=True, parent=self)

        plano_osculador.setRange((-1.5, 1.5, 30))
        plano_normal.setRange((-1.5, 1.5, 30))
        plano_rectificante.setRange((-1.5, 1.5, 30))

        def set_origen(n):
            pt = curva.domainPoints[n]
            plano_osculador.setOrigin((pt, 0))
            plano_normal.setOrigin((pt, 0))
            plano_rectificante.setOrigin((pt, 0))

        plano_osculador.animation = Animation(set_origen, (8000, 0, len(curva) - 1))
        #=======================================================================
        # Vectores
        #=======================================================================
        curva.setField("tangente", tangente)
        curva.setField("normal", normal)
        curva.setField("binormal", binormal)
        curva.fields['tangente'].show()
        curva.fields['normal'].show()
        curva.fields['binormal'].show()
        rango = (8000,0,len(curva)-1)
        self.setupAnimations([ AnimationGroup( [
                plano_osculador,
                curva.fields['tangente'],
                curva.fields['normal'],
                curva.fields['binormal']],
            rango ) ])


#class SerieOrden4(Page):
#    def __init__(self):
#        Page.__init__(self, u"Desarrollo en serie")
#        def param(s):
#            return Vec3()
#
#        curva = Curve3D(param, (tmin, tmax, 100), parent=self)



class Esfera1(Page):
    def __init__(self):
        Page.__init__(self, u"Sobre la esfera")

        def make_circulo(t):
            return partial(par_esfera, t)

        par_esfera = lambda t, f: 0.99*Vec3(sin(t) * cos(f), sin(t) * sin(f), cos(t))
        esf = ParametricPlot3D(par_esfera, (0, pi, 100), (0, 2 * pi, 120))
        esf.setTransparencyType(SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND)
        esf.setTransparency(0.4)
        esf.setDiffuseColor(_1(68, 28, 119))
        VisibleCheckBox("esfera", esf, True, parent=self)
        self.addChild(esf)

        def par_curva(c,t):
            t = tan(t/(4*pi))
            den = c**2+t**2+1
            return Vec3(2*c / den, 2*t / den, (c**2+t**2-1) / den)


        def par_tang(c,t):
            t = tan(t/(4*pi))
            den = (c**2+t**2+1)**2
            return Vec3(-2*c*(2*t) / den, (2*(c**2+t**2+1)-4*t**2) / den, 4*t / den)

        def make_curva(c):
            return partial(par_curva,c)

        def make_tang(c):
            return partial(par_tang,c)

        tangentes = []

        for c in range(-10,11):
            ct = tan(c/(2*pi))
            curva = Curve3D(make_curva(ct),(-20,20,80), width=1, parent=self)
            curva.setField("tangente", make_tang(ct)).setLengthFactor(1).setWidthFactor(.1)
            curva.fields['tangente'].show()
            tangentes.append(curva.fields['tangente'])


        def animaTangentes(n):
            for tang in tangentes:
                tang.animate_field(n)

        a1 = Animation(animaTangentes, (10000, 0, 79))
        self.setupAnimations([a1])


class Esfera2(Page):
    ## paralelos
    def __init__(self):
        Page.__init__(self, u"Sobre la esfera")

        par_esfera = lambda u, v: Vec3(sin(u) * cos(v), sin(u) * sin(v), cos(u))
            
        def esfera_u(u,v):
            return Vec3(cos(u)*cos(v), cos(u)*sin(v), -sin(u))

        def esfera_v(u,v):
            return Vec3(-sin(u)*sin(v), cos(v)*sin(u), 0)


        parab = ParametricPlot3D(par_esfera, (0,2,150),(0,2*pi,100))
        parab.setTransparency(0.4)
        parab.setTransparencyType(SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND)
        parab.setDiffuseColor(_1(68, 28, 119))
        self.addChild(parab)

        def make_curva(c):
            return partial(par_esfera,c)

        def make_tang(c):
            return partial(esfera_v,c)

        tangentes = []
        ncurves = 70
        for c in range(0,ncurves+1):
            ## -1 < ct < 1
            ct = c/float(ncurves) * 2*pi
            curva = Curve3D(make_curva(ct),(0,2*pi,100), width=1, parent=self)
            curva.setField("tangente", make_tang(ct)).setLengthFactor(.4).setWidthFactor(.1)
            curva.fields['tangente'].show()
            tangentes.append(curva.fields['tangente'])


        def animaTangentes(n):
            for tang in tangentes:
                tang.animate_field(n)

        a1 = Animation(animaTangentes, (6000, 0, 99))
        self.setupAnimations([a1])

class Esfera3(Page):
    ## meridianos
    def __init__(self):
        Page.__init__(self, u"Sobre la esfera")

        par_esfera = lambda u, v: Vec3(sin(u) * cos(v), sin(u) * sin(v), cos(u))

        def esfera_u(u,v):
            return Vec3(cos(u)*cos(v), cos(u)*sin(v), -sin(u))

        def esfera_v(u,v):
            return Vec3(-sin(u)*sin(v), cos(v)*sin(u), 0)


        parab = ParametricPlot3D(par_esfera, (0,2,150),(0,2*pi,100))
        parab.setTransparency(0.4)
        parab.setTransparencyType(SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND)
        parab.setDiffuseColor(_1(68, 28, 119))
        self.addChild(parab)

        def make_curva(c):
            return lambda t: par_esfera(t,c)

        def make_tang(c):
            return lambda t: esfera_u(t,c)

        tangentes = []
        ncurves = 70
        for c in range(0,ncurves+1):
            ## -1 < ct < 1
            ct = c/float(ncurves) * 2*pi
            curva = Curve3D(make_curva(ct),(0.1,pi-.1,100), width=1, parent=self)
            curva.setField("tangente", make_tang(ct)).setLengthFactor(.4).setWidthFactor(.1)
            curva.fields['tangente'].show()
            tangentes.append(curva.fields['tangente'])


        def animaTangentes(n):
            for tang in tangentes:
                tang.animate_field(n)

        a1 = Animation(animaTangentes, (6000, 0, 99))
        self.setupAnimations([a1])


class ParaboloideHiperbolico(Page):
    def __init__(self):
        Page.__init__(self, u"Sobre el paraboloide hiperbólico")

        par_parab = lambda x, y: Vec3(x,y,x ** 2 - y ** 2)
        par_tang = lambda x,y: Vec3(0,1,-2*y)

        parab = ParametricPlot3D(par_parab, (-1, 1), (-1, 1))
        parab.setTransparency(0.4)
        parab.setTransparencyType(SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND)
        parab.setDiffuseColor(_1(68, 28, 119))        
        self.addChild(parab)

        def make_curva(c):
            return partial(par_parab,c)

        def make_tang(c):
            return partial(par_tang,c)

        tangentes = []
        
        for c in range(0,21):
            ## -1 < ct < 1
            ct = 2*c/20.0-1
            curva = Curve3D(make_curva(ct),(-1,1,50), width=1, parent=self)
            curva.setField("tangente", make_tang(ct)).setLengthFactor(.3).setWidthFactor(.075)
            curva.fields['tangente'].show()
            tangentes.append(curva.fields['tangente'])


        def animaTangentes(n):
            for tang in tangentes:
                tang.animate_field(n)

        a1 = Animation(animaTangentes, (6000, 0, 49))
        self.setupAnimations([a1])


class ParaboloideHiperbolicoReglado(Page):
    def __init__(self):
        Page.__init__(self, u"Sobre el paraboloide hiperbólico")

        par_parab = lambda x, y: Vec3(x,y,x*y)
        par_tang = lambda x,y: Vec3(0,1,x)

        parab = ParametricPlot3D(par_parab, (-1, 1), (-1, 1))
        parab.setTransparency(0.4)
        parab.setTransparencyType(SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND)
        parab.setDiffuseColor(_1(68, 28, 119))
        self.addChild(parab)

        def make_curva(c):
            return partial(par_parab,c)

        def make_tang(c):
            return partial(par_tang,c)

        tangentes = []

        for c in range(0,21):
            ## -1 < ct < 1
            ct = 2*c/20.0-1
            curva = Curve3D(make_curva(ct),(-1,1,50), width=1, parent=self)
            curva.setField("tangente", make_tang(ct)).setLengthFactor(.4).setWidthFactor(.1)
            curva.fields['tangente'].show()
            tangentes.append(curva.fields['tangente'])


        def animaTangentes(n):
            for tang in tangentes:
                tang.animate_field(n)

        a1 = Animation(animaTangentes, (6000, 0, 49))
        self.setupAnimations([a1])



class ParaboloideHiperbolicoCortes(Page):
    def __init__(self):
        Page.__init__(self, u"Sobre el paraboloide hiperbólico")

        par_parab = lambda x, y: Vec3(x,y,x*y)
        par_tang = lambda x,y: Vec3(0,1,x)

        parab = ParametricPlot3D(par_parab, (-1, 1), (-1, 1))
        parab.setTransparency(0.4)
        parab.setTransparencyType(SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND)
        parab.setDiffuseColor(_1(68, 28, 119))
        self.addChild(parab)

        def make_curva(c):
            return partial(par_parab,c)

        def make_tang(c):
            return partial(par_tang,c)

        tangentes = []

        for c in range(0,21):
            ## -1 < ct < 1
            ct = 2*c/20.0-1
            curva = Curve3D(make_curva(ct),(-1,1,50), width=1, parent=self)
            curva.setField("tangente", make_tang(ct)).setLengthFactor(.4).setWidthFactor(.1)
            curva.fields['tangente'].show()
            tangentes.append(curva.fields['tangente'])


        def animaTangentes(n):
            for tang in tangentes:
                tang.animate_field(n)

        a1 = Animation(animaTangentes, (6000, 0, 49))
        self.setupAnimations([a1])


class ToroMeridianos(Page):
    def __init__(self):
        Page.__init__(self, u"Sobre el toro")
        a = 1
        b = 0.5
        def toroParam1(u,v):
            return ((a+b*cos(v))*cos(u),(a+b*cos(v))*sin(u),b*sin(v))

        def toro_u(u,v):
            return Vec3(-(a+b*cos(v))*sin(u), (a+b*cos(v))*cos(u), 0)

        def toro_v(u,v):
            return Vec3(-b*sin(v)*cos(u), -b*sin(v)*sin(u), b*cos(v))
        

        parab = ParametricPlot3D(toroParam1, (0,2*pi,150),(0,2*pi,100))
        parab.setTransparency(0.4)
        parab.setTransparencyType(SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND)
        parab.setDiffuseColor(_1(68, 28, 119))
        self.addChild(parab)


        def make_curva(c):
            return partial(toroParam1,c)

        def make_tang(c):
            return partial(toro_v,c)

        tangentes = []
        ncurves = 70
        for c in range(0,ncurves+1):
            ## -1 < ct < 1
            ct = c/float(ncurves) * 2*pi
            curva = Curve3D(make_curva(ct),(0,2*pi,100), width=1, parent=self)
            curva.setField("tangente", make_tang(ct)).setLengthFactor(.4).setWidthFactor(.1)
            curva.fields['tangente'].show()
            tangentes.append(curva.fields['tangente'])


        def animaTangentes(n):
            for tang in tangentes:
                tang.animate_field(n)

        a1 = Animation(animaTangentes, (6000, 0, 99))
        self.setupAnimations([a1])


class ToroParalelos(Page):
    def __init__(self):
        Page.__init__(self, u"Sobre el toro")
        a = 1
        b = 0.5
        def toroParam1(u,v):
            return ((a+b*cos(v))*cos(u),(a+b*cos(v))*sin(u),b*sin(v))

        def toro_u(u,v):
            return Vec3(-(a+b*cos(v))*sin(u), (a+b*cos(v))*cos(u), 0)

        def toro_v(u,v):
            return Vec3(-b*sin(v)*cos(u), -b*sin(v)*sin(u), b*cos(v))


        parab = ParametricPlot3D(toroParam1, (0,2*pi,150),(0,2*pi,100))
        parab.setTransparency(0.4)
        parab.setTransparencyType(SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND)
        parab.setDiffuseColor(_1(68, 28, 119))
        self.addChild(parab)


        def make_curva(c):
            return lambda t: toroParam1(t,c)

        def make_tang(c):
            return lambda t: toro_u(t,c)

        tangentes = []
        ncurves = 50
        for c in range(0,ncurves+1):
            ## -1 < ct < 1
            ct = c/float(ncurves) * 2*pi
            curva = Curve3D(make_curva(ct),(0,2*pi,100), width=1, parent=self)
            curva.setField("tangente", make_tang(ct)).setLengthFactor(.4).setWidthFactor(.1)
            curva.fields['tangente'].show()
            tangentes.append(curva.fields['tangente'])


        def animaTangentes(n):
            for tang in tangentes:
                tang.animate_field(n)

        a1 = Animation(animaTangentes, (6000, 0, 99))
        self.setupAnimations([a1])

figuras = [
        Esfera1,
        Esfera2,
        Esfera3,
        ParaboloideHiperbolico,
        ParaboloideHiperbolicoReglado,
        ToroMeridianos,
        ToroParalelos
]

class CamposVectoriales(Chapter):
    def __init__(self):
        Chapter.__init__(self, name="Campos Vectoriales")
        for f in figuras:
            self.addPage(f())

    def chapterSpecificIn(self):
        print "chapterSpecificIn"
#        self.viewer.setTransparencyType(SoGLRenderAction.SORTED_LAYERS_BLEND)


if __name__ == "__main__":
    import sys
    from superficie.Viewer import Viewer
    app = QtGui.QApplication(sys.argv)
    visor = Viewer()
    visor.setColorLightOn(False)
    visor.setWhiteLightOn(True)
    visor.addChapter(CamposVectoriales())
    visor.chapter.chapterSpecificIn()
    visor.whichPage = 0
    visor.resize(400, 400)
    visor.show()
    visor.chaptersStack.show()
    sys.exit(app.exec_())