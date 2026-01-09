from storage import load_data, save_data

def add_trade(signal):
    data = load_data()
    data["open"].append(signal)
    save_data(data)

def close_trade(trade, result):
    data = load_data()
    data["open"] = [t for t in data["open"] if t != trade]

    trade["result"] = result  # WIN or LOSS
    data["closed"].append(trade)

    save_data(data)

def stats():
    data = load_data()
    closed = data["closed"]

    wins = sum(1 for t in closed if t["result"] == "WIN")
    losses = sum(1 for t in closed if t["result"] == "LOSS")

    total = wins + losses
    winrate = (wins / total * 100) if total > 0 else 0

    return {
        "total": total,
        "wins": wins,
        "losses": losses,
        "winrate": round(winrate, 2)
    }
