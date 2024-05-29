from hashlib import md5
import json
import threading


class ContextHolder:
    _thread_local = threading.local()

    @staticmethod
    def set_context(context):
        setattr(
            ContextHolder._thread_local,
            "context",
            {"thread_name": threading.current_thread().name, **context},
        )

    @staticmethod
    def set_context_kv(key, value):
        context = getattr(ContextHolder._thread_local, "context", {})
        context[key] = value
        ContextHolder.set_context(context)

    @staticmethod
    def set_context_kv_pre_request(request, key, value):
        request_hash = ContextHolder.make_request_hash(request)
        context = getattr(ContextHolder._thread_local, "context", {})
        context[request_hash] = {**context.get(request_hash, {}), key: value}
        ContextHolder.set_context(context)

    @staticmethod
    def make_request_hash(request):
        str = json.dumps(
            {
                "path": request.path,
                "method": request.method,
                "query": request.GET.dict(),
                "body": request.body.decode("utf-8"),
            }
        )
        return md5(str.encode("utf-8")).hexdigest()

    @staticmethod
    def get_context_kv_pre_request(request, key):
        request_hash = ContextHolder.make_request_hash(request)
        context = ContextHolder.get_context()
        return context.get(request_hash, {}).get(key) if context else None

    @staticmethod
    def get_context_pre_request(request):
        return ContextHolder.get_context_kv(ContextHolder.make_request_hash(request))

    @staticmethod
    def set_context_pre_request(request, obj):
        ContextHolder.set_context_kv(ContextHolder.make_request_hash(request), obj)

    @staticmethod
    def get_context_kv(key):
        context = getattr(ContextHolder._thread_local, "context", {})
        return context.get(key)

    @staticmethod
    def get_context():
        return getattr(ContextHolder._thread_local, "context", None)
