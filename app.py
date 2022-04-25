from routing import routing_algo

route = routing_algo([[0, 1, 1], [1, 0, 0], [0, 1, 0]])
print(route)

from server import app

if __name__ == "__main__":
    app.run(debug=True)