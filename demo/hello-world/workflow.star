hello = command(
    name = "hello",
    run = "python3 run.py",
    emits = ["message"],
)
workflow(type = "playbook", tasks = [hello])
