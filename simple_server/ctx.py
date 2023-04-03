from simple_server.local import Local, LocalProxy


__request_ctx: Local = Local()


request = LocalProxy(__request_ctx, "request")
