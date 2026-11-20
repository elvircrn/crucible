build = command(
    name = "build",
    run = "python3 build.py",
    emits = ["digest"],
)
workflow(type = "playbook", tasks = [build])
