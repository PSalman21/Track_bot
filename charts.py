import matplotlib.pyplot as plt


def create_mood_chart(rows):

    dates = [str(row[0]) for row in rows]
    moods = [row[1] for row in rows]

    plt.figure(figsize=(8, 4))

    plt.plot(
        dates,
        moods,
        marker='o'
    )

    plt.title("Настроение по дням")

    plt.xlabel("Дата")
    plt.ylabel("Настроение")

    plt.grid()

    plt.tight_layout()

    path = "mood_chart.png"

    plt.savefig(path)

    plt.close()

    return path