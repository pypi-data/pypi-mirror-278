#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/6/12 下午7:25
@Author  : Gie
@File    : __init__.py.py
@Desc    : 
"""
import sys
from pathlib import Path

path = str(Path(__file__).resolve().parents[2])
sys.path.append(path)
