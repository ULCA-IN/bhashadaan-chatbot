from flask import Flask, request
import requests
from controller.controller import app

if __name__ == "__main__":
    app.run(port=5002)