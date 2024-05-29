import threading


class ContextHolder:
    _thread_local = threading.local()

    @staticmethod
    def set_context(context):
        setattr(ContextHolder._thread_local,"context",{
            "thread_name":threading.current_thread().name,
            **context
        })

    @staticmethod
    def set_context_kv(key, value):
        context = getattr(ContextHolder._thread_local, "context", {})
        context[key] = value
        ContextHolder.set_context(context)

    @staticmethod
    def get_context_kv(key):
        context = getattr(ContextHolder._thread_local, "context", {})
        return context.get(key)

    @staticmethod
    def get_context():
        return getattr(ContextHolder._thread_local, "context", None)