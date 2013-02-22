# -*- coding: utf-8 -*-
from PyQt4 import QtGui
from pivy.coin import *
from math import *
from superficie.widgets import Slider

try:
    from pivy.quarter import QuarterWidget

    Quarter = True
except ImportError:
    from pivy.gui.soqt import *

    Quarter = False

from superficie.nodes import Sphere, BasePlane, Line, Curve3D, TangentPlane2
from superficie.animations import Animation
from superficie.book import Chapter, Page
from superficie.plots import Plot3D, RevolutionPlot3D, ParametricPlot3D
from superficie.util import _1, Vec3, intervalPartition
from superficie.utils import to_polar


class Elipsoide(Page):
    u"""
    """
    def __init__(self):
        Page.__init__(self, u"Elipsoide")
        param = lambda u,v: (cos(u)*cos(v), 1.5*cos(v)*sin(u), 2*sin(v))
        elipsoide = ParametricPlot3D(param, (-pi, pi), (-pi/2,pi/2))
        col = _1(84,129,121)
        elipsoide.setAmbientColor(col).setDiffuseColor(col).setSpecularColor(col)
        par1 = lambda u,v: Vec3(-sin(u)*cos(v), 1.5*cos(u)*cos(v), 0)
        par2 = lambda u,v: Vec3(-cos(u)*sin(v), -1.5*sin(u)*sin(v), 2*cos(v))
        tp = TangentPlane2(param,par1,par2,(0,0),_1(252,250,225))
        self.addChild(elipsoide)
        self.addChild(tp)
        Slider(rangep=('u', -pi,pi,0,20),func=tp.setU, parent=self)
        Slider(rangep=('v', -pi/2,pi/2,0,20),func=tp.setV,parent=self)


class Cilindro(Page):
    u"""
    """
    def __init__(self):
        Page.__init__(self, u"Cilindro")
        param = lambda u,t: Vec3(cos(u),sin(u),t)
        cilindro = ParametricPlot3D(param, (0, 2*pi), (-1,1))
        col = _1(177,89,77)
        cilindro.setAmbientColor(col).setDiffuseColor(col).setSpecularColor(col)

        def par1(u,t): return Vec3(-sin(u),cos(u),0)
        def par2(u,t): return Vec3(0,0,1)
        tp = TangentPlane2(param,par1,par2,(0,0),_1(252,250,225))
        tp.localOriginSphere.hide()
        tp.localYAxis.setColor(col).setWidth(2).show()
        Slider(rangep=('u', 0,2*pi,0,20),func=tp.setU, parent=self)
        Slider(rangep=('t', -1,1,0,20),func=tp.setV,parent=self)
        self.addChild(cilindro)
        self.addChild(tp)


class ParaboloideHiperbolico(Page):
    u"""Para el paraboloide hiperbólico, el plano tangente en cada punto corta a la superficie
    en dos rectas y hay parte de la superficie en cada uno de los semiespacios definidos
    por él. Hay curvas en la superficie cuyos vectores de aceleración apuntan a lados distintos
    del plano tangente.
    """

    def __init__(self):
        """x^2 - y^2 - z = 0"""
        Page.__init__(self, u"Paraboloide Hiperbólico")

        z = 1.5

        def fn(x, y):
            return x ** 2 - y ** 2 + z

        def polar(function):
            def polar_fn(r, t):
                x = r * cos(t)
                y = r * sin(t)
                return x, y, function(x, y)

            return polar_fn

        paraboloid = ParametricPlot3D(polar(fn), (.001, 1, 20), (0, 2 * pi, 60))

        paraboloid. \
            setAmbientColor(_1(145, 61, 74)). \
            setDiffuseColor(_1(127, 119, 20)). \
            setSpecularColor(_1(145, 61, 74))

        base_plane = BasePlane()
        base_plane.setHeight(0)
        base_plane.setRange((-2, 2, 7))

        ## the hiperbolic paraboloid in parametric form
        def fn_par(x,y): return Vec3(x, y, x ** 2 - y ** 2 + z)

        ## its derivatives
        def fn_x(x,y): return Vec3(1, 0, 2 * x)

        def fn_y(x,y): return Vec3(0, 1, -2 * y)

        tangent_plane = TangentPlane2(fn_par, fn_x, fn_y, (0, 0), _1(252, 250, 225))
        tangent_plane.setRange((-1.2, 1.2, 7))

        self.addChild(paraboloid)
        self.addChild(base_plane)
        self.addChild(tangent_plane)

        def spiral(t):
            c = t / (2 * pi)
            t2 = t * 2
            return c * cos(t2), c * sin(t2)

        animate_points = 200

        def animate_plane(n):
            tangent_plane.setLocalOrigin(spiral(2 * pi * n / float(animate_points)))

        def animate_plane_2(t):
            tangent_plane.setLocalOrigin(spiral(t))

        a1 = Animation(animate_plane, (10000, 0, animate_points))

        Slider(('t', 0, 2 * pi, 0, animate_points), animate_plane_2, duration=10000, parent=self)

        self.setupAnimations([a1])


