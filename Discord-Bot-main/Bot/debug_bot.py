from importlib import reload
import event
import types


# Déclaration d'un décorateur à fonction (@update_module(module_name))
def update_module(module):
    def __update__(func):
        # Recherche du module pour voir s'il est déjà chargé ; si ce n'est pas le cas :
        # il importe dynamiquement et ensuite, la fonction 'reload' recharge le module.
        async def callback(*args, **kwargs):
            reload(__import__(module, globals(), locals(), [],
                              0))
            return await func(*args, **kwargs)
        return callback
    return __update__


def update_all_modules(func):
    async def __update__(*args, **kwargs):
        for name, val in globals().items():
            if isinstance(val, types.ModuleType):
                print(val.__name__)
                reload(__import__(val.__name__, globals(), locals(), [], 0))

            reload(__import__("DebugBot", globals(), locals(), [], 0))

        return await func(*args, **kwargs)
    return __update__


async def debug_on_message(*args, **kwargs):
    return await event.on_message(*args, **kwargs)


async def debug_on_prez(*args, **kwargs):
    return await event.on_prez(*args, **kwargs)


async def debug_on_help(*args, **kwargs):
    return await event.on_help(*args, **kwargs)
