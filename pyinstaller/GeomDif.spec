# -*- mode: python -*-

# GeomDif pyinstaller's "spec" configuration file

#def Datafiles(*filenames, **kw):
#    import os
    
#    def datafile(path, strip_path=True):
#        parts = path.split('/')
#        path = name = os.path.join(*parts)
#        if strip_path:
#            name = os.path.basename(path)
#        return name, path, 'DATA'

#    strip_path = kw.get('strip_path', True)
#    return TOC(
#        datafile(filename, strip_path=strip_path)
#        for filename in filenames
#        if os.path.isfile(filename))

#uifiles = Datafiles( '../../../../Dev/GeomDif.git/ui/mainwindow2.ui',
#                     '../../../../Dev/GeomDif.git/ui/presentacion.ui',
#                     '../../../../Dev/Superficie.git/viewer/change-page.ui',  
#                     strip_path=True )

dir = '../../../../Dev/GeomDif.git/'
#, dir+'Presentacion.py'
a = Analysis([dir+'main.py'], #, dir+'__init__.py'],
             pathex=['/usr/lib/pymodules/python2.7/', '/usr/lib/pymodules/python2.7/superficie/', '../../../../Dev/GeomDif.git', dir, '/home/rlerichev/Software/App/pyinstaller-2.0/projects/GeomDif'],
             #hiddenimports=[ 'Presentacion' ],
             hookspath=dir)

pyz = PYZ(a.pure)

exe = EXE(pyz,
#					a.pure,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.dependencies,
#          a.datas + uifiles,
					a.datas,
					[ ( 'change-page.ui', '../../../../Dev/Superficie.git/viewer/change-page.ui', 'DATA' ),
            ( 'paramTemplate.ui', '../../../../Dev/Superficie.git/Gui/paramTemplate.ui', 'DATA' ),
            ( 'paramTemplate2.ui', '../../../../Dev/Superficie.git/Gui/paramTemplate2.ui', 'DATA' ),
						( 'axis.iv', '../../../../Dev/Superficie.git/viewer/axis.iv', 'DATA' ),
						( 'lights.iv', '../../../../Dev/Superficie.git/viewer/lights.iv', 'DATA' ),
            #( 'Presentacion', dir+'Presentacion.py', 'PYMODULE' ),
						( 'Presentacion', dir+'Presentacion.py', 'EXTENSION' ),
						( 'Curvas1', dir+'Curvas1.py', 'EXTENSION' ),
						( 'CurvasAlabeadas', dir+'CurvasAlabeadas.py', 'EXTENSION' ),
						( 'Curvas3', dir+'Curvas3.py', 'EXTENSION' ),
						( 'CurvasEnSuperficies', dir+'CurvasEnSuperficies.py', 'EXTENSION' ),
						( 'Superficies1', dir+'Superficies1.py', 'EXTENSION' ),
						( 'Superficies2', dir+'Superficies2.py', 'EXTENSION' ),
						( 'CurvaturasNormales', dir+'CurvaturasNormales.py', 'EXTENSION' ),
						( 'Superficies4', dir+'Superficies4.py', 'EXTENSION' ),
						( 'CamposVectoriales', dir+'CamposVectoriales.py', 'EXTENSION' ),
            #( 'superficie.viewer.Viewer', '/usr/lib/pymodules/python2.7/superficie/viewer/Viewer.py', 'EXTENSION' ),
            #( 'superficie.plots', '/usr/lib/pymodules/python2.7/superficie/plots/__init__.py', 'EXTENSION' ),
					  ( 'mainwindow2.ui', dir+'ui/mainwindow2.ui', 'DATA' ),
					  ( 'presentacion.ui', dir+'ui/presentacion.ui', 'DATA' ),
          ],
					name='GeomDif',
          debug=True,
          strip=False,
          upx=False,
					#exclude_binaries=1,
          console=True )

#icofiles = Datafiles('db/countries.db', strip_path=False) # keep the path of this file

#dist = COLLECT( exe,
#               a.binaries,
#			         a.dependencies,
#               a.zipfiles,
#               a.datas,
#               uifiles,
               #icofiles,
#			         strip=False,
#							 upx=False,
               #name=os.path.join('dist', 'GeomDif') )
#							 name='dist' )

