def AddActionWrapper(handler):
    def wraps(env, files, action):
        if not isinstance(files, (list, tuple, set)):
            files = [files]
        known_nodes = []
        unknown_files = []
        for item in files:
            nodes = env.arg2nodes(item, env.fs.Entry)
            if nodes and nodes[0].exists():
                known_nodes.extend(nodes)
            else:
                unknown_files.append(item)
        if unknown_files:
            env.Append(**{"_ZX_DELAYED_ACTIONS": [(handler, unknown_files, action)]})
        if known_nodes:
            return handler(known_nodes, action)
        return []

    return wraps


def ProcessDelayedActions(env):
    for func, nodes, action in env.get("_ZX_DELAYED_ACTIONS", []):
        func(nodes, action)


def generate(env):
    env.Replace(**{"_ZX_DELAYED_ACTIONS": []})
    env.AddMethod(AddActionWrapper(env.AddPreAction), "AddPreAction")
    env.AddMethod(AddActionWrapper(env.AddPostAction), "AddPostAction")
    env.AddMethod(ProcessDelayedActions)


def exists(_):
    return True