class Toro(Page):
    u"""Los puntos del toro de revolución ubicados en la circunferencia exterior son elípticos
    porque el plano tangente en uno de ellos toca al toro sólo en ese punto y deja al toro de
    un solo lado del plano; los puntos de la circunferencia interior son hiperbólicos porque
    el plano tangente en uno de ellos tiene puntos del toro en ambos lados del plano, y los
    puntos de la circunferencia superior son parabólicos porque el plano tangente y el toro
    tienen en común toda esa circunferencia."""

    def __init__(self):
        Page.__init__(self, u"Toro")
        a = 1
        b = 0.5

        def toroParam1(u, v):
            return (a + b * cos(v)) * cos(u), (a + b * cos(v)) * sin(u), b * sin(v)

        toro = ParametricPlot3D(toroParam1, (0, 2 * pi, 150), (0, 2 * pi, 100))
        toro.setTransparencyType(SoTransparencyType.SORTED_OBJECT_SORTED_TRIANGLE_BLEND)
        toro.setTransparency(.4)

        #        delta = 0
        #        p_eli = Sphere((.9571067805, .9571067805, .35+delta),0.02,visible=True)
        #        p_eli.setColor( _1(194,38,69))
        #        p_eli.setShininess(1)
        #
        #        p_par = Sphere ((-0.7071067810, 0.7071067810, 0.5+delta),0.02,visible=True)
        #        p_par.setColor( _1(240,108,21))
        #        p_par.setShininess(1)
        #
        #        p_hyp = Sphere ((0, -0.6464466095, .3535+delta),0.02,visible=True)
        #        p_hyp.setColor( _1(78,186,69))
        #        p_hyp.setShininess(1)

        def toro_u(u, v):
            return Vec3(-(a + b * cos(v)) * sin(u), (a + b * cos(v)) * cos(u), 0)

        def toro_v(u, v):
            return Vec3(-b * sin(v) * cos(u), -b * sin(v) * sin(u), b * cos(v))

        ## plano parabólico
        ptopar = (0, pi / 2)
        b2 = b - .00025
        ## trick: the tangent plane is located in a torus of diameter slightly smaller than the torus; so the
        ## intersection is visible to the naked eye
        def toroParam_delta(u, v):
            return (a + b2 * cos(v)) * cos(u), (a + b2 * cos(v)) * sin(u), b2 * sin(v)
        plane_par = TangentPlane2(toroParam_delta, toro_u, toro_v, ptopar, _1(252, 250, 225))
        plane_par.baseplane.setTransparency(0)
        plane_par.setRange((-.5, .5, 7))

        self.addChild(toro)
        self.addChild(plane_par)

        def animaCurva1(n):
            def curva(t): return (t * 2 * pi, pi / 2)

            plane_par.setLocalOrigin(curva(n / 100.))

        def animaCurva2(n):
            def curva(t): return (0, pi / 2 - t * (2 * pi + pi / 2))

            plane_par.setLocalOrigin(curva(n / 100.))

        def animaCurva3(n):
            def curva(t): return (t * 2 * pi, 0)

            plane_par.setLocalOrigin(curva(n / 100.))

        a1 = Animation(animaCurva1, (6000, 0, 100))
        a2 = Animation(animaCurva2, (6000, 0, 100))
        a3 = Animation(animaCurva3, (6000, 0, 100))

        self.setupAnimations([a1, a2, a3])


figuras = [
    Elipsoide,
    Cilindro,
    ParaboloideHiperbolico,
    Toro
]


class Superficies2(Chapter):
    def __init__(self):
        Chapter.__init__(self, name="Plano tangente")
        for f in figuras:
            self.addPage(f())
        self.whichPage = 0

    def chapterSpecificIn(self):
        print "chapterSpecificIn"


if __name__ == "__main__":
    import sys
    from superficie.viewer.Viewer import Viewer

    app = QtGui.QApplication(sys.argv)
    visor = Viewer()
    visor.addChapter(Superficies2())
    ## ============================
    visor.whichPage = 0
    visor.resize(400, 400)
    visor.show()
    visor.chaptersStack.show()

    if Quarter:
        sys.exit(app.exec_())
    else:
        SoQt.mainLoop()

