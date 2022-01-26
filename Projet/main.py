from flask import Flask, make_response, render_template, request
import pymongo
from pymongo import MongoClient

import pandas as pd
import plotly
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json

from data_scrap import scrap
from insert_db import insert_value_db


if __name__ == '__main__':
    scrap()
    insert_value_db()