import editables.redirector

F = editables.redirector.RedirectingFinder
F.install()
F.map_module(
    'coherent.build', '/Users/jaraco/code/coherent-oss/coherent.build/__init__.py'
)
