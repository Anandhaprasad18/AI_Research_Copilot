import os
import sys
sys.path.insert(0, r'd:\AI_Research_Copilot_completed\AI_Research_Copilot')
os.environ['GROQ_API_KEY'] = 'dummy'
import main

print('APP TITLE:', main.app.title)
for idx, route in enumerate(main.app.routes):
    print('ROUTE', idx, type(route).__name__)
    print('  path:', getattr(route, 'path', None))
    print('  name:', getattr(route, 'name', None))
    print('  methods:', getattr(route, 'methods', None))
    print('  include:', hasattr(route, 'routes'))
    if hasattr(route, 'routes'):
        print('  nested routes count:', len(route.routes))
        for nr in route.routes:
            print('    NEST', type(nr).__name__, getattr(nr, 'path', None), getattr(nr, 'name', None), getattr(nr, 'methods', None))
