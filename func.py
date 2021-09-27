#!/usr/bin/python3

def removeDup(data: list[dict[str, str]]):
    return list({list(v.keys())[0]: v for v in data}.values())
