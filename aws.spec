# -*- mode: python -*-
import glob


def Datafiles(filenames, **kw):
    import os
    
    def datafile(path, strip_path=True, prefix=''):
        name = path
        if strip_path:
            name = os.path.basename(path)
        if prefix:
            name = os.path.basename(path)
            name = os.path.join(prefix, name)
        return name, path, 'DATA'

    strip_path = kw.get('strip_path', True)
    prefix = kw.get('prefix', '')

    datafiles = []
    for filename in filenames:
        if os.path.isfile(filename):
            datafiles.append(datafile(filename, strip_path=strip_path, prefix=prefix))
    return TOC(datafiles)

botocore_location = [s for s in os.sys.path if "botocore" in s][0]
boto_datafiles = Datafiles(glob.glob('%s/botocore/data/aws/*.json' % botocore_location), prefix='botocore/data/aws')
boto_servicefiles = Datafiles(glob.glob('%s/services/*.json' % botocore_location), prefix='botocore/services')

doc_examples = Datafiles(glob.glob('./awscli/examples/**/*.rst'))
cacert = '%s/botocore/vendored/requests/cacert.pem' % botocore_location
cacert_datafile = Datafiles([cacert], prefix='botocore/vendored/requests')

a = Analysis(['bin/aws', 'awscli/__init__.py','awscli/customizations/commands.py','awscli/handlers.py', 'awscli/clidriver.py'],
             pathex=['.', './awscli/customizations','awscli/data/'],
             hiddenimports=['HTMLParser','markupbase','awscli.handlers','awscli.errorhandler','awscli.customizations','IPython','awscli.customizations.s3.s3'],
             hookspath=None,
             runtime_hooks=None)
aws_data = [('awscli/data/cli.json', './awscli/data/cli.json', 'DATA'),
            ]
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.datas,
          a.zipfiles,
          aws_data,
          doc_examples,
          boto_datafiles,
          boto_servicefiles,
          cacert_datafile,
          exclude_binaries=False,
          name='aws',
          debug=False,
          strip=None,
          upx=True,
          console=True )
